import json
import os
from typing import Any

import numpy as np
from agent.base_agent import BaseAgent
from datetime import datetime
from helper import utils
from tensorflow.python.keras.optimizer_v2 import optimizer_v2
from helper import context


class BaseRunner():

    def __init__(self) -> None:
        self.now = utils.time_to_str()
        self.model_config: dict = None
        self.model: BaseAgent = None
        self.config = None
        self.config_path = None
        self.valid = True

    def np_encoder(self, object):
        if isinstance(object, np.generic):
            return object.item()

    def get_optimizer(self) -> optimizer_v2.OptimizerV2:
        raise NotImplementedError()

    def get_tag(self) -> str:
        raise NotImplementedError()

    def train(self, training_steps: int, reset_model: bool = True) -> Any:
        raise NotImplementedError()

    def save_history(self, history: dict) -> None:
        '''
            Saves the training history \n
            Each history file name uses a time-based alias for each trained model
        '''
        raise NotImplementedError()

    def save_model(self, reset_model: bool = True) -> str:
        raise NotImplementedError()

    def init_config(self, path: str) -> dict:

        config = {
            'models': [],
            'runs': [],
            'traces': []
        }

        self.save_config(path, config)

        print(f'{self.get_tag()}: initialized config successfully')
        return config

    def load_config(self, path: str) -> dict:

        try:
            with open(path) as file:
                config = json.load(file)

            return config

        except FileNotFoundError as error:
            print(f'Configuration file: {path} not found. So, creating one')

            return self.init_config(path)

    def save_config(self, path: str, config: dict) -> None:

        with open(path, 'w+') as file:
            json.dump(config, file, default=self.np_encoder,
                      indent=4, sort_keys=True)

        print(f'{self.get_tag()}: saved config successfully')

    def test(self, episodes: int) -> None:
        raise NotImplementedError()

    def load_basic(self) -> Any:
        raise NotImplementedError()

    def reset_model(self) -> None:
        self.model: BaseAgent = self.load_basic()
        self.model.reset_name()
        self.model_config = {}

    def load_best(self, config: dict) -> BaseAgent:

        models = config['models']

        if len(models) == 0:
            return self.load_basic(), {}

        sorted_models = sorted(
            models, key=lambda model: model['score'], reverse=True)
        selected_model_config = sorted_models[0]

        model: BaseAgent = self.load_basic()
        model.load_weights(selected_model_config['path'])
        model.set_model_name(selected_model_config['name'])

        print(
            f'{self.get_tag()}: loaded {selected_model_config["name"]} as best model')
        return model, selected_model_config

    def load_latest(self, config: dict, model_path: str, retrain=False) -> BaseAgent:

        models = config['models']

        if len(models) == 0:
            return self.load_basic(), {}

        sorted_models = sorted(
            models, key=lambda model: utils.str_to_time(model['timestamp']), reverse=True)
        selected_model_config = sorted_models[0]

        # Correct path when using new mimic environment
        # TODO: correct every entry in the model directory
        model: BaseAgent = self.load_basic()
        # model.load_weights(selected_model_config['path'])
        if not(retrain):
            model.load_weights(os.path.join(model_path, selected_model_config['name']+'.h5'))
        else:
            print("[DEBUG] retraining model from scratch...")

        model.set_model_name(selected_model_config['name'])

        print(
            f'{self.get_tag()}: loaded {selected_model_config["name"]} as latest model')
        return model, selected_model_config

    def get_model(self) -> BaseAgent:
        raise NotImplementedError()

    def predict(self, x: np.ndarray) -> np.ndarray:
        raise NotImplementedError()

    def calculate_score(self) -> float:
        raise NotImplementedError()

    def get_prod_score(self) -> float:

        if self.model_config is not None:
            return self.model_config['prod_score']

        return 0

    def get_test_score(self) -> float:

        if self.model_config is not None:
            return self.model_config['score']

        return 0

    def update_prod_score(self, score: float) -> None:

        self.model_config['prod_score'] = score

        for model in self.config['models']:

            if model['name'] == self.model_config['name']:
                model['prod_score'] = score
                break

        self.save_config(self.config_path, self.config)

    def close(self) -> None:
        raise NotImplementedError()

    def set_best(self) -> None:
        self.model, self.model_config = self.load_best(self.config)

    def set_latest(self, model_path: str, retrain: bool) -> None:
        self.model, self.model_config = self.load_latest(self.config, model_path, retrain)

    def is_valid(self) -> bool:
        return 'name' in self.model_config.keys() and self.valid

    def mark_invalid(self) -> None:
        self.valid = False

    def update_model_in_config(self, config: dict, model: dict) -> None:

        newlist = []

        if len(config['models']) == 0:
            config['models'].append(model)
            return

        for current_model in config['models']:

            if current_model['name'] == model['name']:
                newlist.append(model)
            else:
                newlist.append(current_model)

        config['models'] = newlist
