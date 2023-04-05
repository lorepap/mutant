"""
Generate experiments to train MahiMahi traces.
Traces located in traces/
Look at models.yml to see available models for MAB

Example usage

python3 run_mahimahi_traces.py -m active_explorer -r

"""

import os
import yaml
import re
import sys
import subprocess
from argparse import ArgumentParser

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ml.helper import context, utils
from ml.helper.debug import set_debug

TRAINING_FILENAME = os.path.join(context.ml_dir, "train.py")

def run_experiments(args):
    ip = utils.get_private_ip()
    
    # read trace names and paths from YAML file
    yaml_data = utils.parse_traces_config()

    # Select only mahimahi traces for training
    trace_names = ["att.lte.driving", "att.lte.driving.2016", "tm.lte.driving", "tm.lte.short", "tm.umts.driving", "vz.evdo.driving", "vz.lte.driving", "vz.lte.short"]
    trace_data = {name: data for name, data in yaml_data["traces"].items() if name in trace_names}

    for model in args.models:
        for i, trace_name in enumerate(trace_data.keys()):

            trace_path = trace_name
            print(trace_path)
            # Train from scratch on the first trace, then retrain the same model over the others
            if args.retrain:
                retrain = 1 if i > 0 else 0
                print("Training from scratch over the first trace...")
            else:
                retrain = 1
            # generate command to execute for this trace
           
            command = f"python3 {TRAINING_FILENAME} -m {model} -t {trace_path} -x {ip} -e 86400 -rt {retrain}"
            print("Executing", command)
            # execute each command and wait for it to finish
            try:
                subprocess.check_call(command, shell=True, stderr=sys.stderr, stdin=sys.stdin, stdout=sys.stdout, bufsize=1)
            
            except subprocess.CalledProcessError as e:
                print(f"Error running command '{command}': {e}")
    
    
if __name__ == "__main__":
    parser = ArgumentParser()
    # parser.add_argument("--model", "-m", help="MAB policy to train")
    parser.add_argument('-m', '--models', nargs='+', help='List of models to run')
    parser.add_argument("--retrain", "-r", action="store_true", help="True: retrain from scratch")
    args = parser.parse_args()
    run_experiments(args)
