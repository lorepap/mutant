"""
Generate experiments to test all policies.
Traces located in traces/
Look at traces.yml to see available cellular traces

Example usage

python3 run_policies_all.py -t att.lte.driving

"""

import os
import yaml
import re
import sys
import subprocess
from argparse import ArgumentParser

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ml.helper import context, utils


SCRIPT_FILENAME = os.path.join(context.entry_dir, "tests", "policies_tests.sh")  # name of bash script to generate
TRAINING_FILENAME = os.path.join(context.ml_dir, "train.py")

def generate_experiments(trace):
    ip = utils.get_private_ip()
    # read trace names and paths from YAML file
    models_config = utils.parse_models_config()

    if not os.path.exists(SCRIPT_FILENAME):
        with open(SCRIPT_FILENAME, 'w') as f:
            f.write('#!/bin/bash\n')

    # generate bash script to execute experiments for each trace
    os.chmod(SCRIPT_FILENAME, 0o777)
    with open(SCRIPT_FILENAME, "w") as script_file:
        for model_name, model_info in models_config["models"].items():
            model_path = model_info["name"]
            # generate command to execute for this trace
            command = f"python3 {TRAINING_FILENAME} -t {trace} -m {model_path} -x {ip} -e 86400 -rt 0"
            # write command to script file
            script_file.write(command + "\n")
    
    
def run_experiments():
    # read commands from script file
    with open(SCRIPT_FILENAME, "r") as script_file:
        commands = script_file.read().splitlines()

    # execute each command and wait for it to finish
    for command in commands:
        subprocess.run(command, shell=True, check=True)
    
if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--trace", "-t", help="cellular trace for link simulation")
    args = parser.parse_args()
    generate_experiments(trace=args.trace)
    run_experiments()
