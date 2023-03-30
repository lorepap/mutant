import os
from experiment import MabExperiment

class ExpManager():
    def __init__(self, experiment, policy) -> None:
        self.experiment: MabExperiment = MabExperiment(policy=policy)

    def getMabTest(self, ):
        pass

    def getMabModelName(self) -> str:
        # TODO: multiple models? Get the most recent?
        expConfig = self.experiment.getExperimentConfig()
        return expConfig["models"]["name"]
    
    def getTestName(self) -> str:
        pass