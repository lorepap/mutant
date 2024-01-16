from agent.mab.base_mab_agent import BaseMabAgent
from copy import deepcopy
from sklearn.linear_model import SGDClassifier
from contextualbandits.online import _BasePolicy
from contextualbandits.online import AdaptiveGreedy


class AdaptiveGreedyThresholdAgent(BaseMabAgent):

    def __init__(self, nchoices: int, **kwargs) -> None:
        super(AdaptiveGreedyThresholdAgent, self).__init__(nchoices, **kwargs)

    def get_policy(self, nchoices: int) -> _BasePolicy:

        base_algorithm = SGDClassifier(
            random_state=123, loss='log', warm_start=False)

        return AdaptiveGreedy(deepcopy(base_algorithm), nchoices=nchoices, decay_type='threshold', batch_train=True)

    def get_tag(self) -> str:
        return "adaptive_greedy_threshold"