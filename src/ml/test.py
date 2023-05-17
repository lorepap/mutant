#!/usr/bin/env python3

import os
import traceback
from argparse import ArgumentError
from typing import Any

from helper import arg_parser, utils, debug
from base import Base
from network.netlink_communicator import NetlinkCommunicator
from runner.base_runner import BaseRunner
from runner.mab.policy.active_explorer import ActiveExplorerRunner
from runner.mab.policy.adaptive_greedy_threshold import \
    AdaptiveGreedyThresholdRunner
from runner.mab.policy.adaptive_greedy_weighted import \
    AdaptiveGreedyWeightedRunner
from runner.mab.policy.bootstrapped_ts import BootstrappedTSRunner
from runner.mab.policy.bootstrapped_ucb import BootstrappedUCBRunner
from runner.mab.policy.epsilon_greedy import EpsilonGreedyRunner
from runner.mab.policy.epsilon_greedy_decay import EpsilonGreedyDecayRunner
from runner.mab.policy.explore_first import ExploreFirstRunner
from runner.mab.policy.separate_classifiers import SeparateClassifiersRunner
from runner.mab.policy.softmax_explorer import SoftmaxExplorerRunner
from runner.mab.policy.adpative_greedy_percentile import AdaptiveGreedyPercentileRunner
from runner.mab.policy.random_policy import RandomRunner


class Tester(Base):

    def __init__(self, args: Any) -> None:
        super(Tester, self).__init__(args)

        self.train_config: dict = utils.parse_training_config()
        self.model_config = utils.parse_models_config()

        self.train_episodes = int(self.train_config['train_episodes'])
        self.test_episodes = int(self.train_config['test_episodes'])
        self.steps_per_episode = int(self.train_config['steps_per_episode']) 

        print(f'We will be testing for {self.test_episodes} epochs\n')

        self.model_runners = self.init_runners()

        if self.train_config["debug"]:
            print("VALUE", self.train_config["debug"])
            debug.set_debug()
        
        self.debug_mode = debug.is_debug_on()
        print("DEBUG MODE", self.debug_mode)

    def init_runners(self) -> dict:

        runners = {

            # 'active_explorer': ActiveExplorerRunner(self.nchoices, lr, num_features, window_len, num_fields_kernel, jiffies_per_state, steps_per_episode, delta, step_wait_seconds, self.netlink_communicator, self.moderator),

            'adaptive_greedy_threshold': AdaptiveGreedyThresholdRunner,

            # 'adaptive_greedy_weighted': AdaptiveGreedyWeightedRunner(self.nchoices, lr, num_features, window_len, num_fields_kernel, jiffies_per_state, steps_per_episode, delta, step_wait_seconds, self.netlink_communicator, self.moderator),

            # 'adaptive_greedy_percentile': AdaptiveGreedyPercentileRunner(self.nchoices, lr, num_features, window_len, num_fields_kernel, jiffies_per_state, steps_per_episode, delta, step_wait_seconds, self.netlink_communicator, self.moderator),

            # 'bootstrapped_ts': BootstrappedTSRunner(self.nchoices, lr, num_features, window_len, num_fields_kernel, jiffies_per_state, steps_per_episode, delta, step_wait_seconds, self.netlink_communicator, self.moderator),

            'bootstrapped_ucb': BootstrappedUCBRunner, 

            # 'epsilon_greedy_decay': EpsilonGreedyDecayRunner(self.nchoices, lr, num_features, window_len, num_fields_kernel, jiffies_per_state, steps_per_episode, delta, step_wait_seconds, self.netlink_communicator, self.moderator),

            'epsilon_greedy': EpsilonGreedyRunner,
            
            # 'explore_first': ExploreFirstRunner(self.nchoices, lr, num_features, window_len, num_fields_kernel, jiffies_per_state, steps_per_episode, delta, step_wait_seconds, self.netlink_communicator, self.moderator),

            # 'separate_classifiers': SeparateClassifiersRunner(self.nchoices, lr, num_features, window_len, num_fields_kernel, jiffies_per_state, steps_per_episode, delta, step_wait_seconds, self.netlink_communicator, self.moderator),

            # 'softmax_explorer': SoftmaxExplorerRunner(self.nchoices, lr, num_features, window_len, num_fields_kernel, jiffies_per_state, steps_per_episode, delta, step_wait_seconds, self.netlink_communicator, self.moderator)
        
            'random_policy': RandomRunner
        }

        return runners

    def run(self) -> None:

        try:

            available_models = self.model_config['models'].keys()

            if self.args.all:

                for indexer, model in enumerate(available_models):
                    self.run_model(model, indexer)

            elif self.args.models and self.args.models is not None:
                selected_models = self.args.models.split()

                for indexer, model in enumerate(selected_models):
                    self.run_model(model, indexer)

            else:
                raise ArgumentError('No model selected to be tested')

            print('\n---- Testing is done ----\n')

        except Exception as _:
            print('\n')
            print(traceback.format_exc())

    def run_model(self, model: str, indexer: int) -> None:
        
        num_features = int(self.train_config['num_features'])
        window_len = int(self.train_config['window_len'])
        jiffies_per_state = int(self.train_config['jiffies_per_state'])
        num_fields_kernel = int(self.train_config['num_fields_kernel'])
        steps_per_episode = int(self.train_config['steps_per_episode']) if not(self.train_config["debug"]) \
            else 5
        delta = float(self.train_config['delta'])
        lr = float(self.train_config['lr'])
        step_wait_seconds = float(self.train_config['step_wait_seconds'])
        
        try:
            print(f'#{indexer}: running test for model: {model}')

            # Start client and server communication (mahimahi + iperf3)
            self.start_communication(tag=f'{self.args.trace}.{model}')

            runner: BaseRunner = self.model_runners[model](
                self.nchoices, lr, num_features, window_len, num_fields_kernel, jiffies_per_state, steps_per_episode, delta, step_wait_seconds, self.netlink_communicator, self.moderator, self.trace, reward_name=self.args.reward, model_name=self.args.model_name
            )

            # test
            try:
                runner.test(self.test_episodes)
                print(f'#{indexer}: test is done for model: {model}')

            except Exception as e:    
                print(f"Error during testing: {e}")
                # close the communication between client and server
                self.stop_communication()
                runner.close()
                raise e

            self.stop_communication()

            runner.close()

        except Exception as _:
            print('\n')
            print(traceback.format_exc())


def main():
    args = arg_parser.parse_test_setup()

    tester = Tester(args)

    for index in range(args.runs):
        print(f'\n\nRun #{index+1}\n\n')

        tester.run()

    tester.close_communication()


if __name__ == '__main__':
    main()
    os._exit(1)
