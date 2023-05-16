"""
Generate experiments to train MahiMahi traces.
Traces located in traces/
Look at models.yml to see available models for MAB

Example usage

python3 run_mahimahi_traces.py -m active_explorer -t att.lte.driving -r

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
    print("Server IP:", ip)
    # read trace names and paths from YAML file
    yaml_data = utils.parse_traces_config()

    for model in args.models:
        for trace in args.traces:
            print(f"Training {model} on {trace}")

            if args.retrain:
                retrain = 1
            else:
                retrain = 0

            # generate command to execute for this trace        
            command = f"python3 {TRAINING_FILENAME} -m {model} -t {trace} -x {ip} -e 86400 -rt {retrain} -rw {args.reward} --iperf_dir log/iperf/{args.nchoices}_arms"
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
    parser.add_argument('-t', '--traces', nargs='+', help='List of traces to run')
    parser.add_argument('-rw', '--reward', help='The reward type for the RL module', default='orca')
    parser.add_argument('-n', '--nchoices', help='The number of arms (choices)')
    parser.add_argument("--retrain", "-r", action="store_true", help="True: retrain the latest trained model otherwise train a new model from scratch")
    args = parser.parse_args()
    run_experiments(args)
