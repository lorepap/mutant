#!/usr/bin/env python3

import os
import traceback
from argparse import ArgumentError
from typing import Any

from helper import arg_parser, utils
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
from runner.owl.owl_runner import OwlRunner


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

    def init_runners(self) -> dict:

        num_features = int(self.train_config['num_features'])
        window_len = int(self.train_config['window_len'])
        jiffies_per_state = int(self.train_config['jiffies_per_state'])
        num_fields_kernel = int(self.train_config['num_fields_kernel'])
        steps_per_episode = int(self.train_config['steps_per_episode'])
        delta = float(self.train_config['delta'])
        lr = float(self.train_config['lr'])
        step_wait_seconds = float(self.train_config['step_wait_seconds'])

        runners = {
            'owl': OwlRunner(self.nchoices, lr, num_features, window_len, num_fields_kernel, jiffies_per_state, steps_per_episode, delta, self.netlink_communicator, self.moderator),

            'active_explorer': ActiveExplorerRunner(self.nchoices, lr, num_features, window_len, num_fields_kernel, jiffies_per_state, steps_per_episode, delta, step_wait_seconds, self.netlink_communicator, self.moderator),

            'adaptive_greedy_threshold': AdaptiveGreedyThresholdRunner(self.nchoices, lr, num_features, window_len, num_fields_kernel, jiffies_per_state, steps_per_episode, delta, step_wait_seconds, self.netlink_communicator, self.moderator),

            'adaptive_greedy_weighted': AdaptiveGreedyWeightedRunner(self.nchoices, lr, num_features, window_len, num_fields_kernel, jiffies_per_state, steps_per_episode, delta, step_wait_seconds, self.netlink_communicator, self.moderator),

            'adaptive_greedy_percentile': AdaptiveGreedyPercentileRunner(self.nchoices, lr, num_features, window_len, num_fields_kernel, jiffies_per_state, steps_per_episode, delta, step_wait_seconds, self.netlink_communicator, self.moderator),

            'bootstrapped_ts': BootstrappedTSRunner(self.nchoices, lr, num_features, window_len, num_fields_kernel, jiffies_per_state, steps_per_episode, delta, step_wait_seconds, self.netlink_communicator, self.moderator),

            'bootstrapped_ucb': BootstrappedUCBRunner(self.nchoices, lr, num_features, window_len, num_fields_kernel, jiffies_per_state, steps_per_episode, delta, step_wait_seconds, self.netlink_communicator, self.moderator),

            'epsilon_greedy_decay': EpsilonGreedyDecayRunner(self.nchoices, lr, num_features, window_len, num_fields_kernel, jiffies_per_state, steps_per_episode, delta, step_wait_seconds, self.netlink_communicator, self.moderator),

            'epsilon_greedy': EpsilonGreedyRunner(self.nchoices, lr, num_features, window_len, num_fields_kernel, jiffies_per_state, steps_per_episode, delta, step_wait_seconds, self.netlink_communicator, self.moderator),

            'explore_first': ExploreFirstRunner(self.nchoices, lr, num_features, window_len, num_fields_kernel, jiffies_per_state, steps_per_episode, delta, step_wait_seconds, self.netlink_communicator, self.moderator),

            'separate_classifiers': SeparateClassifiersRunner(self.nchoices, lr, num_features, window_len, num_fields_kernel, jiffies_per_state, steps_per_episode, delta, step_wait_seconds, self.netlink_communicator, self.moderator),

            'softmax_explorer': SoftmaxExplorerRunner(self.nchoices, lr, num_features, window_len, num_fields_kernel, jiffies_per_state, steps_per_episode, delta, step_wait_seconds, self.netlink_communicator, self.moderator)
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
        try:
            print(f'#{indexer}: running test for model: {model}')

            model_tag = 'owl.agent' if model == 'owl' else model

            self.start_client(f'{self.args.trace}.{model_tag}')

            runner: BaseRunner = self.model_runners[model]

            # test
            runner.test(self.test_episodes, self.args.trace)

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
