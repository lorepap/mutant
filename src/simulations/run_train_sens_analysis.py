"""
Sensitivity analysis on parameters in train.yml
This module has been thought to run experiments varying the step_wait time during which
Mimic keeps executing the same protocol and received statistics from the kernel module.
Current value is 0.5.

Research questions:
What is the model behavior when a protocol runs for >1 s? 
What if it runs for a very small amount of time?

This is a modified version of run_train.py python file

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
TRAIN_CONFIG_FILENAME = os.path.join("config", "train.yml")

def run_experiments(args):
    ip = utils.get_private_ip()
    print("Server IP:", ip)
    # read trace names and paths from YAML file
    yaml_data = utils.parse_traces_config()
    # execute the command for each value of "steps_wait_seconds"
    for model in args.models:
        for step_wait_seconds in [0.01, 0.1, 1, 5]:
            for i, trace in enumerate(args.traces):
                print(f"Training {model} on {trace}")

                if args.retrain or i > 0:
                    print("Retraining on", trace)
                    retrain = 1
                else:
                    print("New model about to train on", trace)
                    retrain = 0

                base_step_wait = 0.5
                base_step_per_episode = 500

                # Update "steps_wait_seconds" value in the "train.yml" config file
                with open(TRAIN_CONFIG_FILENAME, 'r') as f:
                    train_config = yaml.load(f, Loader=yaml.FullLoader)
                train_config["step_wait_seconds"] = step_wait_seconds
                # Adjust the training time accordingly setting the steps per episode
                train_config["steps_per_episode"] = base_step_wait/step_wait_seconds * base_step_per_episode
                with open(TRAIN_CONFIG_FILENAME, 'w') as f:
                    yaml.dump(train_config, f)

                # generate command to execute for this trace        
                command = f"python3 {TRAINING_FILENAME} -m {model} -t {trace} -x {ip} -e 86400 -rt {retrain} -rw {args.reward}"
                print("Executing", command)
                # execute each command and wait for it to finish
                try:
                    subprocess.check_call(command, shell=True, stderr=sys.stderr, stdin=sys.stdin, stdout=sys.stdout, bufsize=1)
                
                except subprocess.CalledProcessError as e:
                    print(f"Error running command '{command}': {e}")

    
if __name__ == "__main__":
    parser = ArgumentParser()
    # parser.add_argument("--model", "-m", help="MAB policy to train")
    parser.add_argument('-m', '--models', nargs='+', help='List of models to run', default='bootstrapped_ucb')
    parser.add_argument('-t', '--traces', nargs='+', help='List of traces to run', default='att.lte.driving')
    parser.add_argument('-rw', '--reward', help='The reward type for the RL module', default='owl')
    parser.add_argument("--retrain", "-r", action="store_true", help="True: retrain the latest trained model otherwise train a new model from scratch")
    args = parser.parse_args()
    run_experiments(args)


