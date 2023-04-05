"""
Test model on cellular traces.
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

TEST_FILENAME = os.path.join(context.ml_dir, "test.py")

def run_experiments(items):
    ip = utils.get_private_ip()
    # read trace names and paths from YAML file
    trace_data = utils.parse_traces_config()

    # generate bash script to execute experiments for each trace
    for i, trace_name in enumerate(trace_data["traces"].keys()):

        # generate command to execute for this trace
        command = f"python3 {TEST_FILENAME} -m {items.model} -t {trace_name} -x {ip} -e {items.iperf_duration}"
        
        subprocess.call(command, shell=True, stderr=sys.stderr)
        # except subprocess.CalledProcessError as e:
        #     print(f"Error running command '{command}': {e}")
        #     raise e

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--model", "-m", help="MAB policy to train")
    parser.add_argument("--iperf_duration", "-id", help="Experiment duration", default=60)
    args = parser.parse_args()
    run_experiments(items=args)
