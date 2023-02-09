#!/usr/bin/env python3

import os
import sys
import threading
from concurrent.futures import thread
import traceback

from helper import context, utils, moderator
from helper.subprocess_wrappers import Popen, call, check_output, print_output
from model.mahimahi_trace import MahimahiTrace


class IperfClient(threading.Thread):

    def __init__(self, trace: MahimahiTrace, ip: str, time: int, log_file: str, moderator: moderator.Moderator) -> None:
        threading.Thread.__init__(self)

        self.trace: MahimahiTrace = trace
        self.ip = ip
        self.time = time
        self.log_file = log_file
        self.moderator = moderator

    def ip_forwarding_set(self) -> bool:
        cmd = ['sysctl', 'net.ipv4.ip_forward']

        res = check_output(cmd)

        val = res.strip().decode('utf-8')

        return val == 'net.ipv4.ip_forward = 1'

    def set_ip_forwarding(self):

        if self.ip_forwarding_set():
            print('IP forwarding is already set\n')
            return

        cmd = ['sudo', 'sysctl', '-w', 'net.ipv4.ip_forward=1']
        res = call(cmd)

        if res != 0:
            raise Exception("Unable to set ipv4 forwarding")

    def get_mahimahi_cmd(self):

        cmd = ['mm-link']

        utils.check_dir(os.path.join(context.entry_dir, 'log/mahimahi'))

        uplink = os.path.join(context.entry_dir, 'log/mahimahi',
                              f'{self.trace}.{utils.time_to_str()}.up.log')
        downlink = os.path.join(
            context.entry_dir, 'log/mahimahi', f'{self.trace}.{utils.time_to_str()}.down.log')

        up_path, down_path = MahimahiTrace.path(self.trace)

        cmd = ['mm-link',
               up_path,
               down_path,
               f'--uplink-log={uplink}', f'--downlink-log={downlink}']

        return cmd

    def get_iperf_cmd(self):

        return [
            'python3',
            f'{context.ml_dir}/iperf.py',
            self.ip,
            str(self.time),
            self.log_file
        ]

    def run(self) -> None:
        try:

            self.set_ip_forwarding()

            cmd = self.get_mahimahi_cmd() + self.get_iperf_cmd()

            print("[DEBUG] Command executing:", cmd)

            if self.trace == MahimahiTrace.none:
                cmd = self.get_iperf_cmd()

            self.moderator.start()

            check_output(cmd)

            self.moderator.stop()

            print("mahimahi experiment ran successfully\n")

        except Exception as _:
            print('\n')

            print(traceback.format_exc())
            self.moderator.stop()
