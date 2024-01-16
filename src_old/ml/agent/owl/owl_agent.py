from typing import Any

import numpy as np
import tensorflow as tf
from agent.base_agent import BaseAgent
from keras import Sequential
from keras.layers import Activation, Dense, Flatten
from rl.agents import DQNAgent
from rl.core import Agent
from rl.memory import SequentialMemory
from rl.policy import EpsGreedyQPolicy


class OwlAgent(BaseAgent):

    def __init__(self, num_features: int, window_len: int, nchoices: int, **kwargs):
        super(OwlAgent, self).__init__(**kwargs)

        self.nchoices = nchoices
        self.num_features = num_features
        self.window_len = window_len
        self.model: Agent = self.init_model()

    def get_model(self) -> Agent:
        return self.model

    def init_model(self) -> Any:
        model = Sequential()

        # input layer
        model.add(Flatten(input_shape=(1,) +
                  (self.num_features, self.window_len)))

        # first hidden layer
        model.add(Dense(512))
        model.add(Activation('relu'))

        # second hidden layer
        model.add(Dense(256))
        model.add(Activation('relu'))

        # output layer
        model.add(Dense(self.nchoices))
        model.add(Activation('linear'))
        # model.add(Flatten()) # new

        policy = EpsGreedyQPolicy()
        memory = SequentialMemory(limit=50000, window_length=1)
        dqn = DQNAgent(model=model, nb_actions=self.nchoices, memory=memory, nb_steps_warmup=10,
                       target_model_update=1e-2, policy=policy)

        return dqn

    def save_weights(self, filepath, overwrite=False):
        self.model.save_weights(filepath, overwrite=overwrite)

    def load_weights(self, filepath) -> None:
        self.model.load_weights(filepath)


    def reset_states(self):
        return self.model.reset_states()

    def compile(self, optimizer, metrics=[]):
        self.compiled = True
        return self.model.compile(optimizer, metrics)

    def forward(self, observation):
        return self.model.forward(observation)

    def backward(self, reward, terminal):
        return self.model.backward(reward, terminal)

    def get_tag(self) -> str:
        return "owl.agent"

    @property
    def layers(self):
        return self.model.layers()


    def can_exploit(self) -> bool:
        return False

    def alter_x(self, x: np.ndarray) -> np.ndarray:
        return super().alter_x(x)
