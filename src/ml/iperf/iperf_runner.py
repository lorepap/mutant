#!/usr/bin/env python3

import os
import subprocess

from helper import context, utils
from helper.subprocess_wrappers import print_output

class IperfRunner():

    def __init__(self, ip: str, time: int, log: str) -> None:
        self.ip = ip
        self.time = time
        self.log = log

    def run(self) -> None:

        cmd = [
            'iperf3',
            '-c',
            self.ip,
            '-t',
            str(self.time),
            '-J',
            self.log
        ]

        ps = None

        with open(self.log, 'w+') as file:
            ps = subprocess.Popen(cmd, preexec_fn=os.setsid,
                                  stdin=subprocess.PIPE, stdout=file)
            res = ps.wait()

        if res != 0:
            raise Exception("iperf ran into an exception")
