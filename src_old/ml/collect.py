#!/usr/bin/env python3

import os
import traceback
import time
from argparse import ArgumentError
from typing import Any

from base import Base
from helper import arg_parser, utils, context
from runner.collector_manager import CollectorManager


class Collector(Base):

    def __init__(self, args: Any) -> None:
        super(Collector, self).__init__(args)

        self.model_config: dict = utils.parse_models_config()

        self.prod_config: dict = utils.parse_prod_config()

        self.manager: CollectorManager = None

    def run(self) -> None:

        try:

            print('\n--- Running ---\n')

            protocolSize = len(self.nprotocols.keys())
            max_steps = int(self.args.logsize)

            if self.args.all:

                for index, protocol in enumerate(self.nprotocols.keys()):
                    islast = index == protocolSize - 1
                    self.run_protocol(protocol, max_steps,  islast)

            elif self.args.protocols and self.args.protocols is not None:
                selected_protocols = self.args.protocols.split()

                for index, protocol in enumerate(selected_protocols):
                    if protocol in self.nprotocols:
                        islast = index == protocolSize - 1
                        self.run_protocol(protocol, max_steps,  islast)

            else:
                raise ArgumentError('No protocols selected to be collected')

            print('\n ---- Done ----')

        except Exception as error:
            print('\n')
            print(traceback.format_exc())

            if self.manager:
                self.manager.exit()

    def run_protocol(self, protocol: str, max_steps: int, islast: bool) -> None:

        try:

            num_features = int(self.prod_config['num_features'])
            num_fields_kernel = int(self.prod_config['num_fields_kernel'])
            delta = float(self.prod_config['delta'])
            step_wait_seconds = float(self.prod_config['step_wait_seconds'])
            log_range_steps = int(self.prod_config['log_range_steps'])
            trace = self.args.trace
            tag = f'{self.args.trace}.{protocol}'

            iperf_logfile = self.start_client(tag)
            log_dir = os.path.join(context.entry_dir, self.args.trace_dir, trace)
            utils.check_dir(log_dir)

            self.manager = CollectorManager(self.netlink_communicator, step_wait_seconds, num_fields_kernel,
                                            num_features, delta, protocol, max_steps, self.nprotocols, trace, 
                                            log_range_steps, self.moderator, iperf_logfile, log_dir)
            self.manager.start()
            self.manager.join()

        except Exception as _:
            print('\n')
            print(traceback.format_exc())


def main():
    args = arg_parser.parse_collect_setup()

    collector = Collector(args)

    for index in range(args.runs):
        print(f'\n\nRun #{index+1}\n\n')

        collector.run()
        time.sleep(10)

    collector.close_communication()


if __name__ == '__main__':
    main()
    os._exit(1)
