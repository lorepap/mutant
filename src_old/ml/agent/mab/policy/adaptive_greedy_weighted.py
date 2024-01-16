from agent.mab.base_mab_agent import BaseMabAgent
from copy import deepcopy
from sklearn.linear_model import SGDClassifier
from contextualbandits.online import _BasePolicy
from contextualbandits.online import AdaptiveGreedy


class AdaptiveGreedyWeightedAgent(BaseMabAgent):

    def __init__(self, nchoices: int, **kwargs) -> None:
        super(AdaptiveGreedyWeightedAgent, self).__init__(nchoices, **kwargs)

    def get_policy(self, nchoices: int) -> _BasePolicy:

        base_algorithm = SGDClassifier(
            random_state=123, loss='log', warm_start=False)

        beta_prior = ((3./nchoices, 4.), 2)

        return AdaptiveGreedy(deepcopy(base_algorithm), nchoices=nchoices, beta_prior=beta_prior, active_choice='weighted', decay_type='percentile', decay=0.9997, batch_train=True)

    def get_tag(self) -> str:
        return "adaptive_greedy_weighted"