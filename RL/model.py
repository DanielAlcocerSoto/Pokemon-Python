
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
from keras.models import Sequential, load_model
from keras.layers import Dense, Activation
from keras.optimizers import Adam

# General imports
from random import randint, choice, random, sample
from numpy import argmax, amax, array
from copy import deepcopy as copy
from ast import literal_eval
from pandas import read_csv
import csv


__version__ = '0.5'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'



file_log = "RL/Data/log"
model_path = "RL/Data/"






"""
	Extended class from Trainer that use RL.
"""
class Model:
	def __init__(self, model_file=None):
		self.gamma = 0.95   # discount rate
		self.epsilon = 1.0  # exploration rate --var
		self.epsilon_min = 0.01 #train
		self.epsilon_decay = 0.995 #train
		if model_file == None: self.model = self._build_model()
		else: self.model = load_model(model_path+model_file+'.h5')

	def _build_model(self, learning_rate = 0.001, state_size = 10):
		# Neural Net for Deep-Q learning Model
		# Sequential() creates the foundation of the layers.
		model = Sequential()
		# 'Dense' is the basic form of a neural network layer
		# Input Layer of state size(4) and Hidden Layer with 24 nodes
		model.add(Dense(24, input_dim=self.state_size, activation='relu'))
		# Hidden layer with 24 nodes
		model.add(Dense(24, activation='relu'))
		# Output Layer with # of actions: 8 nodes (left, right)
		model.add(Dense(4*2, activation='linear'))
		# Create the model based on the information above
		model.compile(loss='categorical_crossentropy',
		              optimizer=Adam(lr=self.learning_rate))
		return model

	def _encode_state(self, state):
		#TODO  index-->value
		return [1,2,3,4,5,6,7,8,9,0]

	def _encode_action(self,move, target):
		return target*4 + move

	def _decode_action(self, action):
		return action%4, action//4,

	def remember(self, state, move, target, reward, next_state, done):
		state = self._encode_state(state)
		action = self._encode_action(move, target)
		next_state = self._encode_state(next_state)
		obj = (state, action, reward, next_state, done)
	    with open(file_log+'.csv', 'a') as csv_file:
	        writer = csv.writer(csv_file)
	        writer.writerow(obj)

	def predict(self, state):
		state = self._encode_state(state)
		act_values = self.model.predict(state)
		print(act_values)#see how is it
		action = argmax(act_values[0])
		return move, target = self._decode_action(action)

	def _load():
		df = read_csv(file_log+'.csv', delimiter=',', header=None)
		ret = [ array (
				[literal_eval(field) if isinstance(field, str) else field
				 for field in row]
				) for row in df.values]
		return ret

	# train the agent with the experience of the episode
	def train(self):
		memory = self._load()
		batch_size = min(len(memory),32)
		minibatch = sample(memory, batch_size)
		for state, action, reward, next_state, done in minibatch:
			state = array([state]) # list of inputs in a numpy.array
			next_state = array([next_state])
			target = reward
			if not done:
				target = reward + self.gamma * \
			           amax(self.model.predict(next_state)[0])
			target_f = self.model.predict(state)
			target_f[0][action] = target
			self.model.fit(state, target_f, epochs=1, verbose=0)
		if self.epsilon > self.epsilon_min:
			self.epsilon *= self.epsilon_decay

	def save(self, model_file):
		self.model.save(model_path+model_file+'.h5')
