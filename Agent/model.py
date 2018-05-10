
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
              		  loss='mse',
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

	# Train the agent with the experience of the episode
	def train(self,	memory):
		# Extract informations from each memory
		print('Training model with this battle...')
		for state, action, reward, next_state, done in memory:
			self.learn_turn(state, action, reward, next_state, done)

	# Train the agent with the experience of a turn
	def learn_turn(self,state, action, reward, next_state, done):
		learning_rate = Agent_config['LEARNING_RATE_RL']
		gama = Agent_config['GAMMA_DISCOUNTING_RATE']
		state = array([state])
		next_state = array([next_state])

		target_f = self.model.predict(state)[0]
		aux = 0
		if not done:
			aux = gamma*amax(self.model.predict(next_state)[0])-target_f[action]
		target_f[action] += learning_rate*(reward+aux)

		# Train the Neural Net with the state and target_f
		self.model.fit(state, target_f, epochs=1, verbose=0)


	def _load_log_memory(self,log_file):
		df = read_csv(log_file, delimiter=',', header=None)
		ret = [ [literal_eval(field) if isinstance(field, str) else field
				 for field in row] for row in df.values]
		return ret

	def rebuid_Q_function(self, log_file):
		print('Rebuilding Q-function\nPreparing fit...')
		memory = self._load_log_memory(log_file)
		# Extract informations from each memory
		learning_rate = Agent_config['LEARNING_RATE_RL']
		gama = Agent_config['GAMMA_DISCOUNTING_RATE']
		states, actions, rewards, next_states, dones = zip(*memory)
		dones = array(dones)
		states = array(states)
		rewards = array(rewards)
		next_states = array(next_states)
		predict_s = self.model.predict(states) # Actual prediction

		# Calculate new prediction
		Q_s_a = array([pred[action] for pred, action in zip(predict_s,actions)])
		Q_next = array(list(map(amax,self.model.predict(next_states))))
		news_Q = Q_s_a + learning_rate*(rewards + dones*(gama*Q_next - Q_s_a))
		# Replace new Q-value in predict_s
		for pred, act, new in zip(predict_s, actions, news_Q): pred[act] = new

		# Train the Neural Net with the state and news_rewards
		print('Fitting...')
		self.model.fit( states, predict_s,
						batch_size=Agent_config['BATCH_SIZE_FACTOR'],
						validation_split = Agent_config['VAL_SPLIT_FIT'],
						epochs=Agent_config['EPOCHS_FIT'],
						verbose=Agent_config['VERBOSE_FIT'])
