
#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Module that contains the Model, main class of RL.

It contains the following class:

	Model
"""

# Local import
from Configuration.settings import Directory, Agent_config
from .encoder import Encoder

# 3rd party imports
from keras.models import Sequential, load_model
from keras.layers import Dense, Activation
from keras.optimizers import Adam

# General imports
from random import random, sample
from numpy import argmax, amax, array
from copy import deepcopy as copy
from ast import literal_eval
from pandas import read_csv
from os.path import exists
import csv


__version__ = '0.5'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'


"""
	Extended class from Trainer that use RL.
"""
class Model:
	def __init__(self, model_file=None, log_file=None):
		self.encoder = Encoder()
		self.gamma = Agent_config['GAMMA']   # discount rate
		# Log_file
		if log_file == None: log_file = Agent_config['DEFAULT_LOG']
		self.log_file = Directory['DIR_LOGS'] + log_file + '.csv'
		# Model_file
		mf = Agent_config['DEFAULT_MODEL'] if model_file == None else model_file
		self.model_file = Directory['DIR_MODELS'] + mf + '.h5'
		# Model
		if model_file == None or not exists(self.model_file):
			self.model = self._build_model()
		else: self.model = load_model(self.model_file)

	def save(self, model_file=None):
		print('Saving model...')
		if model_file==None: model_file = self.model_file
		else: model_file = Directory['DIR_MODELS'] + model_file + '.h5'
		self.model.save(model_file)

	def _build_model(self):
		# Neural Net for Deep-Q learning Model
		# Sequential() creates the foundation of the layers.
		# 'Dense' is the basic form of a neural network layer
		Neural_net = zip(Agent_config['NEURAL_NET_NODES'],\
						 Agent_config['NEURAL_NET_ACTIVATION'])
		dim_input = self.encoder.state_size
		Neural_net = list(Neural_net)
		last = len(Neural_net) - 1
		model = Sequential()
		for i, (nodes, act_func) in enumerate(Neural_net):
			# Input Layer of state size and Hidden Layer with 24 nodes
			if i==0:layer=Dense(nodes,input_dim=dim_input,activation=act_func)
			# Output Layer with # of actions: 4*2 nodes
			elif i==last:layer = Dense(8, activation=act_func)
			# Hidden layer with X nodes
			else: layer = Dense(nodes, activation=act_func)
			model.add(layer)
			#model.add(Dropout(0.5))
		# Create the model based on the information above
		# Configure the learning process,
		model.compile(optimizer='rmsprop',#Adam(lr=learning_rate), #rmsprop
              		  loss='categorical_crossentropy',
			  		  metrics=['accuracy']) # categorical_accuracy
		return model

	def _calc_reward(self, my_role, attacks):
		# TODO self.actual_state
		if my_role in attacks.keys():
			attack=attacks[my_role]
			return attack.dmg
		else: return 0

	def remember(self, state, move, target, my_role, attacks, next_state, done):
		state = self.encoder.encode_state(state)
		action = self.encoder.encode_action(move, target)
		reward = self._calc_reward(my_role, attacks)
		print('reward= ',reward)
		next_state = self.encoder.encode_state(next_state)
		#save
		obj = (state, action, reward, next_state, done)
		print('Saving in log...')
		with open(self.log_file, 'a') as csv_file:
			csv.writer(csv_file).writerow(obj)

	def predict(self, state):
		print('Predicting...')
		state = array([self.encoder.encode_state(state)])
		act_values = self.model.predict(state)
		print('Result keras model: {}'.format(act_values))
		ret = self.encoder.decode_action(act_values[0])
		print('Result my model: {}'.format(ret))
		return ret

	def _load(self):
		df = read_csv(self.log_file, delimiter=',', header=None)
		ret = [ array (
				[literal_eval(field) if isinstance(field, str) else field
				 for field in row]
				) for row in df.values]
		return ret

	# train the agent with the experience of the episode
	def train(self,	batch_factor = Agent_config['BATCH_FACTOR']):
		memory = self._load()
		minibatch = sample(memory,  int(len(memory)*batch_factor))
		# Extract informations from each memory
		print('Training...')
		"""
		for state, action, reward, next_state, done in minibatch:
			state = array([state]) # list of inputs in a numpy.array
			next_state = array([next_state])
			# if done, make our target reward
			target = reward
			if not done: # predict the future discounted reward
				target += self.gamma * amax(self.model.predict(next_state)[0])

			# make the agent to approximately map
		    # the current state to future discounted reward
		    # We'll call that target_f
			target_f = self.model.predict(state)
			target_f[0][action] = target

			# Train the Neural Net with the state and target_f
			self.model.fit(state, target_f,epochs=1,verbose=0)
		"""
		print('Preparing fit...')
		states, actions, rewards, next_states, dones = zip(*minibatch)
		states = array(states) # list of inputs in a numpy.array
		next_states = array(next_states)
		targets = [reward if done else
				  reward + self.gamma * amax(self.model.predict(next_states)[0])
				  for reward, done in zip(rewards, dones)]
		target_f = self.model.predict(states)
		for i, (action, target) in enumerate(zip(actions, targets)):
			target_f[i][action] = target

		# Train the Neural Net with the state and target_f
		print('Fitting...')
		self.model.fit( states, target_f,
						batch_size=Agent_config['BATCH_SIZE_FACTOR'],
						validation_split = Agent_config['VAL_SPLIT_FIT'],
						epochs=Agent_config['EPOCHS_FIT'],
						verbose=Agent_config['VERBOSE_FIT'])
