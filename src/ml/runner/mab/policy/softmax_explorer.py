from network.netlink_communicator import NetlinkCommunicator
from runner.mab.mab_runner import MabBaseRunner
from agent.mab.policy.softmax_explorer import SoftmaxExplorerAgent
from typing import Any
import traceback
from helper.moderator import Moderator


class SoftmaxExplorerRunner(MabBaseRunner):

    def __init__(self, nchoices: int, lr: int, num_features: int,
                 window_len: int, num_fields_kernel: int, jiffies_per_state: int,
                 steps_per_episode: int, delta: float, step_wait_seconds: float,
                 comm: NetlinkCommunicator, moderator: Moderator, **kwargs) -> None:

        super(SoftmaxExplorerRunner, self).__init__(nchoices, lr, num_features, window_len,
                                                    num_fields_kernel, jiffies_per_state,
                                                    steps_per_episode, delta, step_wait_seconds, comm,
                                                    moderator)

        self.kwargs = kwargs

    def load_basic(self) -> Any:
        try:

            model = SoftmaxExplorerAgent(self.nchoices, moderator=self.moderator)
            model.compile(self.get_optimizer(), metrics=['mae'])
            return model

        except Exception as error:
            print(traceback.format_exc())
            return None

    def get_tag(self) -> str:
        return "softmax_explorer"
