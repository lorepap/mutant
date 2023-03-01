from argparse import ArgumentParser
from helper import context, utils
from helper.subprocess_wrappers import call, check_output
from helper.moderator import Moderator
from network.netlink_communicator import NetlinkCommunicator
from runner.iperf_client import IperfClient
from model.mahimahi_trace import MahimahiTrace
from runner.mab.policy.active_explorer import ActiveExplorerRunner

import os
import subprocess

def main():
    # -- Input arguments --

    ## From command
    parser = ArgumentParser(
        description='by default, run python3 ml/new_train_simple.py')

    parser.add_argument('--model', '-m', help='Model to train', default='active_explorer')

    parser.add_argument('--retrain', '-rt', type=int,
                        help='--retrain: Flag (0:false, 1:true) to retrain latest model or not', default=1)

    parser.add_argument('--trace', '-t', type=str,
                        help='--trace: Name of mahimahi trace file used', default="none")

    parser.add_argument('--ip', '-x', type=str,
                        help='--ip: IP of iperf server machine', default=None)

    parser.add_argument('--time', '-e', type=int,
                        help='--time: Number of seconds to run iperf', default=86400)

    parser.add_argument('--iperf', '-u', type=int,
                        help='--iperf: Flag (0:false, 1:true) to indicate whether to use iperf or not', default=1)

    parser.add_argument('--iperf_dir', '-d', type=str,
                        help='--iperf_dir: iperf directory to use', default="log/iperf")

    parser.add_argument('--trace_dir', '-f', type=str,
                        help='--trace_dir: trace directory to use', default="log/prod")

    parser.add_argument('--runs', '-r', type=int,
                        help='--runs: Number of times to run', default=1)
    
    args = parser.parse_args()

    if args.ip == None :
        args.ip = utils.get_private_ip()
        print("\nwill connect to", args.ip,"\n")

    ## From config
    train_config: dict = utils.parse_training_config()
    train_episodes = int(train_config['train_episodes'])
    test_episodes = int(train_config['test_episodes'])
    steps_per_episodes = int(train_config['steps_per_episode'])

    # -- Initialization --
    
    ## Initialize kernel (plug mimic module in)
    res = check_output(['cat', '/proc/sys/net/ipv4/tcp_congestion_control'])
    protocol = res.strip().decode('utf-8')
    if (protocol != "mimic"):
        cmd = os.path.join(context.entry_dir, 'scripts/init_kernel.sh')
        res = call(['chmod', '755', cmd])
        res = call(cmd)
        if res != 0:
            raise Exception('Unable to init kernel\n')
    
    ## Initialize kernel communication
    netlink_communicator = NetlinkCommunicator()
    msg = netlink_communicator.create_netlink_msg(
            'INIT_COMMUNICATION', msg_flags=netlink_communicator.INIT_COMM_FLAG)

    netlink_communicator.send_msg(msg)

    print("Communication initiated")

    nchoices, nprotocols = utils.get_number_of_actions(netlink_communicator)

    print(f'\n\n----- Number of protocols available is {nchoices} ----- \n\n')

    # -- Running Model -- 

    model = args.model

    ## Initialize runner
    
    num_features = int(train_config['num_features'])
    ### Time in seconds for switching protocol
    window_len = int(train_config['window_len'])
    ### Number of jiffies for switching protocol
    jiffies_per_state = int(train_config['jiffies_per_state'])
    ### Number of network statistics
    num_fields_kernel = int(train_config['num_fields_kernel'])
    ### Number of steps per episode
    steps_per_episode = int(train_config['steps_per_episode'])
    ### Delta factor for reward function
    delta = float(train_config['delta'])
    ### Learning rate for the optimized
    lr = float(train_config['lr'])
    ### Step episode time
    step_wait_seconds = float(train_config['step_wait_seconds'])
    ### Train from scratch or train from a pre-existing model
    reset_model = args.retrain != 1
    
    ## Set and start the thread client
    moderator: Moderator = Moderator(args.iperf == 1)
    base_path = os.path.join(context.entry_dir, args.iperf_dir)
    tag = f"{args.trace}.{model}"
    filename = f'{tag}.{utils.time_to_str()}.json'
    log_filename = f'{base_path}/{filename}'
    client = IperfClient(MahimahiTrace.fromString(args.trace), 
                         args.ip, args.time, log_filename, moderator)
    client.start()


    ## Let's try one policy
    runner: ActiveExplorerRunner = ActiveExplorerRunner(nchoices, lr,
                                    num_features, window_len, num_fields_kernel, jiffies_per_state, 
                                    steps_per_episode, delta, step_wait_seconds, netlink_communicator, moderator)

    ## Run the model
    ### NOTE: if runner (model) is reset, previous timestamp is change to current
    history = runner.train(train_episodes*steps_per_episode, reset_model)

    print("Training finished")

    ## Save model
    runner.save_history(history)
    print(f'saved training history for model: {model}')
    runner.save_model(reset_model)

    print(f'running test for model: {model}')

    runner.test(test_episodes, args.trace)

    # Stop client
    client.stop()
    
    runner.close()
    


if __name__ == '__main__':
    main()
    os._exit(1)