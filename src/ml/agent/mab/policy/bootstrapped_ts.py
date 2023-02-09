from copy import deepcopy

import numpy as np
from agent.mab.base_mab_agent import BaseMabAgent
from contextualbandits.online import BootstrappedTS, _BasePolicy
from sklearn.linear_model import SGDClassifier


class BootstrappedTSAgent(BaseMabAgent):

    def __init__(self, nchoices: int, **kwargs) -> None:
        super(BootstrappedTSAgent, self).__init__(nchoices, **kwargs)

    def get_policy(self, nchoices: int) -> _BasePolicy:

        base_algorithm = SGDClassifier(
            random_state=123, loss='log', warm_start=False)

        beta_prior = ((3./nchoices, 4.), 2)
        
        return BootstrappedTS(deepcopy(base_algorithm), nchoices=nchoices, beta_prior=beta_prior, batch_train=True)

    def get_tag(self) -> str:
        return "bootstrapped_ts"

    
    def alter_x(self, x: np.ndarray) -> np.ndarray:
        return x.reshape(-1, x.shape[0])
