import numpy as np
from gym import spaces
from environment.base_environment import BaseEnvironment
from helper.moderator import Moderator
from network.netlink_communicator import NetlinkCommunicator


class OwlEnvironment(BaseEnvironment):
    '''Kernel Environment that follows gym interface'''
    metadata = {'render.modes': ['human']}

    def __init__(self, num_features: int,
                 window_len: int, num_fields_kernel: int, jiffies_per_state: int,
                 num_actions: int, steps_per_episode: int, delta: float, 
                 comm: NetlinkCommunicator, moderator: Moderator) -> None:
        super(OwlEnvironment, self).__init__(comm, num_fields_kernel)

        self.moderator = moderator
        height_state = num_features
        width_state = window_len

        # Kernel state
        self.jiffies_per_state = jiffies_per_state
        self.last_delivered = 0

        # Define action and observation space
        self.action_space = spaces.Discrete(num_actions)
        self.observation_space = spaces.Box(
            low=0, high=np.inf, shape=(height_state, width_state), dtype=int)

        # Step counter
        self.steps_per_episode = steps_per_episode
        self.step_counter = 0

        # Keep current state
        self.curr_state = np.zeros((height_state, width_state))

        # Reward
        self.delta = delta
        self.curr_reward = 0
        self.last_rtt = 0

        self.last_cwnd = 0

        self.cwnd_dic = [0, -10, -3, -1, 1, 3, 10]

        self.epoch = -1
        self.allow_save = False

    def update_rtt(self, rtt: float) -> None:

        if rtt > 0:
            self.last_rtt = rtt

    def _get_state(self):
        state = self.curr_state
        recevied_jiffies = 0

        if self.with_kernel_thread:
            timestamp, cwnd, rtt, rtt_dev, mss, delivered, lost, in_flight, retrans, action = self._read_data()
        else:
            timestamp, cwnd, rtt, rtt_dev, mss, delivered, lost, in_flight, retrans, action = self._recv_data()

        delivered_diff = delivered - self.last_delivered
        self.last_delivered = delivered
        self.update_rtt(rtt)

        curr_kernel_features = np.array(
            [cwnd, rtt, rtt_dev, delivered, delivered_diff, lost, in_flight, retrans])

        curr_timestamp = timestamp

        num_msg = 1

        while recevied_jiffies < self.jiffies_per_state:

            if self.with_kernel_thread:
                timestamp, cwnd, rtt, rtt_dev, mss, delivered, lost, in_flight, retrans, action = self._read_data()
            else:
                timestamp, cwnd, rtt, rtt_dev, mss, delivered, lost, in_flight, retrans, action = self._recv_data()

            delivered_diff = delivered - self.last_delivered
            self.last_delivered = delivered
            self.update_rtt(rtt)

            if timestamp != curr_timestamp:
                curr_kernel_features = np.divide(curr_kernel_features, num_msg)

                curr_features = curr_kernel_features

                state = np.roll(state, -1, axis=1)

                state[:, -1] = curr_features

                curr_kernel_features = np.array(
                    [cwnd, rtt, rtt_dev, delivered, delivered_diff, lost, in_flight, retrans])

                curr_timestamp = timestamp

                num_msg = 1

                recevied_jiffies += 1

            else:
                curr_kernel_features = np.add(curr_kernel_features,
                                              np.array([cwnd, rtt, rtt_dev, delivered, delivered_diff, lost, in_flight, retrans]))
                num_msg += 1

        self.curr_state = state
        return (state, action)

    def _get_reward(self):

        cwnd, rtt, _, delivered, delivered_diff, lost, _, _ = np.mean(self.curr_state, axis=1)

        if rtt == 0:
            rtt = self.last_rtt

        throughput = cwnd / (rtt / self.nb)
        p = lost / (lost + delivered)

        reward = throughput - self.delta * throughput * (1 / (1 - p))

        binary_reward = 0 if reward <= self.curr_reward else 1

        self.curr_reward = reward

        return binary_reward

    def record(self, state, reward, step, action):
        yshape = state.shape[1]
        cwnd = int(state[0][yshape-1])
        rtt = int(state[1][yshape-1])
        rtt_dev = int(state[2][yshape-1])
        delivered = int(state[3][yshape-1])
        delivered_diff = int(state[4][yshape-1])
        lost = int(state[5][yshape-1])
        in_flight = int(state[6][yshape-1])
        retrans = int(state[7][yshape-1])

        if cwnd == 0:
            return

        cwnd_diff = cwnd - self.last_cwnd

        self.last_cwnd = cwnd

        self.log_traces = f"{self.log_traces}\n {1}, {action}, {cwnd}, {rtt}, {rtt_dev}, {delivered}, {delivered_diff}, {lost}, {in_flight}, {retrans}, {cwnd_diff}, {step}, {round(self.curr_reward, 4)}, {round(reward, 4)}"

    def step(self, action):
        self._change_cwnd(int(action))
        observation, observed_action = self._get_state()
        reward = self._get_reward()
        done = False if self.step_counter != self.steps_per_episode-1 else True
        self.step_counter = (self.step_counter+1) % self.steps_per_episode

        info = {  # 'observation': observation,
            'reward': reward}

        print(f'\nStep: {self.step_counter} | Sent Action: {action} | Received Action: {observed_action} | Reward: {self.curr_reward} ({reward}) | epoch: {self.epoch}')

        counter = self.step_counter if self.step_counter != 0 else self.steps_per_episode

        step = self.epoch * self.steps_per_episode + counter

        if self.allow_save:
            self.record(observation, reward, step, observed_action)

        
        if not self.moderator.can_start() and step > 1:
            done = True

        return observation, reward, done, info

    def reset(self):
        self._init_communication()
        self._change_cwnd(0)
        observation, observed_action = self._get_state()

        self.epoch += 1

        return observation  # reward, done, info can't be included
