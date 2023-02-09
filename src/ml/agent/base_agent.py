from datetime import datetime
from typing import Any

import numpy as np
import tensorflow as tf
from contextualbandits.online import _BasePolicy
from helper import utils
from rl.core import Agent

class BaseAgent(Agent):

    def __init__(self, **kwargs):
        super(BaseAgent, self).__init__(**kwargs)

        self.now = utils.time_to_str()
        self.model_name = f'{self.get_tag()}.{self.now}'
        self.orig_name = f'{self.get_tag()}.{self.now}'

    def set_model_name(self, name: str) -> None:
        self.model_name = name

    def get_model_name(self) -> str:
        return self.model_name

    def get_orig_name(self) -> str:
        return self.orig_name

    def get_tag(self) -> str:
        """
            Returns the name of the model
        """

        raise NotImplementedError()

    def get_model(self) -> Any:

        raise NotImplementedError()

    def reset_name(self) -> None:
        self.model_name = self.orig_name

    def can_exploit(self) -> bool:
        raise NotImplementedError()

    def alter_x(self, x: np.ndarray) -> np.ndarray:
        raise NotImplementedError()
