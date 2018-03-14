
#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Module that contains the Agent, an extencion of Trainer class.
This classes is a test of use a RL method in Game.

It contains the following classes:

	Agent
"""

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
	def __init__(self, model_file=None, gama = 0.95):
		self.gamma = gama   # discount rate
		if model_file == None: self.model = self._build_model()
		else: self.model = load_model(model_path+model_file+'.h5')

	def save(self, model_file):
		self.model.save(model_path+model_file+'.h5')

	def _build_model(self, learning_rate = 0.001, state_size = 45):
		# Neural Net for Deep-Q learning Model
		# Sequential() creates the foundation of the layers.
		model = Sequential()
		# 'Dense' is the basic form of a neural network layer
		# Input Layer of state size(4) and Hidden Layer with 24 nodes
		model.add(Dense(24, input_dim=state_size, activation='relu'))
		# Hidden layer with 24 nodes
		model.add(Dense(24, activation='relu'))
		# Output Layer with # of actions: 8 nodes (left, right)
		model.add(Dense(4*2, activation='linear'))
		# Create the model based on the information above
		model.compile(loss='categorical_crossentropy',
		              optimizer=Adam(lr=learning_rate))
		return model

	def _calc_reward(self, my_role, attacks):
		# TODO self.actual_state
		if my_role in attacks.keys():
			attack=attacks[my_role]
			return attack.dmg
		else: return 0

	def _poke_to_list(self, poke): #'6'+2+3 =11
		n = ["hp", "attack", "special-attack", "defense", \
			 "special-defense", "speed"]
		stats = [poke.get_stat(s) for s in n]
		types = [t.name() for t in poke.types()]
		if len(types)==1:types.append('-')
		return stats+types+[poke.health(),poke.level(),poke.is_fainted()]

	def _move_to_list(self, move): #3
		return [move.type().name(), move.actual_pp(), move.power()]

	def _encode_state(self, state):# 3*4 + 11*3
		#TODO  index-->value
		#my_pokemon_data
		ret = self._poke_to_list(state['Ally_1'])
		moves=state['Ally_1'].moves()
		for i in range(4):
			if i < len(moves): ret+= self._move_to_list(moves[i])
			else: ret+= ['-']*3#numero_de_datos_de_move
		for j in range(2):
			ret+=self._poke_to_list(state['Foe_'+str(j)])
		# enemies_data
		return ret

	def _encode_action(self,move, target):
		return target*4 + move

	def _decode_action(self, action):
		return action%4, action//4,

	def remember(self, state, move, target, my_role, attacks, next_state, done):
		state = self._encode_state(state)
		action = self._encode_action(move, target)
		reward = self._calc_reward(my_role, attacks)
		next_state = self._encode_state(next_state)
		#save
		obj = (state, action, reward, next_state, done)
		with open(file_log+'.csv', 'a') as csv_file:
			writer = csv.writer(csv_file)
			writer.writerow(obj)

	def predict(self, state):
		#predic 1 action with 1 state of 10 elemens
		state = array([self._encode_state(state)])
		act_values = self.model.predict(state)
		action = argmax(act_values[0])
		return self._decode_action(action)

	def _load(self):
		df = read_csv(file_log+'.csv', delimiter=',', header=None)
		ret = [ array (
				[literal_eval(field) if isinstance(field, str) else field
				 for field in row]
				) for row in df.values]
		return ret

	# train the agent with the experience of the episode
	def train(self,	batch_size = 32):
		memory = self._load()
		minibatch = sample(memory,  min(len(memory), batch_size))
		# Extract informations from each memory

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
			self.model.fit(state, target_f, epochs=1, verbose=0)

		"""
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
		self.model.fit(states, target_f, epochs=1, verbose=0)
		"""
