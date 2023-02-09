#!/usr/bin/env python3

import time
import os
import traceback
from typing import Any

from base import Base
from helper import arg_parser, utils, context
from runner.basic_manager import BasicManager


class BasicRunner(Base):

    def __init__(self, args: Any) -> None:
        super(BasicRunner, self).__init__(args)

        self.prod_config: dict = utils.parse_prod_config()

        self.manager: BasicManager = None

    def run(self) -> None:

        try:

            num_features = int(self.prod_config['num_features'])
            num_fields_kernel = int(self.prod_config['num_fields_kernel'])
            delta = float(self.prod_config['delta'])
            step_wait_seconds = float(self.prod_config['step_wait_seconds'])
            log_range_steps = int(self.prod_config['log_range_steps'])
            trace = self.args.trace
            tag = f'{trace}.bs'

            iperf_logfile = self.start_client(tag)
            log_dir = os.path.join(context.entry_dir, self.args.trace_dir, trace)
            utils.check_dir(log_dir)

            self.manager = BasicManager(self.netlink_communicator, step_wait_seconds, num_fields_kernel,
                                        num_features, delta, log_range_steps, self.nprotocols, trace, 
                                        self.moderator, iperf_logfile, log_dir)
            self.manager.start()
            self.manager.join()

            print('\n---- Done ----\n')


        except Exception as err:
            print('\n')
            print(traceback.format_exc())

            if self.manager:
                self.manager.exit()

def main():

    args = arg_parser.parse_basic_setup()

    runner = BasicRunner(args)
    # runner.run()


    for index in range(args.runs):
        print(f'\n\nRun #{index+1}\n\n')

        runner.run()
        time.sleep(10)

    runner.close_communication()

if __name__ == '__main__':
    main()
    os._exit(1)