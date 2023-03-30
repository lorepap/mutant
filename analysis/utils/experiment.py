import os
from misc import read_json_file

class MabExperiment():
    def __init__(self, policy) -> None:
        # self.tool = tool
        self.policy = policy
        self.expName = self.policy + '.json'
        self.config_dir_path = os.path.join('mab', 'config')
        self.timestamp = None


    def getExperimentConfig(self):
        return read_json_file(os.path.join(self.config_dir_path, self.expName))
    
 