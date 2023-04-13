from copy import deepcopy

import numpy as np
from src.ml.agent.mab.base_random_agent import BaseRandomAgent
from sklearn.linear_model import SGDClassifier


class RandomAgent(BaseRandomAgent):

    def __init__(self, nchoices: int, **kwargs) -> None:
        super(RandomAgent, self).__init__(nchoices, **kwargs)

    def get_policy(self, nchoices: int):
        pass

    def get_tag(self) -> str:
        return "random_policy"
    
    def alter_x(self, x: np.ndarray) -> np.ndarray:
        return x.reshape(-1, x.shape[0])
