"""
Generate experiments to test all traces.
Traces located in traces/
Look at models.yml to see available models for MAB

Example usage

python3 run_traces_all.py -m active_explorer

"""

import os
import yaml
import re
import sys
import subprocess
from argparse import ArgumentParser

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ml.helper import context, utils

SCRIPT_FILENAME = os.path.join(context.entry_dir, "tests", "traces_tests.sh")  # name of bash script to generate
TRAINING_FILENAME = os.path.join(context.ml_dir, "train.py")

def generate_experiments(model):
    ip = utils.get_private_ip()
    
    
    # read trace names and paths from YAML file
    yaml_data = utils.parse_traces_config()

    # Select only mahimahi traces for training
    trace_names = ["att.lte.driving", "att.lte.driving.2016", "tm.lte.driving", "tm.lte.short", "tm.umts.driving", "vz.evdo.driving", "vz.lte.driving", "vz.lte.short"]
    trace_data = {name: data for name, data in yaml_data["traces"].items() if name in trace_names}


    # generate bash script to execute experiments for each trace
    os.chmod(SCRIPT_FILENAME, 0o777)

    with open(SCRIPT_FILENAME, "w") as script_file:

        for trace_name, trace_info in trace_data["traces"].items():

            trace_path = trace_name
            # generate command to execute for this trace
            command = f"python3 {TRAINING_FILENAME} -m {model} -t {trace_path} -x {ip} -e 86400 -rt 0"
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
    parser.add_argument("--model", "-m", help="MAB policy to train")
    parser.add_argument("--retrain", "-r", help="True: retrain from scratch")
    args = parser.parse_args()
    generate_experiments(model=args.model)
    run_experiments()
