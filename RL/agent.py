#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Module that contains the Agent, an extencion of Trainer class.
This classes is a test of use a RL method in Game.

It contains the following classes:

	Agent
"""

# Local imports
from Game.engine.trainer import Trainer, ALLY, FOE
from Game.engine.core.pokemon import Pokemon, possible_pokemons_names

# 3rd party imports
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.optimizers import Adam

# General imports
from random import randint, choice, random, sample
from numpy import argmax
from copy import deepcopy as copy
from collections import deque


__version__ = '0.5'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'


"""
	Extended class from Trainer that use RL.
"""
class Agent(Trainer):
    def __init__(self):
        self.state_size = 30
        self.action_size = 4*2
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95   # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()

        pokemon_name = choice(possible_pokemons_names())
        Trainer.__init__(self,ALLY,Pokemon(pokemon_name, 50))

    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse',
                      optimizer=Adam(lr=self.learning_rate))
        return model

    def remember(self, reward, done):
        state = self.get_state_coded(self.last_state)
        action = self.get_action_coded()
        next_state = self.get_state_coded(self.actual_state)
        self.memory.append((state, action, reward, next_state, done))

    def set_state(self, state):
        self.actual_state = state
        self.last_state = copy(state)

    def choice_action(self):
        if random() <= self.epsilon:
            self._idmove = randint(0, self.num_moves_can_use()-1)
            self._target = randint(0, 1)
        else:
            act_values = self.model.predict(state)
            argmax(act_values[0])  # TODO save action

    def recive_results(self, attacks, done):
        self.actual_state
        #TODO calc reward

        self._remember(reward, done)
        self.last_state = copy(state)

    # train the agent with the experience of the episode
    def replay(self):
        batch_size = 32
        minibatch = sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
              target = reward + self.gamma * \
                       np.amax(self.model.predict(next_state)[0])
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
