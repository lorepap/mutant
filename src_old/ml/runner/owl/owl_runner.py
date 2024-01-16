import os
import traceback
from typing import Any

import numpy as np
import json

from helper import context, utils
from keras.optimizers import Adam
from agent.base_agent import BaseAgent
from agent.mab.base_mab_agent import BaseMabAgent
from agent.owl.owl_agent import OwlAgent
from environment.owl.owl_environment import OwlEnvironment
from network.netlink_communicator import NetlinkCommunicator
from runner.base_runner import BaseRunner
import tensorflow as tf
from tensorflow.python.keras.optimizer_v2 import optimizer_v2
from helper.moderator import Moderator


class OwlRunner(BaseRunner):

    def __init__(self, nchoices: int, lr: int, num_features: int,
                 window_len: int, num_fields_kernel: int, jiffies_per_state: int,
                 steps_per_episode: int, delta: float, 
                 comm: NetlinkCommunicator, moderator: Moderator, **kwargs) -> None:
        super(OwlRunner, self).__init__()

        self.nchoices = nchoices
        self.lr = lr
        self.num_features = num_features
        self.kwargs = kwargs
        self.window_len = window_len

        self.base_config_dir = os.path.join(context.entry_dir, 'log/owl/config')
        self.config_path = os.path.join(
            self.base_config_dir, f'{self.get_tag()}.json')
        self.config = self.load_config(self.config_path)

        self.environment = OwlEnvironment(num_features, window_len, num_fields_kernel, jiffies_per_state,
                                          nchoices, steps_per_episode, delta, comm, moderator)
        # Model dir to save and load old trained models
        self.model_path = os.path.join(
            context.entry_dir, f'log/owl/model')
        # Model dir is given to set_latest to load latest trained model
        self.set_latest(self.model_path)
        self.graph = tf.Graph()

    def load_basic(self) -> Any:
        try:

            model = OwlAgent(self.num_features, self.window_len, self.nchoices)
            model.compile(self.get_optimizer(), metrics=['mae'])
            return model

        except Exception as error:
            print(traceback.format_exc())
            return None

    def get_model(self) -> BaseAgent:
        return self.model

    def get_optimizer(self) -> optimizer_v2.OptimizerV2:
        return Adam(lr=self.lr)

    def get_tag(self) -> str:
        return 'owl'

    def train(self, training_steps: int, reset_model: bool = True) -> Any:
        if reset_model:
            self.reset_model()

        self.train_res = self.model.fit(
            self.environment, nb_steps=training_steps, visualize=True, verbose=2)

        self.history = self.train_res.history
        return self.history

    def test(self, episodes: int, trace: str) -> None:
        self.environment.enable_log_traces()
        self.model.test(self.environment,
                        nb_episodes=episodes, visualize=True)

        tag = f'{trace}.{self.get_tag()}'

        # save logs
        log_name, log_path = self.environment.save_log(tag, 'log/owl/trace')

        # update config
        self.config['traces'].append({
            'model_name': self.model.get_model_name(),
            'trace_name': log_name,
            'path': log_path,
            'timestamp': self.now
        })
        self.save_config(self.config_path, self.config)

    def predict(self, x: np.ndarray) -> np.ndarray:
        # with self.graph.as_default():
        state = np.zeros((self.num_features, self.window_len))

        for _ in range(5):
            state = np.roll(state, -1, axis=1)
            state[:, -1] = x.astype(int)

        agent = self.model
        # agent.reset_states()
        model: tf.keras.Model = agent.get_model().model
        # q_values = agent.compute_q_values(state.reshape((1, self.num_features, self.window_len)))
        # model.reset_states()
        q_values = agent.forward(state)
        # q_values = model.predict(state.reshape(
        #     (1, 1, self.num_features, self.window_len)))
        return q_values

    def save_history(self, history: dict) -> None:
        # use a different alias for each run history
        path = os.path.join(
            context.entry_dir, f'log/owl/history/{self.model.get_model_name()}.{self.now}.json')

        with open(path, 'w+') as file:
            json.dump(history, file, default=self.np_encoder)

        # update config
        self.config['runs'].append({
            'name': self.model.get_model_name(),
            'path': path,
            'timestamp': self.now
        })
        self.save_config(self.config_path, self.config)

    def save_model(self, reset_model: bool = True) -> str:
        path = os.path.join(
            context.entry_dir, f'log/owl/model/{self.model.get_model_name()}.h5')

        self.model.save_weights(path, True)

        self.model_config = {
            'name': self.model.get_model_name(),
            'path': path,
            'timestamp': self.now,
            'score': self.calculate_score(),
            'prod_score': self.calculate_score()
        }

        # update config
        if reset_model:
            self.config['models'].append(self.model_config)
        else:
            self.update_model_in_config(self.config, self.model_config)

        self.save_config(self.config_path, self.config)

        return self.model.get_model_name()

    def calculate_score(self) -> float:
        return np.mean(self.history['episode_reward'])

    def close(self) -> None:
        self.environment.close()
