from argparse import ArgumentParser
from collection.collector import Collector


def run(args):

    # Collection process
    runner = Collector(protocol=args.proto, running_time=args.time)
    # Setup connection with the kernel and setup client-server communication (iperf + mahimahi)
    runner.setup_communication()
    
    # Collect data
    runner.run_collection()
    # Stop communication
    runner.stop_communication()


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("--proto", type=str, default="cubic", help="Protocol to run for data collection")
    parser.add_argument("--time", type=float, default=10, help="Experiment running time (s)")
    args = parser.parse_args()
    run(args)