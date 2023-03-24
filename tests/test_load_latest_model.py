import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ml.helper import context, utils
from src.ml.runner.mab.mab_runner import MabBaseRunner
from src.ml.runner.mab.policy.adaptive_greedy_threshold import AdaptiveGreedyThresholdRunner
from src.ml.helper.utils import parse_training_config
from src.ml.helper.moderator import Moderator
from src.ml.network.netlink_communicator import NetlinkCommunicator

class RunnerTest():

    def __init__(self,):
        self.train_config: dict = parse_training_config()
    
    def test_load_latest_model(self):
        num_features = int(self.train_config['num_features'])
        # Time in seconds for switching protocol
        window_len = int(self.train_config['window_len'])
        # Number of jiffies for switching protocol
        jiffies_per_state = int(self.train_config['jiffies_per_state'])
        # Number of network statistics
        num_fields_kernel = int(self.train_config['num_fields_kernel'])
        # Number of steps per episode
        steps_per_episode = self.train_config['steps_per_episode']
        # Delta factor for reward function
        delta = float(self.train_config['delta'])
        # Learning rate for the optimized
        lr = float(self.train_config['lr'])
        # Time to wait for next 
        step_wait_seconds = float(self.train_config['step_wait_seconds'])

        runner = AdaptiveGreedyThresholdRunner(4, lr, num_features, window_len, 
                num_fields_kernel, jiffies_per_state, steps_per_episode, 
                delta, step_wait_seconds, NetlinkCommunicator(), moderator=Moderator(True), trace="att.lte.driving")
        
        # Model loaded
        model = runner.get_model().get_model_name()
        model_config = runner.get_model_config()

        print("\nModel:", model,"\n")
        print("Model config", model_config,"\n")

if __name__ == "__main__":
    tester = RunnerTest()
    tester.test_load_latest_model()
    print("Done.")