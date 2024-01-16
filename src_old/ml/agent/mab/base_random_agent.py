
from typing import Any

import dill as pickle
import numpy as np
from agent.base_agent import BaseAgent
from contextualbandits.online import _BasePolicy


class BaseRandomAgent(BaseAgent):

    def __init__(self, nchoices: int, **kwargs) -> None:
        super(BaseRandomAgent, self).__init__(**kwargs)

        self.counter = 0
        self.prev_action = 0
        self.nchoices = nchoices
        self.compiled = True


    def get_model(self) -> _BasePolicy:
        return self.model

    def reset_states(self) -> None:
        self.recent_action = None
        self.recent_observation = None

    def compile(self, optimizer, metrics=[]) -> None:
        self.compiled = True

    def forward(self, observation) -> np.ndarray:

        if observation['obs'].shape[0] == 0:
            print('Observation is empty. Cannot predict')
            return self.prev_action

        # Select an action.
        actions = np.random.randint(low=0, high=self.nchoices, size=observation['obs'].shape[0], dtype='uint8')        # print("[DEBUG] actions: ", actions)
        N = len(actions)
        # print("[DEBUG] length actions:", N)

        # print(f'Observation: {observation["obs"].shape}')

        # Book-keeping.
        self.recent_observation = observation
        self.recent_action = actions[N-1]
        self.actions = actions
        self.counter += 1
        self.prev_action = actions[N-1]

        return actions[N-1]

    def backward(self, reward, terminal) -> None:
        pass

    @property
    def layers(self):
        pass

    def alter_x(self, x: np.ndarray) -> np.ndarray:
        return x

    def can_exploit(self) -> bool:
        return True