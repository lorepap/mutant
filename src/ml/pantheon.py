import os
import sys
import traceback
from typing import Any

from helper import arg_parser, context, subprocess_wrappers, utils
from model.mahimahi_trace import MahimahiTrace


class PantheonRunner():

    def __init__(self, args: Any) -> None:
        self.__args = args

    def run(self):
     for t in self.__args.trace:
        try:
            now = utils.time_to_str()

            test_py = utils.get_fullpath('pantheon/src/experiments/test.py')
            analysis_py = utils.get_fullpath(
                'pantheon/src/analysis/analyze.py')

            utils.check_dir(os.path.join(context.entry_dir,
                            'log/pantheon', t))

            # Add to sys
            sys.path.append(os.path.abspath(os.path.join(os.path.dirname(test_py), os.pardir)))

            self.__log_path = os.path.join(
                context.entry_dir,
                'log/pantheon',
                t,
                now
            )

            utils.check_dir(self.__log_path)

            up_trace, down_trace = MahimahiTrace.fromString(
                t).path()

            all_cmd = None

            if self.__args.all:
                all_cmd = ['--all']
            else:
                all_cmd = ['--schemes'] + [p for p in self.__args.protocols.split()]

            test_cmd = [
                test_py,
                'local'
            ] + all_cmd + [
                f'-f={self.__args.runs}',
                f'--data-dir={self.__log_path}',
                f'--uplink-trace={up_trace}',
                f'--downlink-trace={down_trace}',
            ]

            analyze_cmd = [
                analysis_py,
                f'--data-dir={self.__log_path}'
            ]

            print(f'Running: {" ".join(test_cmd)}\n\n')
            subprocess_wrappers.check_output(test_cmd)

            print(f'Running: {" ".join(analyze_cmd)}')
            subprocess_wrappers.check_output(analyze_cmd)

        except Exception as _:
            print('\n')
            print(traceback.format_exc())
            os.rmdir(self.__log_path)


def main():
    args = arg_parser.parse_pantheon_setup()

    pr = PantheonRunner(args)
    pr.run()

if __name__ == '__main__':
    main()
    os._exit(1)
