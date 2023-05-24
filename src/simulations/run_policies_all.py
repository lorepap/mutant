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

TRAINING_FILENAME = os.path.join(context.ml_dir, "train.py")

def run_experiments(traces):
    ip = utils.get_private_ip()
    # read trace names and paths from YAML file
    models_config = utils.parse_models_config()

    for model in models_config["models"].keys():
        for i, t in enumerate(traces):
            print(f"Training {model} on {t}")

            if i > 0: # the same model will be retrained on multiple input traces
                retrain = 1
            else:
                retrain = 0

            # generate command to execute for this trace        
            command = f"python3 {TRAINING_FILENAME} -m {model} -t {t} -x {ip} -e 86400 -rt {retrain} --iperf_dir log/iperf/{args.nchoices}_arms"
            print("Executing", command)
            # execute each command and wait for it to finish
            try:
                subprocess.check_call(command, shell=True, stderr=sys.stderr, stdin=sys.stdin, stdout=sys.stdout, bufsize=1)
            
            except subprocess.CalledProcessError as e:
                print(f"Error running command '{command}': {e}")

    
if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-t', '--traces', nargs='+', help='List of traces to run')
    parser.add_argument('-n', '--nchoices', help='The number of arms (choices)')
    args = parser.parse_args()
    run_experiments(traces=args.traces)
    run_experiments()
