
from typing import Any

import dill as pickle
import numpy as np
from agent.base_agent import BaseAgent
from contextualbandits.online import _BasePolicy


class BaseMabAgent(BaseAgent):

    def __init__(self, nchoices: int, **kwargs) -> None:
        super(BaseMabAgent, self).__init__(**kwargs)

        self.counter = 0
        self.prev_action = 0

        self.model = self.get_policy(nchoices)

    def get_model(self) -> _BasePolicy:
        return self.model

    def get_policy(self, choices: int) -> _BasePolicy:
        """
            Builds the multi-arm bandit policy
        """

        raise NotImplementedError()

    def load_weights(self, filepath) -> None:

        with open(filepath, 'rb') as file:
            self.model = pickle.load(file)

    def save_weights(self, filepath, overwrite=False) -> None:

        with open(filepath, 'wb') as file:
            pickle.dump(self.model, file)

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
        actions = self.model.predict(observation['obs']).astype('uint8')
        # print("[DEBUG] actions: ", actions)
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

        if not self.training or 'rewards' not in self.recent_observation:
            return {}

        np.random.seed(self.counter)

        N = len(self.actions)

        # print(self.recent_observation.shape)
        # print(self.actions)
        # print(len(reward))

        # print(f'Observation: {self.recent_observation.shape} | Rewards: {len(reward)}')

        # if isinstance(reward, float):
        #     lr_reward = [reward for _ in range(N)]
        # else:
        #     lr_reward = reward

        self.model.partial_fit(
            self.recent_observation['obs'],
            np.array(self.actions),
            np.array(self.recent_observation['rewards']))

    @property
    def layers(self):
        pass

    def alter_x(self, x: np.ndarray) -> np.ndarray:
        return x

    def can_exploit(self) -> bool:
        return True