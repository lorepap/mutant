import os
import threading
import time
import traceback
from helper.moderator import Moderator

import numpy as np
from helper import context, utils
from network.kernel_feedback import KernelRequest
from network.netlink_communicator import NetlinkCommunicator

from runner.base_runner import BaseRunner
from runner.base_manager import BaseManager


class BasicManager(BaseManager):

    def __init__(self, comm: NetlinkCommunicator, wait_ts: float, num_fields_kernel: int, num_features: int, 
    delta: float, log_range_steps: int, protocols: dict, trace: str, moderator: Moderator, iperf_logfile: str, log_dir: str):
        super(BasicManager, self).__init__(iperf_logfile)

        self.__nl_comm = comm
        self.wait_ts = wait_ts
        self.num_fields_kernel = num_fields_kernel
        self.num_features = num_features
        self.nb = 1e9
        self.delta = delta
        self.last_protocol_predicted = 0
        self.last_cwnd = 0
        self.last_delivered = 0
        self.stepper = 1
        self.mss = 0
        self.last_rtt = 0
        self.timestamps: list = []
        self.trace = trace
        self.protocols: dict = protocols
        self.protocol_labels: list = [*protocols]
        self.log_range_steps = log_range_steps
        self.curr_timestamp = None
        self.protocol_index = 0
        self.__moderator = moderator
        self.log_dir = log_dir

        # Thread for kernel info
        self.kernel_thread = KernelRequest(
            self.__nl_comm, self.num_fields_kernel)

        self.kernel_thread.start()

        self.scores = {}
        self.init_protocols()

    def read_data(self):
        kernel_info = self.kernel_thread.queue.get()
        self.kernel_thread.queue.task_done()
        return kernel_info

    def change_cwnd(self, protocol):

        msg = self.__nl_comm.create_netlink_msg(
            'SENDING ACTION', msg_flags=self.__nl_comm.ACTION_FLAG, msg_seq=protocol)

        self.__nl_comm.send_msg(msg)

        print(
            f'Step {self.stepper}: Changed protocol to {protocol} - {self.protocol_labels[protocol]}')

    def update_rtt(self, rtt: float) -> None:

        if rtt > 0:
            self.last_rtt = rtt

    def run(self) -> None:
        while self.allow_run:

            if not self.__moderator.can_start():
                if self.stepper > 1:
                    self.exit()
                    continue
                
                time.sleep(1)
                continue

            print(f'\nStep {self.stepper}: Running ....')

            state = np.array([])
            self.timestamps = []

            timestamp, cwnd, rtt, rtt_dev, mss, delivered, lost, in_flight, retrans, protocol = self.read_data()

            delivered_diff = delivered - self.last_delivered
            self.last_delivered = delivered
            self.mss = mss
            self.update_rtt(rtt)
            self.timestamps.append(timestamp)

            curr_kernel_features = np.array(
                [cwnd, rtt, rtt_dev, delivered, delivered_diff, lost, in_flight, retrans])

            self.curr_timestamp = timestamp

            start = time.time()
            num_msg = 1

            while float(time.time() - start) <= float(self.wait_ts):

                timestamp, cwnd, rtt, rtt_dev, mss, delivered, lost, in_flight, retrans, protocol = self.read_data()
                self.mss = mss
                self.timestamps.append(timestamp)
                self.update_rtt(rtt)

                if timestamp != self.curr_timestamp:
                    curr_kernel_features = np.divide(
                        curr_kernel_features, num_msg)

                    if state.shape[0] == 0:
                        state = np.array(curr_kernel_features).reshape(
                            1, self.num_features)
                    else:
                        state = np.vstack(
                            (state, np.array(curr_kernel_features).reshape(1, self.num_features)))

                    curr_kernel_features = np.array(
                        [cwnd, rtt, rtt_dev, delivered, delivered_diff, lost, in_flight, retrans])

                    self.curr_timestamp = timestamp

                    num_msg = 1

                else:
                    # sum new reading to existing readings
                    curr_kernel_features = np.add(curr_kernel_features,
                                                  np.array([cwnd, rtt, rtt_dev, delivered, delivered_diff, lost, in_flight, retrans]))
                    num_msg += 1

            N, _ = state.shape

            x = np.mean(state, axis=0)

            predicted_protocol = self.predict(state)

            print(f'Step {self.stepper}: State has a size of {N}')
            print(
                f'Step {self.stepper}: Next protocol is {self.protocols[predicted_protocol]} - {predicted_protocol} ')

            self.change_cwnd(self.protocols[predicted_protocol])

            # Update reward of last protocol since it caused the just recorded state
            reward = self.update_score(
                self.protocol_labels[self.last_protocol_predicted], state)

            self.record_verbose(state, predicted_protocol)
            self.record(x, reward, predicted_protocol)

            self.last_protocol_predicted = self.protocols[predicted_protocol]

            print(f'Step {self.stepper}: Done ....\n')
            self.stepper += 1

    def init_protocols(self) -> None:

        for p in self.protocol_labels:
            self.scores[p] = 0

    def all_protocols_has_scores(self) -> None:
        return self.protocol_index >= len(self.protocol_labels)

    def predict(self, state: np.ndarray) -> str:

        if self.all_protocols_has_scores():
            return self.get_best_protocol()

        else:
            self.protocol_index += 1
            return self.get_best_protocol() if self.protocol_index == len(self.protocol_labels) else self.protocol_labels[self.protocol_index]

    def update_score(self, protocol: str, state: np.ndarray) -> None:

        reward = self.get_reward(state)

        self.scores[protocol] = reward

        print(
            f'Step {self.stepper}: Updated score of {protocol} to {reward}')
        return reward

    def get_best_protocol(self) -> BaseRunner:

        if len(self.protocol_labels) == 0:
            raise RuntimeError(
                'TCP Congestion Avoidance Protocols are not available\n')

        best_protocol = self.protocol_labels[0]
        best_score = self.scores[best_protocol]

        for protocol in self.scores.keys():

            score = self.scores[protocol]

            if score > best_score:
                best_protocol = protocol
                best_score = score

        print(
            f'Step {self.stepper}: Selected {best_protocol} as best protocol with score {best_score}')
        return best_protocol

    def calculate_reward(self, state: np.ndarray) -> float:
        cwnd, rtt, _, delivered, _, lost, _, _ = state

        if rtt == 0:
            rtt = self.last_rtt
            print(f'Step {self.stepper}: rtt is {rtt}')

        throughput = cwnd / (rtt / self.nb)
        p = lost / (lost + delivered)

        reward = throughput - self.delta * throughput * (1 / (1 - p))

        return reward

    def get_reward(self, curr_state: np.ndarray) -> float:
        rewards = []

        for state in curr_state:

            try:

                reward = self.calculate_reward(state)

                rewards.append(reward)

            except Exception as err:
                print('\n')
                print(traceback.format_exc())

        return np.mean(rewards)

    def exit(self) -> None:
        super().exit()

    def record_verbose(self, curr_state, protocol: str) -> None:

        if not self.__moderator.can_start():
            return

        last_cwnd = self.last_cwnd
        index = 0

        for state in curr_state:
            cwnd, rtt, rtt_dev, delivered, delivered_diff, lost, in_flight, retrans = state
            cwnd_diff = cwnd - last_cwnd
            last_cwnd = cwnd
            reward = self.calculate_reward(state)
            timestamp = self.timestamps[index]

            line = f'{self.last_protocol_predicted}, {cwnd}, {rtt}, {rtt_dev}, {delivered}, {delivered_diff}, {lost}, {in_flight}, {retrans}, {cwnd_diff}, {self.stepper}, {round(reward, 4)}, {protocol}, {timestamp}'
            self.log_traces_verbose = f'{self.log_traces_verbose}\n {line}'
            index += 1

    def record(self, state, reward, protocol: str) -> None:

        if not self.__moderator.can_start():
            return

        cwnd, rtt, rtt_dev, delivered, delivered_diff, lost, in_flight, retrans = state

        cwnd_diff = cwnd - self.last_cwnd

        self.last_cwnd = cwnd

        line = f'{self.last_protocol_predicted}, {cwnd}, {rtt}, {rtt_dev}, {delivered}, {delivered_diff}, {lost}, {in_flight}, {retrans}, {cwnd_diff}, {self.stepper}, {round(reward, 4)}, {protocol}, {self.curr_timestamp}'
        self.log_traces = f'{self.log_traces}\n {line}'

        print(f'Step {self.stepper}: {line}')

        if self.stepper % self.log_range_steps == 0:
            self.save_log()
            self.save_log_verbose()
            self.log_traces = ''
            self.log_traces_verbose = ''

    def save_log(self) -> str:
        now_str = utils.time_to_str()
        log_file_name = f'{self.trace}.bs.{now_str}.csv'
        log_fullpath = os.path.join(self.log_dir, log_file_name)

        with open(log_fullpath, 'w') as writer:
            writer.write(self.log_traces)

        return log_file_name, log_fullpath

    def save_log_verbose(self) -> str:
        now_str = utils.time_to_str()
        log_file_name = f'{self.trace}.verbose.bs.{now_str}.csv'
        log_fullpath = os.path.join(self.log_dir, log_file_name)

        with open(log_fullpath, 'w') as writer:
            writer.write(self.log_traces_verbose)

        return log_file_name, log_fullpath
