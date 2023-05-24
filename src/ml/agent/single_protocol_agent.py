from datetime import datetime
from typing import Any
import warnings
from copy import deepcopy


import numpy as np
import tensorflow as tf
from contextualbandits.online import _BasePolicy
from helper import utils
from rl.core import Agent
from tensorflow.keras.callbacks import History


from rl.callbacks import (
    CallbackList,
    TestLogger,
    TrainEpisodeLogger,
    TrainIntervalLogger,
    Visualizer
)

protocols = {
    "cubic": 0,
    "bbr": 1,
    "hybla": 2,
    "vegas": 3,
    "pcc": 4
}

class SingleProtocolAgent(Agent):

    def __init__(self, moderator=None, protocol=0, **kwargs):
        super(SingleProtocolAgent, self).__init__(**kwargs)

        self.now = utils.time_to_str()
        # The action is the protocol given as input to the agent
        self.protocol = protocol
        self.action = protocols[self.protocol]
        # self.model_name = f'{self.get_tag()}.{self.now}'
        self.orig_name = f'{self.get_tag()}.{self.now}'
        self.moderator = moderator


    def get_tag(self):
        return self.protocol
    
    # def get_model_name(self) -> str:
    #     return self.model_name

    def native_prot_test(self, env, nb_episodes=1, action_repetition=1, callbacks=None, visualize=True,
                nb_max_episode_steps=None, nb_max_start_steps=0, start_step_policy=None, verbose=1):
            """
            Take always the same action for testing a native protocol (cubic, bbr, etc.) inside mimic.
            """

            action = self.action
            
            # if not self.compiled:
            #     raise RuntimeError('Your tried to test your agent but it hasn\'t been compiled yet. Please call `compile()` before `test()`.')
            # if action_repetition < 1:
            #     raise ValueError('action_repetition must be >= 1, is {}'.format(action_repetition))

            self.training = False
            self.step = 0

            callbacks = [] if not callbacks else callbacks[:]

            if verbose >= 1:
                callbacks += [TestLogger()]
            if visualize:
                callbacks += [Visualizer()]
            history = History()
            callbacks += [history]
            callbacks = CallbackList(callbacks)
            if hasattr(callbacks, 'set_model'):
                callbacks.set_model(self)
            else:
                callbacks._set_model(self)
            callbacks._set_env(env)
            params = {
                'nb_episodes': nb_episodes,
            }
            if hasattr(callbacks, 'set_params'):
                callbacks.set_params(params)
            else:
                callbacks._set_params(params)

            self._on_test_begin()
            callbacks.on_train_begin()
            for episode in range(nb_episodes):

                callbacks.on_episode_begin(episode)
                episode_reward = 0.
                episode_step = 0

                # Obtain the initial observation by resetting the environment.
                self.reset_states()
                observation = deepcopy(env.reset())
                if self.processor is not None:
                    observation = self.processor.process_observation(observation)
                assert observation is not None

                # Perform random starts at beginning of episode and do not record them into the experience.
                # This slightly changes the start position between games.
                nb_random_start_steps = 0 if nb_max_start_steps == 0 else np.random.randint(nb_max_start_steps)
                for _ in range(nb_random_start_steps):
                    if start_step_policy is None:
                        action = env.action_space.sample()
                    else:
                        action = start_step_policy(observation)
                    if self.processor is not None:
                        action = self.processor.process_action(action)
                    callbacks.on_action_begin(action)
                    observation, r, done, info = env.step(action)
                    observation = deepcopy(observation)
                    if self.processor is not None:
                        observation, r, done, info = self.processor.process_step(observation, r, done, info)
                    callbacks.on_action_end(action)
                    if done:
                        warnings.warn('Env ended before {} random steps could be performed at the start. You should probably lower the `nb_max_start_steps` parameter.'.format(nb_random_start_steps))
                        observation = deepcopy(env.reset())
                        if self.processor is not None:
                            observation = self.processor.process_observation(observation)
                        break

                # Run the episode until we're done.
                # Edit: check if iperf simulation has done (moderator class)
                done = False
                try:
                    while not done:
                        if self.moderator.is_stopped():
                            print("exiting rl-module....\n")
                            raise StopIteration

                        callbacks.on_step_begin(episode_step)

                        # We have always the same predefined action (protocol under test)
                        # action = self.forward(observation)
                        
                        # if self.processor is not None:
                        #     action = self.processor.process_action(action)
                        
                        reward = 0.
                        accumulated_info = {}
                        for _ in range(action_repetition):
                            callbacks.on_action_begin(action)
                            observation, r, d, info = env.step(action)
                            observation = deepcopy(observation)
                            if self.processor is not None:
                                observation, r, d, info = self.processor.process_step(observation, r, d, info)
                            callbacks.on_action_end(action)
                            reward += r
                            for key, value in info.items():
                                if not np.isreal(value):
                                    continue
                                if key not in accumulated_info:
                                    accumulated_info[key] = np.zeros_like(value)
                                accumulated_info[key] += value
                            if d:
                                done = True
                                break
                        if nb_max_episode_steps and episode_step >= nb_max_episode_steps - 1:
                            done = True
                        
                        # We do not need to update anything
                        # self.backward(reward, terminal=done)

                        episode_reward += reward

                        step_logs = {
                            'action': action,
                            'observation': observation,
                            'reward': reward,
                            'episode': episode,
                            'info': accumulated_info,
                        }
                        callbacks.on_step_end(episode_step, step_logs)
                        episode_step += 1
                        self.step += 1

                except StopIteration:
                    break

                # We are in a terminal state but the agent hasn't yet seen it. We therefore
                # perform one more forward-backward call and simply ignore the action before
                # resetting the environment. We need to pass in `terminal=False` here since
                # the *next* state, that is the state of the newly reset environment, is
                # always non-terminal by convention.
                # self.forward(observation)
                # self.backward(0., terminal=False)

                # Report end of episode.
                episode_logs = {
                    'episode_reward': episode_reward,
                    'nb_steps': episode_step,
                }
                callbacks.on_episode_end(episode, episode_logs)
            callbacks.on_train_end()
            self._on_test_end()

            return history
