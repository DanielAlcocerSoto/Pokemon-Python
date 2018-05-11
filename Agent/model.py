
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
	def __init__(self, model_name=None, log_name=None):
		self.encoder = Encoder()
		self.memory = []

		ln = log_name if log_name != None else Agent_config['DEFAULT_LOG']
		self.log_file = Directory['DIR_LOGS'] + ln + '.csv'
		if model_name != None:
			model_file = Directory['DIR_MODELS'] +model_name+ '.h5'
			self.keras_NN_model = load_model(model_file)
		else:
			self.keras_NN_model = self._build_model()
			if log_name != None: self._rebuid_Q_function(self.log_file)

	def predict(self, state):
		print('Predicting...')
		state = array([self.encoder.encode_state(state)])
		act_values = self.keras_NN_model.predict(state)
		print('Result keras model: {}'.format(act_values))
		ret = self.encoder.decode_action(act_values[0])
		print('Result my model: {}'.format(ret))
		return ret

	def remember(self, state, move, target, my_role, attacks, next_state, done):
		# get information
		state = self.encoder.encode_state(state)
		next_state = self.encoder.encode_state(next_state)
		action = self.encoder.encode_action(move, target)
		reward = self._get_reward(my_role, attacks)
		print('Reward of this turn = ', reward)

		obj = (state, action, reward, next_state, done)
		self.memory.append(obj)

		# Train model in each turn (incremental RL)
		if Agent_config['INCREMENTAL_TRAIN']: self._learn_turn(obj)

	def replay_and_train(self):
		# Save memory in log file
		print('Saving in log...')
		with open(self.log_file, 'a') as csv_file:
			for obj in self.memory:	csv.writer(csv_file).writerow(obj)
		# Train model with all battle (episodic RL)
		if not Agent_config['INCREMENTAL_TRAIN']: self._traing_episode()
		# Reset memory
		self.memory = []

	def save(self, model_name = None):
		if model_name==None: model_name = Agent_config['DEFAULT_MODEL']
		model_file = Directory['DIR_MODELS'] + model_name + '.h5'
		print('Saving model as {} ...'.format(model_name))
		self.keras_NN_model.save(model_file)

#private functions

	def _get_reward(self, my_role, attacks):
		# TODO self.actual_state
		if my_role in attacks.keys():
			attack=attacks[my_role]
			return attack.dmg
		else: return 0

	def _build_model(self):
		# Neural Net for Deep-Q learning Model
		Neural_net = zip(Agent_config['NEURAL_NET_NODES'],\
						 Agent_config['NEURAL_NET_ACTIVATION'])
		dim_input = self.encoder.state_size
		Neural_net = list(Neural_net)
		last = len(Neural_net) - 1
		model = Sequential() #Sequential() creates the foundation of the layers.
		for i, (nodes, act_func) in enumerate(Neural_net):
			# 'Dense' is the basic form of a neural network layer
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
              		  loss='mse', metrics=['accuracy'])
		return model

	# Train the agent with the experience of the episode
	def _traing_episode(self):
		print('Training model with this battle...')
		self.memory.reverse() #reverse for fiting first the next state
		for obj in self.memory: self._learn_turn(obj)

	# Train the agent with the experience of a turn
	def _learn_turn(self, obj):
		state, action, reward, next_state, done = obj
		learning_rate = Agent_config['LEARNING_RATE_RL']
		gamma = Agent_config['GAMMA_DISCOUNTING_RATE']
		state = array([state])
		next_state = array([next_state])

		target_f = self.keras_NN_model.predict(state)[0]
		if not done:
			reward += gamma*amax(self.keras_NN_model.predict(next_state)[0])
			reward -= target_f[action]
		target_f[action] += learning_rate*(reward)
		# Train the Neural Net with the state and target_f
		self.keras_NN_model.fit(state, array([target_f]), epochs=1, verbose=0)

	def _load_log_memory(self,log_file):
		df = read_csv(log_file, delimiter=',', header=None)
		return [[literal_eval(field) if isinstance(field, str) else field
				for field in row] for row in df.values]

	def _rebuid_Q_function(self, log_file):
		print('Rebuilding Q-function\nPreparing fit...')
		learning_rate = Agent_config['LEARNING_RATE_RL']
		gamma = Agent_config['GAMMA_DISCOUNTING_RATE']
		memory = self._load_log_memory(log_file)

		states, actions, rewards, next_states, dones = zip(*memory)
		dones = array(dones)
		states = array(states)
		rewards = array(rewards)
		next_states = array(next_states)

		predict_s = self.keras_NN_model.predict(states) # Actual prediction

		# Calculate new prediction
		Q_s_a = array([pred[action] for pred, action in zip(predict_s,actions)])
		Q_next = array(list(map(amax,self.keras_NN_model.predict(next_states))))
		news_Q = Q_s_a + learning_rate*(rewards + dones*(gamma*Q_next - Q_s_a))
		# Replace new Q-value in predict_s
		for pred, act, new in zip(predict_s, actions, news_Q): pred[act] = new

		# Train the Neural Net with the state and news_rewards
		print('Fitting...')
		self.keras_NN_model.fit( states, predict_s,
						batch_size=Agent_config['BATCH_SIZE_FACTOR'],
						validation_split = Agent_config['VAL_SPLIT_FIT'],
						epochs=Agent_config['EPOCHS_FIT'],
						verbose=Agent_config['VERBOSE_FIT'])
