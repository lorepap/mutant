import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.ml.helper import context
sys.path.append(context.ml_dir)
from argparse import ArgumentParser
from src.ml.helper import utils
from src.ml.helper.subprocess_wrappers import call, check_output
from src.ml.helper.moderator import Moderator
from src.ml.network.netlink_communicator import NetlinkCommunicator
from src.ml.iperf.iperf_client import IperfClient
from src.ml.iperf.iperf_server import IperfServer
from src.ml.model.mahimahi_trace import MahimahiTrace
from src.ml.runner.mab.policy.active_explorer import ActiveExplorerRunner
from src.ml.helper.debug import set_debug, is_debug_on
import signal
import time

import os


if __name__ == "__main__":
    ip = utils.get_private_ip()
    t = 60
    log_filename = "test.log"
    moderator: Moderator = Moderator(True)
    set_debug()
    print("debug", is_debug_on())
    trace = MahimahiTrace.fromString("att.lte.driving")
    # up_path, down_path = MahimahiTrace.path(trace)
    print("trace", trace)
    client = IperfClient(trace, 
                        ip, t, log_filename, moderator, pid_file='pid_test.txt')

    client.start()

    print(" ")