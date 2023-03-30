"""
Collect trace for native protocols (i.e., Cubic, Bbr, Hybla, etc.).
"""

import os
import yaml
import re
import sys
import subprocess
from argparse import ArgumentParser

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ml.helper import context
from ml.helper import utils

SCRIPT_FILENAME = os.path.join(context.ml_dir, "native.py")

def run_experiments(items):
    ip = utils.get_private_ip()
    # read trace names and paths from YAML file
    trace_data = utils.parse_traces_config()

    # Loop over the traces
    for i, trace_name in enumerate(trace_data["traces"].keys()):
        
        
        if items.debug:
            command = f'python3 {SCRIPT_FILENAME} -p {items.protocol} -tr {trace_name} -id {items.iperf_duration} -debug'
        else:
            command = f'python3 {SCRIPT_FILENAME} -p {items.protocol} -tr {trace_name} -id {items.iperf_duration}'

        subprocess.call(command, shell=True, stderr=sys.stderr)
        
        # except subprocess.CalledProcessError as e:
        #     print(f"Error running command '{command}': {e}")
        #     raise e

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--protocol", "-p", help="Linux native CCA to test")
    parser.add_argument("--iperf_duration", "-id", help="Duration of the iperf simulation", default="60")
    parser.add_argument("--debug", "-d", action="store_true", help="Debug mode")
    args = parser.parse_args()
    run_experiments(items=args)
