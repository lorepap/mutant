import time

import numpy as np
from environment.base_environment import BaseEnvironment
from gym import spaces
from helper.moderator import Moderator
from network.netlink_communicator import NetlinkCommunicator


class MabEnvironment(BaseEnvironment):
    '''Kernel Environment that follows gym interface'''
    metadata = {'render.modes': ['human']}

    def __init__(self, num_features: int,
                 window_len: int, num_fields_kernel: int, jiffies_per_state: int,
                 num_actions: int, steps_per_episode: int, delta: float,
                 step_wait_seconds: float, comm: NetlinkCommunicator, moderator: Moderator) -> None:
        super(MabEnvironment, self).__init__(comm, num_fields_kernel)

        self.moderator = moderator
        self.width_state = num_features
        self.height_state = window_len

        # Kernel state
        self.jiffies_per_state = jiffies_per_state
        self.last_delivered = 0

        # Define action and observation space
        self.action_space = spaces.Discrete(num_actions)
        self.observation_space = spaces.Box(
            low=0, high=np.inf, shape=(self.height_state, self.width_state), dtype=int)

        # Step counter
        self.steps_per_episode = steps_per_episode
        self.step_counter = 0

        # Keep current state
        self.curr_state = np.zeros((self.height_state, self.width_state))

        # Reward
        self.delta = delta
        self.curr_reward = 0
        self.last_rtt = 0

        self.last_cwnd = 0

        self.epoch = -1
        self.allow_save = False
        self.step_wait = step_wait_seconds

    def update_rtt(self, rtt: float) -> None:

        if rtt > 0:
            self.last_rtt = rtt

    def _get_state(self):
        # state = self.curr_state
        state = np.array([])
        received_jiffies = 0

        if self.with_kernel_thread:
            print("[DEBUG] reading data from kernel...")
            timestamp, cwnd, rtt, rtt_dev, mss, delivered, lost, in_flight, retrans, action = self._read_data()
        else:
            timestamp, cwnd, rtt, rtt_dev, mss, delivered, lost, in_flight, retrans, action = self._recv_data()

        print("[DEBUG] current CWND=", cwnd)

        delivered_diff = delivered - self.last_delivered
        self.last_delivered = delivered
        self.update_rtt(rtt)

        curr_kernel_features = np.array(
            [cwnd, rtt, rtt_dev, delivered, delivered_diff, lost, in_flight, retrans])

        curr_timestamp = timestamp

        num_msg = 1

        start = time.time()

        # while received_jiffies < self.jiffies_per_state:
        while float(time.time() - start) <= float(self.step_wait):

            if self.with_kernel_thread:
                timestamp, cwnd, rtt, rtt_dev, mss, delivered, lost, in_flight, retrans, action = self._read_data()
            else:
                timestamp, cwnd, rtt, rtt_dev, mss, delivered, lost, in_flight, retrans, action = self._recv_data()

            delivered_diff = delivered - self.last_delivered
            self.last_delivered = delivered
            self.update_rtt(rtt)

            if timestamp != curr_timestamp:
                curr_kernel_features = np.divide(curr_kernel_features, num_msg)

                if state.shape[0] == 0:
                    state = np.array(curr_kernel_features).reshape(
                        1, self.width_state)
                else:
                    state = np.vstack(
                        (state, np.array(curr_kernel_features).reshape(1, self.width_state)))

                curr_kernel_features = np.array(
                    [cwnd, rtt, rtt_dev, delivered, delivered_diff, lost, in_flight, retrans])

                curr_timestamp = timestamp

                num_msg = 1

                received_jiffies += 1

            else:
                # sum new reading to existing readings
                curr_kernel_features = np.add(curr_kernel_features,
                                              np.array([cwnd, rtt, rtt_dev, delivered, delivered_diff, lost, in_flight, retrans]))
                num_msg += 1

        self.curr_state = state
        return (state, action)

    def _get_reward(self):
        rewards = []
        binary_rewards = []

        for state in self.curr_state:

            cwnd, rtt, _, delivered, _, lost, _, _ = state

            if rtt == 0:
                rtt = self.last_rtt

            throughput = cwnd / (rtt / self.nb)
            p = lost / (lost + delivered)

            reward = throughput - self.delta * throughput * (1 / (1 - p))

            binary_reward = 0 if reward <= self.curr_reward else 1

            binary_rewards.append(binary_reward)
            rewards.append(reward)

        self.curr_reward = np.mean(rewards)

        return binary_rewards, rewards

    def record(self, state, reward, step, action):
        cwnd, rtt, rtt_dev, delivered, delivered_diff, lost, in_flight, retrans = state

        if cwnd == 0:
            return

        cwnd_diff = cwnd - self.last_cwnd

        self.last_cwnd = cwnd

        self.log_traces = f'{self.log_traces}\n {action}, {cwnd}, {rtt}, {rtt_dev}, {delivered}, {delivered_diff}, {lost}, {in_flight}, {retrans}, {cwnd_diff}, {step}, {round(self.curr_reward, 4)}, {round(reward, 4)}'

    def step(self, action):
        self._change_cwnd(int(action))
        observation, observed_action = self._get_state()
        binary_rewards, rewards = self._get_reward()

        done = False if self.step_counter != self.steps_per_episode-1 else True
        self.step_counter = (self.step_counter+1) % self.steps_per_episode

        avg_reward = round(np.mean(rewards), 4)
        avg_binary_reward = np.bincount(binary_rewards).argmax()

        info = {'reward': avg_reward}
        data = {'rewards': binary_rewards, 'obs': observation}

        print(
            f'\nStep: {self.step_counter} \t Sent Action: {action} \t Received Action: {observed_action} \t Epoch: {self.epoch} | Reward: {avg_reward} ({np.mean(avg_binary_reward)})  | Data Size: {observation.shape[0]}')

        counter = self.step_counter if self.step_counter != 0 else self.steps_per_episode

        step = self.epoch * self.steps_per_episode + counter

        just_observed = np.mean(observation, axis=0)

        if self.allow_save:
            self.record(just_observed, avg_binary_reward,
                        step, observed_action)

        if not self.moderator.can_start() and step > 1:
            done = True

        return data, avg_reward, done, info

    def reset(self):
        self._init_communication()
        self._change_cwnd(0)
        observation, observed_action = self._get_state()

        self.epoch += 1

        data = {'obs': observation}

        return data  # reward, done, info can't be included
