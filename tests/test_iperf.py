import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.ml.helper import context
sys.path.append(context.ml_dir)
from argparse import ArgumentParser
from helper import utils
from helper.subprocess_wrappers import call, check_output
from helper.moderator import Moderator
from network.netlink_communicator import NetlinkCommunicator
from iperf.iperf_client import IperfClient
from iperf.iperf_server import IperfServer
from model.mahimahi_trace import MahimahiTrace
from runner.mab.policy.active_explorer import ActiveExplorerRunner
from helper.debug import set_debug, is_debug_on
import signal
import time

import os
import subprocess

ip = utils.get_private_ip()
t = 60
log_filename = "test.log"
moderator: Moderator = Moderator(True)
set_debug()
print("debug", is_debug_on())
trace = MahimahiTrace.fromString("att.lte.driving")
print("trace", trace)
client = IperfClient(trace, ip, t, log_filename, moderator)
# launch iperf3 server in a separate shell and redirect output to log file
server = IperfServer(log_file='server_test.txt')
server.start()

client.start()
print("Client started...........")

# Simulating processing.............
time.sleep(5)

# # Read the PID from the file
# pid_file = "pid.txt"
# with open(pid_file, 'r') as f:
#     pid = int(f.read().strip())
#     print("PID:", pid)

# Kill the client process
# os.kill(pid, signal.SIGTERM)
# print("Iperf client killed")
client.stop()
server.stop()
# Restart the server
# server.restart()

print("Testing another run")
client = IperfClient(MahimahiTrace.fromString("att.lte.driving"), 
                    ip, t, log_filename, moderator)
server.start()
client.start()
time.sleep(2)
client.stop()
server.stop()