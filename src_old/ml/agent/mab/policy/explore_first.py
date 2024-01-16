from agent.mab.base_mab_agent import BaseMabAgent
from copy import deepcopy
from sklearn.linear_model import SGDClassifier
from contextualbandits.online import _BasePolicy
from contextualbandits.online import ExploreFirst


class ExploreFirstAgent(BaseMabAgent):

    def __init__(self, nchoices: int, **kwargs) -> None:
        super(ExploreFirstAgent, self).__init__(nchoices, **kwargs)

    def get_policy(self, nchoices: int) -> _BasePolicy:

        base_algorithm = SGDClassifier(
            random_state=123, loss='log', warm_start=False)

        return ExploreFirst(deepcopy(base_algorithm), nchoices=nchoices, beta_prior=None, explore_rounds=1500, batch_train=True)

    def get_tag(self) -> str:
        return "explore_first"