from concurrent.futures import ThreadPoolExecutor
import subprocess
import threading
import sys
import os
from argparse import ArgumentParser
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ml.helper import context
from ml.helper import utils
from ml.iperf.iperf_server import IperfServer
from ml.model.mahimahi_trace import MahimahiTrace

def get_mahimahi_cmd():

        cmd = ['mm-link']

        utils.check_dir(os.path.join(context.entry_dir, 'log/mahimahi'))

        uplink = os.path.join(context.entry_dir, 'log/mahimahi',
                              f'{args.trace}.{utils.time_to_str()}.up.log')
        downlink = os.path.join(
            context.entry_dir, 'log/mahimahi', f'{args.trace}.{utils.time_to_str()}.down.log')

        up_path, down_path = MahimahiTrace.fromString(args.trace).path()

        cmd = ['mm-link',
               up_path,
               down_path,
               f'--uplink-log={uplink}', f'--downlink-log={downlink}']

        return cmd

def run_command(cmd):
    subprocess.run(cmd, check=True)

def main(args):
    prot = args.prot
    ip = utils.get_private_ip()
    now = utils.time_to_str()
    tag = 'solo' if args.solo else 'against'
    log_path = os.path.join(
            context.entry_dir,
            'log/iperf/harm',
            f'{args.trace}.{prot}.{tag}.{now}.json'
        )
    
    # Start server for single protcol running
    base_path = os.path.join(context.entry_dir, "log", "iperf", "server")
    filename = f'server_harm_test.log'
    log_filename = f'{base_path}/{filename}'
    os.makedirs(os.path.dirname(log_filename), exist_ok=True)
    server = IperfServer(log_filename, port=5202)
    server.start()
    
    # Define the commands to run
    cmd1 = ['python3', f'{context.ml_dir}/test.py', f'-t', f'{args.trace}',
            f'-n', f'{args.nchoices}', f'-mN', f'{args.model_name}',
            f'-m', 'bootstrapped_ucb', f'-x', f'{ip}', "-e", "60",
            "-d", f"log/iperf/harm"]

    iperf_cmd = ['python3', f'{context.ml_dir}/iperf.py', f'{ip}', '60',
            log_path, os.path.join(context.ml_dir, "pid.txt"), '5202', prot]
    
    cmd2 = get_mahimahi_cmd() + iperf_cmd

    if MahimahiTrace.fromString(args.trace) == MahimahiTrace.none:
        cmd2 = iperf_cmd


    # Create thread objects for each command
    if args.against:
        thread1 = threading.Thread(target=run_command, args=(cmd1,))
    thread2 = threading.Thread(target=run_command, args=(cmd2,))

    # # Start both threads
    # thread1.start()
    # thread2.start()

    # # Wait for both threads to finish
    # thread1.join()
    # thread2.join()

    # Create a ThreadPoolExecutor with a maximum of 2 threads
    executor = ThreadPoolExecutor(max_workers=2)

    # Submit the commands to the executor for parallel execution
    if args.against:
        future1 = executor.submit(run_command, cmd1)
    future2 = executor.submit(run_command, cmd2)

    # Wait for both futures to complete
    executor.shutdown(wait=True)

    # Code here will continue executing after both threads have finished

if __name__=="__main__":
    argparser = ArgumentParser()
    argparser.add_argument('--solo', action='store_true', help='Run only Linux protocol')
    argparser.add_argument('--against', action='store_true', help='Run Linux protocol against Mutant')
    argparser.add_argument("--trace", default="att.lte.driving.2016")
    argparser.add_argument("--model_name", default="bootstrapped_ucb.2023.04.19.09.08.39")
    argparser.add_argument("--model", default="bootstrapped_ucb")
    argparser.add_argument("--nchoices", default=3)
    argparser.add_argument("--prot", default="cubic")
    args = argparser.parse_args()
    main(args)
    os._exit(0)