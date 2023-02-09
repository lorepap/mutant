import os
import sys
import threading
import traceback
from typing import Any

from helper import arg_parser, context, subprocess_wrappers, utils
from model.mahimahi_trace import MahimahiTrace


class HarmActor(threading.Thread):
    def __init__(self, cmd) -> None:
        threading.Thread.__init__(self)
        self.__cmd = cmd

    def run(self) -> None:

        print(f'Running: {" ".join(self.__cmd)}')
        subprocess_wrappers.check_output(self.__cmd)


class HarmRunner():

    def __init__(self, args: Any) -> None:
        self.__args = args

    def get_mahimahi_cmd(self):

        cmd = ['mm-link']

        utils.check_dir(os.path.join(context.entry_dir, 'log/mahimahi'))

        uplink = os.path.join(context.entry_dir, 'log/mahimahi',
                              f'{self.__args.trace}.{utils.time_to_str()}.up.log')
        downlink = os.path.join(
            context.entry_dir, 'log/mahimahi', f'{self.__args.trace}.{utils.time_to_str()}.down.log')

        up_path, down_path = MahimahiTrace.fromString(self.__args.trace).path()

        cmd = ['mm-link',
               up_path,
               down_path,
               f'--uplink-log={uplink}', f'--downlink-log={downlink}']

        return cmd

    def run_cubic(self) -> HarmActor:

        now = utils.time_to_str()

        tag = 'solo' if self.__args.solo else 'against'

        log_path = os.path.join(
            context.entry_dir,
            'log/iperf/harm',
            f'{self.__args.trace}.cubic.{tag}.{now}.json'
        )

        iperf_cmd = [
            'python3',
            f'{context.ml_dir}/iperf.py',
            # '192.168.1.46',
            self.__args.ip,
            str(self.__args.time),
            log_path,
            'cubic'
        ]

        cmd = self.get_mahimahi_cmd() + iperf_cmd

        if MahimahiTrace.fromString(self.__args.trace) == MahimahiTrace.none:
            cmd = iperf_cmd

        hr = HarmActor(cmd)
        hr.start()

        return hr

    def run_mimic(self) -> HarmActor:

        cmd = [
            'python3',
            f'{context.ml_dir}/predict.py',
            '--all',
            # f'--ip={self.__args.ip}',
            f'--iperf_dir={self.__args.iperf_dir}',
            f'--trace_dir={self.__args.trace_dir}',
            f'-t={self.__args.trace}'
        ]

        hr = HarmActor(cmd)
        hr.start()

        return hr

    def run(self):

        try:

            utils.check_dir(os.path.join(context.entry_dir, 'log/iperf/harm'))

            if self.__args.against:
                self.run_mimic()

            cc = self.run_cubic()
            cc.join()

            print('\n---- Harm is done ----\n')

        except Exception as _:
            print('\n')
            print(traceback.format_exc())


def main():
    args = arg_parser.parse_harm_setup()

    harm = HarmRunner(args)
    harm.run()


if __name__ == '__main__':
    main()
    os._exit(1)
