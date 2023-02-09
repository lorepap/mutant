#!/usr/bin/env python3

from ast import arg
import sys
import time
import traceback
from helper.subprocess_wrappers import call, check_output


class IperfRunner():

    def __init__(self, ip: str, time: int, log: str, scheme: str) -> None:
        self.ip = ip
        self.time = time
        self.log = log
        self.scheme = scheme

    def run(self) -> None:

        trials = 1

        ss_cmd = ['iperf3']

        if self.scheme != None and self.scheme.strip() != '':
            ss_cmd = ['iperf3', '-C', str(self.scheme)]

        while trials <= 5:
            try:
                cmd = [
                    '-c',
                    self.ip,
                    '-p',
                    '5201',
                    '-t',
                    str(self.time),
                    '-J',
                    '--logfile',
                    self.log
                ]

                cmd = ss_cmd + cmd

                check_output(cmd)

                sys.stderr.write("iperf completed successfully\n")

                break
            except Exception as _:
                sys.stderr.write(traceback.format_exc())
                sys.stderr.write(
                    f'Trails #{trials}: Server is still busy, trying again after a second\n')
                time.sleep(10)
                trials += 1


def main():
    scheme = None if len(sys.argv) == 4 else sys.argv[4]
    runner = IperfRunner(sys.argv[1], str(sys.argv[2]), sys.argv[3], scheme)
    runner.run()


if __name__ == '__main__':
    main()
