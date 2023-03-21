import json
import os
import time
from typing import Any

import numpy as np
from helper import context, utils
from keras.optimizers import Adam
from agent.base_agent import BaseAgent
from agent.mab.base_mab_agent import BaseMabAgent
from environment.mab.mab_environment import MabEnvironment
from network.netlink_communicator import NetlinkCommunicator
from runner.base_runner import BaseRunner
from tensorflow.python.keras.optimizer_v2 import optimizer_v2
from helper.moderator import Moderator

class MabBaseRunner(BaseRunner):

    def __init__(self, nchoices: int, lr: int, num_features: int,
                 window_len: int, num_fields_kernel: int, jiffies_per_state: int,
                 steps_per_episode: int, delta: float, step_wait_seconds: float, 
                 comm: NetlinkCommunicator, moderator: Moderator, trace: str) -> None:
        super(MabBaseRunner, self).__init__()

        self.nchoices = nchoices
        self.lr = lr

        self.base_config_dir = os.path.join(context.entry_dir, 'log/mab/config')
        self.config_path = os.path.join(
            self.base_config_dir, f'{self.get_tag()}.json')
        self.config = self.load_config(self.config_path)
        self.model_path = os.path.join(
            context.entry_dir, f'log/mab/model')
        self.environment = MabEnvironment(num_features, window_len, num_fields_kernel, jiffies_per_state,
                                    nchoices, steps_per_episode, delta, step_wait_seconds, comm, moderator)
        
        self.set_latest(self.model_path)
        self.training_time = None

        self.trace_name = trace

    def get_model(self) -> BaseAgent:
        return self.model

    def get_optimizer(self) -> optimizer_v2.OptimizerV2:
        return Adam(lr=self.lr)

    def get_tag(self) -> str:
        raise NotImplementedError()

    def train(self, training_steps: int, reset_model: bool = True) -> Any:
        if reset_model:
            self.reset_model()
        
        start = time.time()
        
        self.train_res = self.model.fit(self.environment, nb_steps=training_steps,
            visualize=False, verbose=2)
        
        self.training_time = time.time() - start
        
        self.history = self.train_res.history

        return self.history

    def test(self, episodes: int) -> None:
        self.environment.enable_log_traces()
        self.model.test(self.environment,
                        nb_episodes=episodes, visualize=False)

        tag = f'{self.trace_name}.{self.get_tag()}'

        # save logs
        log_name, log_path = self.environment.save_log(tag, 'log/mab/trace')

        # update config
        self.config['traces'].append({
            'model_name': self.model.get_model_name(),
            'trace_name': log_name,
            'path': log_path,
            'timestamp': self.now
        })
        self.save_config(self.config_path, self.config)

    def predict(self, x: np.ndarray) -> np.ndarray:
        model = self.model.get_model()

        x = self.model.alter_x(x)

        if self.model.can_exploit():
            return model.predict(x, exploit=True)
        else:
            return model.predict(x)


    def save_history(self, history: dict) -> None:
        path = os.path.join(
            context.entry_dir, f'log/mab/history/{self.model.get_model_name()}.{self.now}.json')

        with open(path, 'w+') as file:
            json.dump(history, file, default=self.np_encoder)

        # update config
        self.config['runs'].append({
            'model_name': self.model.get_model_name(),
            'path': path,
            'timestamp': self.now,
            'training_time': self.training_time,
            'trace': self.trace_name
        })
        self.save_config(self.config_path, self.config)


    def save_model(self, reset_model: bool = True) -> str:
        path = os.path.join(
            context.entry_dir, f'log/mab/model/{self.model.get_model_name()}.h5')
        # path = os.path.join(self.model_path, self.model.get_model_name() + '.' + self.trace_name +'.h5')
        self.model.save_weights(path, True)

        self.model_config = {
            'name': self.model.get_model_name(),
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
        return np.mean(self.history['episode_reward']) if self.history != None else 0

    def close(self) -> None:
        self.environment.close()
