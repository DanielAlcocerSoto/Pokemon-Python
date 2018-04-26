#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Module that contains the Agent, an extencion of Trainer class.
This classes is a test of use a RL method in Game.

It contains the following classes:

	Agent
"""

# Local import
from .agent_to_play import TrainerIA
from .model import Model

# General imports
from random import randint, random
from copy import deepcopy as copy

__version__ = '0.5'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'


file_model = "model_test"

"""
	Extended class from Trainer that use RL.
"""
class AgentTrain(TrainerIA):
	def __init__(self, role, pokemon, model = Model(),
				 epsilon_min = 0.01, epsilon_decay = 0.995):
		self.epsilon = 1.0  # exploration rate
		self.epsilon_min = epsilon_min
		self.epsilon_decay = epsilon_decay
		TrainerIA.__init__(self, role, pokemon, model)
		#self.replay() #to quick debug

	def set_state(self, state):
	    TrainerIA.set_state(self, state)
	    self.last_state = copy(state)

	def choice_action(self):
		if random() <= self.epsilon:
			self._idmove = randint(0, 3)
			self._target = randint(0, 1)
		else:
			TrainerIA.choice_action(self)

	def recive_results(self, attacks, done):
		state = self.last_state
		next_state = self.actual_state
		self.model.remember(state, self._idmove, self._target, \
							self.role, attacks, next_state, done)
		self.last_state = copy(self.actual_state)

	# train the agent with the experience of the episode and restart the agent
	def replay(self, pokemon):
		self.model.train()

		if self.epsilon > self.epsilon_min:
			self.epsilon *= self.epsilon_decay

		#reset trainer
		self._pk=pokemon

	def save_model(self):
		self.model.save(file_model)
