import json
import os
import time
from typing import Any


import numpy as np
from helper import context, utils
from helper.debug import is_debug_on, change_name
from callbacks import TrainingCallback
from keras.optimizers import Adam
from agent.base_agent import BaseAgent
from agent.single_protocol_agent import SingleProtocolAgent
from environment.mab.mab_environment import MabEnvironment
from network.netlink_communicator import NetlinkCommunicator
from runner.base_runner import BaseRunner
from tensorflow.python.keras.optimizer_v2 import optimizer_v2
from helper.moderator import Moderator


class SingleBaseRunner(BaseRunner):

    def __init__(self, nchoices: int, lr: int, num_features: int,
                 window_len: int, num_fields_kernel: int, jiffies_per_state: int,
                 steps_per_episode: int, delta: float, step_wait_seconds: float, 
                 comm: NetlinkCommunicator, moderator: Moderator, trace: str, protocol: str, retrain: bool = False, reward_name: str = 'owl') -> None:
        super(SingleBaseRunner, self).__init__()

        self.nchoices = nchoices
        self.lr = lr
        self.moderator = moderator
        self.num_features = num_features
        self.protocol = protocol
        self.model: SingleProtocolAgent = SingleProtocolAgent(moderator, protocol)

        self.base_config_dir = os.path.join(context.entry_dir, 'log/mab/config')
        self.trace_name = trace
        self.config_path = os.path.join(
            self.base_config_dir, f'{self.get_tag()}.json')
        self.config = self.load_config(self.config_path)
        # self.model_path = os.path.join(context.entry_dir, f'log/mab/model')
        self.environment = MabEnvironment(num_features, window_len, num_fields_kernel, jiffies_per_state,
                                    nchoices, steps_per_episode, delta, step_wait_seconds, comm, moderator, reward_name)
        
        # self.set_latest(self.model_path, retrain)
        self.training_time = None
        self.step_wait_time = step_wait_seconds
        self.steps_per_episode = steps_per_episode
        self.num_fields_kernel = num_fields_kernel

    def get_model(self) -> SingleProtocolAgent:
        return self.model

    def get_model_config(self) -> dict:
        return self.model_config

    def get_optimizer(self) -> optimizer_v2.OptimizerV2:
        return Adam(lr=self.lr)

    def get_tag(self) -> str:
        return self.protocol

    def test(self, episodes: int) -> None:
        
        self.environment.enable_log_traces()
        now = self.now

        if not(is_debug_on()):
            cb: TrainingCallback = TrainingCallback(log_file_path=os.path.join(
                context.entry_dir, f'log/mab/history/{self.protocol}.{now}.json')
            )
        else:
            cb: TrainingCallback = TrainingCallback(log_file_path=os.path.join(
                context.entry_dir, f'log/mab/history/debug_{self.protocol}.{now}.json')
            )
        
        self.model.native_prot_test(self.environment,
                        nb_episodes=episodes, visualize=False, callbacks=[cb])

        tag = f'{self.trace_name}.{self.get_tag()}'

        # save logs
        log_name, log_path = self.environment.save_log(tag, 'log/mab/trace')
        if is_debug_on():
            log_name = change_name(log_name)

        # update config
        if not(is_debug_on()):
            self.config['traces'].append({
                'trace_name': log_name,
                'path': log_path,
                'timestamp': self.now
            })
            self.save_config(self.config_path, self.config)


    def save_history(self, history: dict) -> None:
        path = os.path.join(
            context.entry_dir, f'log/mab/history/episode_hist_{self.model.get_model_name()}.{self.now}.json')

        with open(path, 'w+') as file:
            json.dump(history, file, default=self.np_encoder)

        # update config
        self.config['runs'].append({
            'model_name': self.model.get_model_name(),
            'path': path,
            'timestamp': self.now,
            'training_time': self.training_time,
            'trace': self.trace_name,
            'actions': self.nchoices,
            'step_wait': self.step_wait_time,
            'num_features': self.num_features,
            'num_kernel_fields': self.num_fields_kernel,
            'steps_per_episode': self.steps_per_episode,
            'reward': self.environment.reward_name
        })
        self.save_config(self.config_path, self.config)

    def calculate_score(self) -> float:
        return np.mean(self.history['episode_reward']) if self.history != None else 0

    def close(self) -> None:
        self.environment.close()