#!/usr/bin/env python3

import os
import time
import traceback
from typing import Any

from helper import arg_parser, utils, context
from base import Base
from runner.predictor_manager import PredictorManager
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
from runner.base_runner import BaseRunner


class Predictor(Base):

    def __init__(self, args: Any) -> None:
        super(Predictor, self).__init__(args)

        self.model_config: dict = utils.parse_models_config()
        self.prod_config: dict = utils.parse_prod_config()

        self.model_runners = self.init_runners()
        self.manager: PredictorManager = None

    def init_runners(self) -> dict:

        num_features = int(self.prod_config['num_features'])
        window_len = int(self.prod_config['window_len'])
        jiffies_per_state = int(self.prod_config['jiffies_per_state'])
        num_fields_kernel = int(self.prod_config['num_fields_kernel'])
        steps_per_episode = int(self.prod_config['steps_per_episode'])
        delta = float(self.prod_config['delta'])
        lr = float(self.prod_config['lr'])
        step_wait_seconds = float(self.prod_config['step_wait_seconds'])

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
            runners = []

            if self.args.all:

                for model in available_models:
                    runner: BaseRunner = self.model_runners[model]
                    runners.append(runner)

            elif self.args.models and self.args.models is not None:
                selected_models = self.args.models.split()

                for model in selected_models:
                    runner: BaseRunner = self.model_runners[model]
                    runners.append(runner)

            else:
                raise Exception('No model selected')

            num_features = int(self.prod_config['num_features'])
            num_fields_kernel = int(self.prod_config['num_fields_kernel'])
            delta = float(self.prod_config['delta'])
            step_wait_seconds = float(self.prod_config['step_wait_seconds'])
            log_range_steps = int(self.prod_config['log_range_steps'])
            trace = self.args.trace
            tag = f'{trace}.mimic'

            iperf_logfile = self.start_client(tag)
            log_dir = os.path.join(context.entry_dir, self.args.trace_dir, trace)
            utils.check_dir(log_dir)

            self.manager = PredictorManager(runners, self.netlink_communicator, step_wait_seconds,
                                            num_fields_kernel, num_features, delta, log_range_steps, trace, self.moderator,
                                            iperf_logfile, self.nprotocols, log_dir)
            self.manager.start()
            self.manager.join()

            print('\n---- Prediction is done ----\n')

        except Exception as _:
            print('\n')
            print(traceback.format_exc())

            if self.manager:
                self.manager.exit()


def main():
    args = arg_parser.parse_predict_setup()

    predictor = Predictor(args)
    # predictor.run()

    for index in range(args.runs):
        print(f'\n\nRun #{index+1}\n\n')

        predictor.run()
        time.sleep(10)

    predictor.close_communication()


if __name__ == '__main__':
    main()
    os._exit(1)
