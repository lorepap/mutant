import os
import threading
import time
import traceback

import numpy as np
from helper import context, utils
from helper.moderator import Moderator
from network.kernel_feedback import KernelRequest
from network.netlink_communicator import NetlinkCommunicator

from runner.base_manager import BaseManager
from runner.base_runner import BaseRunner


class PredictorManager(BaseManager):

    def __init__(self, runners: list, comm: NetlinkCommunicator, wait_ts: float,
                 num_fields_kernel: int, num_features: int, delta: float,
                 log_range_steps: int, trace: str, moderator: Moderator,
                 iperf_logfile: str, protocols: dict, log_dir: str):
        super(PredictorManager, self).__init__(iperf_logfile)

        self.__moderator = moderator
        self.__nl_comm = comm
        self.__wait_ts = wait_ts
        self.__runners = runners
        self.__valid_runners = []
        self.num_fields_kernel = num_fields_kernel
        self.num_features = num_features
        self.floating_error = 1e-12
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
        self.protocol_labels: list = [*protocols]
        self.__log_dir = log_dir

        self.current_runner: BaseRunner = None
        self.log_range_steps = log_range_steps
        self.curr_timestamp = None
        self.__invalid_models: list = list()

        # Thread for kernel info
        self.kernel_thread = KernelRequest(
            self.__nl_comm, self.num_fields_kernel)

        self.kernel_thread.start()

        self.init_runners()

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

            print(f'can start: {self.__moderator.can_start()}')
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

            while float(time.time() - start) <= float(self.__wait_ts):

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

            predicted_protocol = int(self.predict(x))

            print(f'Step {self.stepper}: State has a size of {N}')
            print(
                f'Step {self.stepper}: {self.current_runner.get_model().get_model_name()} predicted arm: {predicted_protocol} - {self.protocol_labels[predicted_protocol]}')

            self.change_cwnd(predicted_protocol)

            reward = self.update_score(self.current_runner, state)

            self.record_verbose(state, self.current_runner)
            self.record(x, reward, self.current_runner)

            self.last_protocol_predicted = predicted_protocol

            print(f'Step {self.stepper}: Done ....\n')
            self.stepper += 1

    def predict(self, x: np.ndarray) -> int:

        exception_occurred = False

        while True:
            try:
                self.current_runner = self.get_best_runner()
                return self.current_runner.predict(x)[0]
            except Exception as err:
                print('\n')
                print(traceback.format_exc())
                print(
                    f'\nStep {self.stepper}: An error occurred while trying to predict with: {self.current_runner.get_model().get_model_name()}')

                self.current_runner.mark_invalid()
                print(
                    f'Step {self.stepper}: Marked {self.current_runner.get_model().get_model_name()} as invalid')
                print(
                    f'Step {self.stepper}: Re-initializing available models')

                exception_occurred = True
                self.__invalid_models.append(
                    self.current_runner.get_model().get_model_name())

            finally:
                if exception_occurred:
                    self.init_runners()

    def update_score(self, runner: BaseRunner, state: np.ndarray) -> None:

        reward = self.get_reward(state)

        runner.update_prod_score(reward)

        print(
            f'Step {self.stepper}: Updated score of {runner.get_model().get_model_name()} to {reward}')
        return reward

    def get_best_runner(self) -> BaseRunner:

        if len(self.__valid_runners) == 0:
            raise RuntimeError('Trained models are not available\n')

        best_runner = self.__valid_runners[0]
        best_score = best_runner.get_prod_score()

        for runner in self.__valid_runners:

            score = runner.get_prod_score()

            if score > best_score:
                best_runner = runner
                best_score = score

        print(f'Step {self.stepper}: Selected {best_runner.get_model().get_model_name()} as best runner with score {best_score}')
        return best_runner

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

    def init_runners(self) -> None:
        print('\n --- Selecting models to be added to poll ---')

        self.__valid_runners = []

        for runner in self.__runners:
            valid = runner.is_valid()
            print(
                f'{runner.get_model().get_model_name()} is valid: {valid}')

            if valid:
                runner.set_best()
                runner.update_prod_score(runner.get_test_score())
                self.__valid_runners.append(runner)
                print(
                    f'{runner.get_model().get_model_name()} has been added to the poll\n\n')

        print('\n')
        if len(self.__valid_runners) == 0:
            raise RuntimeError('Trained models are not available\n')

 
    def exit(self) -> None:
        super().exit()

        print(
            f'\n\nFollowing models were marked as invalid: {self.__invalid_models}')
        

    def record_verbose(self, curr_state, runner: BaseRunner) -> None:
        
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

            line = f'{self.last_protocol_predicted}, {cwnd}, {rtt}, {rtt_dev}, {delivered}, {delivered_diff}, {lost}, {in_flight}, {retrans}, {cwnd_diff}, {self.stepper}, {round(reward, 4)}, {runner.get_tag()}, {timestamp}'
            self.log_traces_verbose = f'{self.log_traces_verbose}\n {line}'
            index += 1

    def record(self, state, reward, runner: BaseRunner) -> None:
        
        if not self.__moderator.can_start():
            return

        cwnd, rtt, rtt_dev, delivered, delivered_diff, lost, in_flight, retrans = state

        cwnd_diff = cwnd - self.last_cwnd

        self.last_cwnd = cwnd

        line = f'{self.last_protocol_predicted}, {cwnd}, {rtt}, {rtt_dev}, {delivered}, {delivered_diff}, {lost}, {in_flight}, {retrans}, {cwnd_diff}, {self.stepper}, {round(reward, 4)}, {runner.get_tag()}, {self.curr_timestamp}'
        self.log_traces = f'{self.log_traces}\n {line}'

        print(f'Step {self.stepper}: {line}')

        if self.stepper % self.log_range_steps == 0:
            self.save_log()
            self.save_log_verbose()
            self.log_traces = ''
            self.log_traces_verbose = ''

    def save_log(self) -> str:
        now_str = utils.time_to_str()
        log_file_name = f'{self.trace}.mimic.{now_str}.csv'
        log_fullpath = os.path.join(self.__log_dir, log_file_name)

        with open(log_fullpath, 'w') as writer:
            writer.write(self.log_traces)

        return log_file_name, log_fullpath

    def save_log_verbose(self) -> str:
        now_str = utils.time_to_str()
        log_file_name = f'{self.trace}.verbose.mimic.{now_str}.csv'
        log_fullpath = os.path.join(self.__log_dir, log_file_name)

        with open(log_fullpath, 'w') as writer:
            writer.write(self.log_traces_verbose)

        return log_file_name, log_fullpath
