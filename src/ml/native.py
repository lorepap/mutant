from argparse import ArgumentParser
from helper.debug import set_debug, is_debug_on, change_name
from subprocess import call
from iperf.iperf_client import IperfClient
from iperf.iperf_server import IperfServer
from helper import context, utils
from helper.moderator import Moderator
from model.mahimahi_trace import MahimahiTrace
import time
import os


class NativeRunner():
    def __init__(self, args) -> None:
        self.args = args
        self.moderator = Moderator(use_iperf=1)

    def set_native_protocol(self):
        cmd = f"sudo sysctl net.ipv4.tcp_congestion_control={self.args.protocol}"
        res = call(cmd, shell=True)
        if res != 0:
            raise Exception('Unable to set native protocol\n')
        
    def start_server(self, tag):
        base_path = os.path.join(context.entry_dir, "log", "iperf", "server")
        filename = f'server.log'
        if is_debug_on():
            filename = change_name(filename)
        log_filename = f'{base_path}/{filename}'
        self.server = IperfServer(log_filename)
        self.server.start()

    # Initialize an IperfClient object for the experiment with an input mahimahi trace (from args)
    def start_client(self, tag: str, pid_file: str = None) -> str:

        base_path = os.path.join(context.entry_dir, self.args.iperf_dir)
        utils.check_dir(base_path)

        filename = f'{tag}.{utils.time_to_str()}.json'
   
        if is_debug_on():
            filename = change_name(filename)
     
        log_filename = f'{base_path}/{filename}'
     
        self.client = IperfClient(MahimahiTrace.fromString(
            self.args.trace), self.args.ip, self.args.iperf_duration, log_filename, self.moderator)

        self.client.start()
        return log_filename


    def start_communication(self, tag):
        self.start_server(tag)
        self.start_client(tag)

    def stop_communication(self):
        # self.client.stop()
        self.server.stop()

    def run(self) -> None:
        if self.args.debug:
            set_debug()

        self.start_communication(tag=f'{self.args.protocol}.{self.args.trace}')
        
        while self.moderator.is_stopped():
            time.sleep(1)
        
        while not self.moderator.is_stopped():
            time.sleep(1)

        self.stop_communication()
        exit()


if __name__ == '__main__':
    parser = ArgumentParser()
    
    parser.add_argument('--protocol', '-p', type=str, default=None)

    parser.add_argument('--iperf_duration', '-id', type=int, default=60)

    parser.add_argument('--trace', '-tr', type=str,
                        help='--trace: Name of trace used', default="none")
    
    parser.add_argument('--debug', '-debug', action='store_true')

    parser.add_argument('--iperf_dir', '-d', type=str,
                        help='--iperf_dir: iperf directory to use', default="log/iperf")
    
    parser.add_argument('--ip', '-x', type=str,
                        help='--ip: IP of iperf server machine', default="10.0.2.15")


    args = parser.parse_args() 
    runner = NativeRunner(args)
    runner.run()
