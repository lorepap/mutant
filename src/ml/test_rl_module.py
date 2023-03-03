"""
We need to test how the protocol is being selected and changed each time.
Protocol choice is made in the environment (MAB environment).
"""
import os
from helper import context
from helper import utils
from agent.mab.base_mab_agent import BaseAgent
from agent.mab.policy.active_explorer import ActiveExplorerAgent
from agent.mab.policy.adaptive_greedy_threshold import AdaptiveGreedyThresholdAgent
from environment.mab.mab_environment import MabEnvironment
from network.netlink_communicator import NetlinkCommunicator
from helper.moderator import Moderator
from iperf.iperf_client import IperfClient
from iperf.iperf_server import IperfServer
from model.mahimahi_trace import MahimahiTrace
from keras.optimizers import Adam
from helper.subprocess_wrappers import check_output, call

def is_kernel_initialized() -> bool:
        cmd = ['cat', '/proc/sys/net/ipv4/tcp_congestion_control']

        res = check_output(cmd)

        protocol = res.strip().decode('utf-8')

        return protocol == 'mimic'

def init_kernel():

    if is_kernel_initialized():
        print('Kernel has already been initialized\n')
        return

    cmd = os.path.join(context.entry_dir, 'scripts/init_kernel.sh')

    # make script runnable
    res = call(['chmod', '755', cmd])
    if res != 0:
        raise Exception('Unable to set run permission\n')

    res = call(cmd)
    if res != 0:
        raise Exception('Unable to init kernel\n')


# Training params
train_config: dict = utils.parse_training_config()

train_episodes = int(train_config['train_episodes'])
num_features = int(train_config['num_features'])
window_len = int(train_config['window_len'])
jiffies_per_state = int(train_config['jiffies_per_state'])
num_fields_kernel = int(train_config['num_fields_kernel'])
steps_per_episode = int(train_config['steps_per_episode'])
delta = float(train_config['delta'])
lr = float(train_config['lr'])
step_wait_seconds = float(train_config['step_wait_seconds'])
nchoices = 3

# Simulation params
trace = 'att.lte.driving'
ip = utils.get_private_ip()
time = 86400
log_file = "/home/lorenzo/Desktop/research-projects/mimic-2/log/test/iperf_test.log"

# Setup kernel and insert mimic module
init_kernel()

# Initialize user-kernel communication
moderator = Moderator(True)
netlink_communicator = NetlinkCommunicator()

msg = netlink_communicator.create_netlink_msg(
        'INIT_COMMUNICATION', msg_flags=netlink_communicator.INIT_COMM_FLAG)

netlink_communicator.send_msg(msg)

print("Communication initiated")

nchoices, nprotocols = utils.get_number_of_actions(
            netlink_communicator)


# Initialize objects under test
model = AdaptiveGreedyThresholdAgent(nchoices)
environment = MabEnvironment(
    num_features, 
    window_len, 
    num_fields_kernel, 
    jiffies_per_state,
    nchoices, 
    steps_per_episode, 
    delta, 
    step_wait_seconds, 
    netlink_communicator, 
    moderator
)
environment.enable_log_traces()

# Initialize client and server comm
client = IperfClient(MahimahiTrace.fromString(
            trace), ip, time, log_file, moderator)
server = IperfServer()

# Start communication
server.start()
client.start()

# Training the model (Here we need to test the agent module)
optimizer = Adam(lr)
model.compile(optimizer, metrics=['mae'])
train_res = model.fit(environment, nb_steps=train_episodes*steps_per_episode,
                                        visualize=True, verbose=2)

client.stop()
server.stop()