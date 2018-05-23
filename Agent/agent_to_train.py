#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Module that contains the Agent, an extencion of Trainer class.
This classes can be used to train a model.

It contains the following classes:

	Agent
"""

# Local import
from Configuration.settings import Agent_config
from .agent_to_play import AgentPlay
from .model import Model

# General imports
from random import randint, random
from copy import deepcopy as copy

__version__ = '0.5'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'

"""
	Extended class from Trainer that use RL.
"""
class AgentTrain(AgentPlay):
	def __init__(self, role, pokemon, model):
		AgentPlay.__init__(self, role, pokemon, model)

	def set_state(self, state):
	    AgentPlay.set_state(self, state)
	    self.last_state = copy(state)

	#to train, exploration random
	def choice_action(self):
		self._idmove = randint(0, 3)
		self._target = randint(0, 1)

	def recive_results(self, attacks, done):
		state = self.last_state
		next_state = self.actual_state
		if not self.last_state[self.role].is_fainted():
			self.model.remember(state, self._idmove, self._target, \
								self.role, attacks, next_state, done)
		self.last_state = copy(self.actual_state)

	# train the agent with the experience of the episode and restart the agent
	def replay_and_train(self, pokemon):
		#reset trainer
		self._pk=pokemon
		self.model.replay_and_train()

	# Once finnished training, save the model ina file
	def save_model(self, model_name = None):
		self.model.save(model_name)
