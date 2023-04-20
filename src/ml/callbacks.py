import copy
from keras.callbacks import Callback
import json
import numpy as np
import copy

class TrainingCallback(Callback):
    def __init__(self, log_file_path):
        super(TrainingCallback, self).__init__()
        self.log_file_path = log_file_path
        
    def np_encoder(self, object):
        if isinstance(object, np.generic):
            return object.item()
    
    def on_step_end(self, step, logs=None):
        # append logs to external file
        log_copy: dict = copy.deepcopy(logs)
        # obs = log_copy["observation"].pop("obs")
        # log_copy["obs"] = obs.tolist()
        log_copy['observation']['obs'] = log_copy['observation']['obs'].tolist()
        with open(self.log_file_path, 'a') as f:
            f.write(json.dumps(log_copy, default=self.np_encoder) + '\n')

    
