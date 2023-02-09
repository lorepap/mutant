import os
import threading
import time
import traceback

import numpy as np
from helper import context, utils
from helper.moderator import Moderator
from network.kernel_feedback import KernelRequest
from network.netlink_communicator import NetlinkCommunicator

from runner.base_runner import BaseRunner
from runner.base_manager import BaseManager


class CollectorManager(BaseManager):

    def __init__(self, comm: NetlinkCommunicator, wait_ts: float,
                 num_fields_kernel: int, num_features: int, delta: float,
                 protocol_name: str, max_steps: int, protocols: dict, trace: str,
                 log_range_steps: int, moderator: Moderator, iperf_logfile: str, log_dir: str):
        super(CollectorManager, self).__init__(iperf_logfile)

        self.__moderator = moderator
        self.netlink_communicator = comm
        self.wait_ts = wait_ts
        self.possible_runners = []
        self.num_fields_kernel = num_fields_kernel
        self.num_features = num_features
        self.floating_error = 1e-12
        self.nb = 1e9
        self.delta = delta
        self.last_protocol_predicted = 0
        self.last_cwnd = 0
        self.last_delivered = 0
        self.curr_timestamp = 0
        self.stepper = 1
        self.last_rtt = 0
        self.timestamps = []
        self.trace = trace
        self.mss = 0
        self.protocol_labels = protocols
        self.log_dir = log_dir

        self.current_runner: BaseRunner = None
        self.protocol = self.protocol_labels[protocol_name]
        self.protocol_name = protocol_name
        self.max_steps = max_steps
        self.log_range_steps = log_range_steps

        # Thread for kernel info
        self.kernel_thread = KernelRequest(
            self.netlink_communicator, self.num_fields_kernel)

        self.kernel_thread.start()

    def read_data(self):
        kernel_info = self.kernel_thread.queue.get()
        self.kernel_thread.queue.task_done()
        return kernel_info

    def change_cwnd(self, protocol):

        msg = self.netlink_communicator.create_netlink_msg(
            'SENDING ACTION', msg_flags=self.netlink_communicator.ACTION_FLAG, msg_seq=protocol)

        self.netlink_communicator.send_msg(msg)

        print(
            f'Step {self.stepper}: Changed protocol to {protocol}')

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

            predicted_protocol = self.protocol

            print(f'Step {self.stepper}: State has a size of {N}')

            self.change_cwnd(predicted_protocol)

            reward = self.get_reward(state)

            self.record_verbose(state)
            self.record(x, reward)

            print(f'Step {self.stepper}: Done ....\n')
            self.stepper += 1
            self.last_protocol_predicted = predicted_protocol

            if self.done():
                self.exit()

    def done(self) -> bool:
        return self.stepper > self.max_steps

    def calculate_reward(self, state: np.ndarray) -> float:
        cwnd, rtt, _, delivered, _, lost, _, _ = state

        if rtt == 0:
            rtt = self.last_rtt
            print(f'Step {self.stepper}: rtt is {rtt}')

        throughput = cwnd / (rtt / self.nb)
        p = lost / (lost + delivered)

        reward = throughput - self.delta * throughput * (1 / (1 - p))

        return reward

    def record_verbose(self, curr_state: np.ndarray) -> None:

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

            line = f'{self.last_protocol_predicted}, {cwnd}, {rtt}, {rtt_dev}, {delivered}, {delivered_diff}, {lost}, {in_flight}, {retrans}, {cwnd_diff}, {self.stepper}, {round(reward, 4)}, none, {timestamp}'
            self.log_traces_verbose = f'{self.log_traces_verbose}\n {line}'
            index += 1

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

    def record(self, state, reward) -> None:

        if not self.__moderator.can_start():
            return

        cwnd, rtt, rtt_dev, delivered, delivered_diff, lost, in_flight, retrans = state

        cwnd_diff = cwnd - self.last_cwnd

        self.last_cwnd = cwnd

        line = f'{self.last_protocol_predicted}, {cwnd}, {rtt}, {rtt_dev}, {delivered}, {delivered_diff}, {lost}, {in_flight}, {retrans}, {cwnd_diff}, {self.stepper}, {round(reward, 4)}, none, {self.curr_timestamp}'
        self.log_traces = f'{self.log_traces}\n {line}'

        print(f'Step {self.stepper}: {line}')

        if self.stepper % self.log_range_steps == 0:
            self.save_log()
            self.save_log_verbose()
            self.log_traces = ''
            self.log_traces_verbose = ''

    def save_log(self) -> str:
        now_str = utils.time_to_str()
        log_file_name = f'{self.trace}.{self.protocol_name}.{now_str}.csv'
        log_fullpath = os.path.join(self.log_dir, log_file_name)

        with open(log_fullpath, 'w') as writer:
            writer.write(self.log_traces)

        return log_file_name, log_fullpath

    def save_log_verbose(self) -> str:
        now_str = utils.time_to_str()
        log_file_name = f'{self.trace}.verbose.{self.protocol_name}.{now_str}.csv'
        log_fullpath = os.path.join(self.log_dir, log_file_name)

        with open(log_fullpath, 'w') as writer:
            writer.write(self.log_traces_verbose)

        return log_file_name, log_fullpath
