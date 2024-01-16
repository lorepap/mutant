import os
import sys
import threading
import traceback
from typing import Any

from helper import arg_parser, context, subprocess_wrappers, utils
from model.mahimahi_trace import MahimahiTrace
from iperf.iperf_server import IperfServer


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

        
        base_path = os.path.join(context.entry_dir, "log", "iperf", "server")
        filename = f'server_harm.log'
        log_filename = f'{base_path}/{filename}'
        os.makedirs(os.path.dirname(log_filename), exist_ok=True)
        self.server = IperfServer(log_filename, port=5202)
        self.server.start()

        iperf_cmd = [
            'python3',
            f'{context.ml_dir}/iperf.py',
            # '192.168.1.46',
            self.__args.ip,
            str(self.__args.time),
            log_path,
            os.path.join(context.ml_dir, "pid.txt"),
            'cubic',
            "5202"
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
            f'{context.ml_dir}/test.py',
            f'-t', f'{self.__args.trace}',
            f'-n', f'{self.__args.nchoices}',
            f'-mN', f'{self.__args.model_name}',
            f'-m', 'bootstrapped_ucb',
            f"-x", f"{self.__args.ip}"
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
