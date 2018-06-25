#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Module that contains the Model, main class of RL.

It contains the following class:

	BaseModel
"""

# Local import
from Configuration.settings import Directory, Agent_config
from .encoder import Encoder

# 3rd party imports
from keras.callbacks import TensorBoard
from keras.models import Sequential, load_model
from keras.layers import Dense

# General imports
from numpy import amax, array
from ast import literal_eval
from pandas import read_csv
from csv import writer
from time import time
from os.path import exists

__version__ = '0.5'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'


class BaseModel:
	def __init__(self, model_name = None, rebuid = False):
		if model_name == None: model_name = Agent_config['MODEL_NAME']
		self.output_layer_size = 8
		self.encoder = Encoder()
		self._init_model(model_name, rebuid)

	def _init_model(self, model_name, rebuid):
		self.memory = []
		self.model_name = model_name
		self.log_file = Directory['DIR_LOGS'] + Agent_config['LOG_NAME'] + '.csv'
		self.tbCallback=TensorBoard(log_dir=Directory['TB_PATH']+self.model_name,
									histogram_freq=0,
									write_graph=True, write_images=True)
		if rebuid:
			print('Rebuilding model from {}'.format(self.log_file))
			self.keras_NN_model = self._build_model()
			self._rebuid_Q_function(self._load_log_memory(self.log_file))
		else:
			model_file=Directory['DIR_MODELS']+self.model_name+'.h5'
			if exists(model_file): self.keras_NN_model = load_model(model_file)
			else: self.keras_NN_model = self._build_model()

	def predict(self, state, role):
		state = array([self.encoder.encode_state(state, role)])
		act_values = self.keras_NN_model.predict(state)
		#print('Result of Keras model for {}: {}'.format(role,act_values))
		return self.encoder.decode_action(act_values[0])

	def remember(self, state, role, attacks, choices, next_state, done, player=False):
		if not state[role].is_fainted():
			# get information
			state = self.encoder.encode_state(state, role)
			next_state = self.encoder.encode_state(next_state, role)
			action = self.encoder.encode_action(choices, role)
			reward = self._get_reward(attacks, role)
			#print('Reward of this turn = ', reward)
			self.memory.append( (state, action, reward, next_state, player, done) )

	def train_and_save(self): # Episodic training
		if self.memory != []:
			# Train model with memory
			self._rebuid_Q_function(self.memory)
			# Save model
			self._save_model()
			# Save memory in log file
			self._save_log()
			# Reset memory
			self.memory = []

	def _save_model(self):
		model_file=Directory['DIR_MODELS']+self.model_name+'.h5'
		print('Saving model in {} ...'.format(model_file))
		self.keras_NN_model.save(model_file)

	def _save_log(self):
		print('Saving log in {} ...'.format(self.log_file))
		with open(self.log_file, 'a') as csv_file:
			for obj in self.memory:	writer(csv_file).writerow(obj)

#private functions
	def _get_reward(self, attacks, my_role):
		if my_role in attacks.keys():
			attack=attacks[my_role]
			return attack.dmg
		else: return 0

	def _build_model(self):
		# Neural Net for Deep-Q learning Model
		Neural_net = Agent_config['NEURAL_NET_DESIGN']
		dim_input = self.encoder.state_size
		model = Sequential()
		for i, (nodes, act_func) in enumerate(Neural_net):
			# Input Layer of state size and Hidden Layer
			if i==0:layer=Dense(nodes,input_dim=dim_input,activation=act_func)
			# Hidden layer with X nodes
			else: layer = Dense(nodes, activation=act_func)
			model.add(layer)  #model.add(Dropout(0.5)) #not to overfit
		# Output Layer with # of actions: 4*2 nodes
		model.add(Dense(self.output_layer_size, activation='linear'))
		# Create the model based on the information above and configure the learning process,
		model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])
		return model

	def _load_log_memory(self, log_file):
		print('Loading data...')
		now=time()
		df = read_csv(log_file, delimiter=',', header=None)
		log = [[literal_eval(field) if isinstance(field, str) else field
				for field in row] for row in df.values]
		print('Data loaded in {}s'.format(time()-now))
		return log

	def _rebuid_Q_function(self, dataset):
		header = '--------------------- RL_EPOCHS: {}/{} ---------------------'
		myheader = header.format('{}',Agent_config['EPOCHS_RL_FIT'])
		gamma = Agent_config['GAMMA_DISCOUNTING_RATE']

		states,actions,rewards,next_states,players,dones = zip(*dataset)
		dones = array(dones)
		states = array(states)
		rewards = array(rewards)
		next_states = array(next_states)
		learning_rate = array([ Agent_config['LEARNING_RATE_RL_PLAYER'] if player \
		 						else Agent_config['LEARNING_RATE_RL']
								for player in players])

		for i in range(Agent_config['EPOCHS_RL_FIT']):
			print(myheader.format(i+1))
			print('Processing data...')
			now=time()
			predict_s = self.keras_NN_model.predict(states) # Actual prediction
			# Calculate new prediction
			Q_s_a = array([pred[action] for pred, action in zip(predict_s,actions)])
			Q_next = array(list(map(amax,self.keras_NN_model.predict(next_states))))
			news_Q = Q_s_a + learning_rate*(rewards - Q_s_a + dones*gamma*Q_next)
			# Replace new Q-value in predict_s
			for pred, act, new in zip(predict_s, actions, news_Q): pred[act] = new
			print('Data processed in {0:.2f}s'.format(time()-now))

			# Train the Neural Net with the state and news_rewards
			print('Fitting Keras model...')
			now=time()
			self.keras_NN_model.fit(states, predict_s,
				batch_size=Agent_config['BATCH_SIZE'],
				validation_split = Agent_config['VAL_SPLIT_FIT'],
				epochs=Agent_config['EPOCHS_FIT'],
				verbose=Agent_config['VERBOSE_FIT'],
				callbacks=[self.tbCallback])
			print('Keras model fited processed in {0:.2f}s'.format(time()-now))
