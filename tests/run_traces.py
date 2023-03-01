import os
import yaml
import subprocess

TRACE_FILENAME = "config/traces.yml"  # name of YAML file containing trace paths and names
SCRIPT_FILENAME = "tests/traces_tests.sh"  # name of bash script to generate

def generate_experiments():
    # read trace names and paths from YAML file
    with open(TRACE_FILENAME, "r") as trace_file:
        trace_data = yaml.safe_load(trace_file)

    # generate bash script to execute experiments for each trace
    with open(SCRIPT_FILENAME, "w") as script_file:
        for trace_name, trace_info in trace_data["traces"].items():
            trace_path = trace_info["name"]
            # generate command to execute for this trace
            command = f"python src/ml/new_train_simple.py -t {trace_path} -x 10.120.8.116 -t 86400"
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
    generate_experiments()
    run_experiments()
