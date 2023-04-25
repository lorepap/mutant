"""
python src/tests/test_mimic_one_protocol.py -prot cubic -t att.lte.driving -rw orca 
"""

import sys
import os
import traceback
from typing import Any

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.ml.helper import context
sys.path.append(context.ml_dir)
from src.ml.native_base import NativeBase
from src.ml.helper import arg_parser, utils, debug
from src.ml.runner.base_runner import BaseRunner
from src.ml.runner.single.single_runner import SingleBaseRunner
from src.ml.helper import utils

class Tester(NativeBase):

    def __init__(self, args: Any) -> None:
        super(Tester, self).__init__(args)

        self.train_config: dict = utils.parse_training_config()
        self.model_config = utils.parse_models_config()
        self.test_episodes = int(self.train_config['test_episodes'])
        self.steps_per_episode = int(self.train_config['steps_per_episode'])
        self.reward_name = args.reward
        self.protocol = args.protocol

        print(f'We will be testing for {self.test_episodes} epochs\n')

        self.model_runner = self.init_runner()

        if self.train_config["debug"]:
            print("VALUE", self.train_config["debug"])
            debug.set_debug()
        
        self.debug_mode = debug.is_debug_on()
        print("DEBUG MODE", self.debug_mode)

    def init_runner(self) -> dict:

        num_features = int(self.train_config['num_features'])
        window_len = int(self.train_config['window_len'])
        jiffies_per_state = int(self.train_config['jiffies_per_state'])
        num_fields_kernel = int(self.train_config['num_fields_kernel'])
        steps_per_episode = int(self.train_config['steps_per_episode']) if not(self.train_config["debug"]) \
            else 5
        delta = float(self.train_config['delta'])
        lr = float(self.train_config['lr'])
        step_wait_seconds = float(self.train_config['step_wait_seconds'])

        runner = SingleBaseRunner(
            self.nchoices,
            lr, 
            num_features, 
            window_len, 
            num_fields_kernel, 
            jiffies_per_state, 
            steps_per_episode, 
            delta, 
            step_wait_seconds, 
            self.netlink_communicator, 
            self.moderator, 
            self.trace,
            protocol=self.protocol,
            reward_name=self.reward_name
            )
        
        return runner

    def run_model(self, protocol: str, indexer: int) -> None:
        try:
            print(f'#{indexer}: running test for model: {protocol}')

            # Start client and server communication (mahimahi + iperf3)
            self.start_communication(tag=f'{self.args.trace}.{protocol}')

            runner: BaseRunner = self.model_runner

            # test
            try:
                runner.test(self.test_episodes)
                print(f'#{indexer}: test is done for model: {protocol}')

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

        tester.run_model(args.protocol, index)

    tester.close_communication()

if __name__ == "__main__":
    main()
    os._exit(1)