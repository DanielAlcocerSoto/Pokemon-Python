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
from pandas import read_csv
import csv
from numpy import amax


__version__ = '0.5'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'



memory = "RL/Data/log"

def save(obj):
    with open(memory+'.csv', 'a') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(obj)

def load():
    df = read_csv(memory+'.csv', delimiter=',', header=None)
    return [tuple(x) for x in df.values]


"""
	Extended class from Trainer that use RL.
"""
class Agent(Trainer):
	def __init__(self):
		self.state_size = 30
		self.action_size = 4*2
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
		# Sequential() creates the foundation of the layers.
		model = Sequential()
		# 'Dense' is the basic form of a neural network layer
		# Input Layer of state size(4) and Hidden Layer with 24 nodes
		model.add(Dense(24, input_dim=self.state_size, activation='relu'))
		# Hidden layer with 24 nodes
		model.add(Dense(24, activation='relu'))
		# Output Layer with # of actions: 2 nodes (left, right)
		model.add(Dense(self.action_size, activation='linear'))
		# Create the model based on the information above
		model.compile(loss='mse',
		              optimizer=Adam(lr=self.learning_rate))
		return model

	def _get_state_coded(self, state):
		#TODO  index-->value
		return [1,2,3,4,5,6,7,8,9,0]

	def _get_action_coded(self):
		return self._idmove*10+self._target

	def _decode_action(self, action):
		return action//10, action%10

	def _remember(self, reward, done):
		state = self._get_state_coded(self.last_state)
		action = self._get_action_coded()
		next_state = self._get_state_coded(self.actual_state)
		# state = array floats
		# action = num
		#
		save((state, action, reward, next_state, done))

	def set_state(self, state):
	    self.actual_state = state
	    self.last_state = copy(state)

	def choice_action(self):
		if random() <= self.epsilon:
			self._idmove = randint(0, self.num_moves_can_use()-1)
			self._target = randint(0, 1)
		else:
			state = self._get_state_coded(self.actual_state)
			act_values = self.model.predict(state)
			action = argmax(act_values[0])
			self._idmove, self._target = self._decode_action(action)


	def recive_results(self, attacks):

		#TODO calc reward self.actual_state
		reward = 5
		self._remember(reward, self.pokemon().is_fainted())
		self.last_state = copy(self.actual_state)

	# train the agent with the experience of the episode
	def replay(self):
		memory = load()
		batch_size = min(len(memory),32)
		minibatch = sample(memory, batch_size)
		for state, action, reward, next_state, done in minibatch:
			target = reward
			if not done:
			  target = reward + self.gamma * \
			           amax(self.model.predict(next_state)[0])
			target_f = self.model.predict(state)
			target_f[0][action] = target
			self.model.fit(state, target_f, epochs=1, verbose=0)
		if self.epsilon > self.epsilon_min:
			self.epsilon *= self.epsilon_decay
