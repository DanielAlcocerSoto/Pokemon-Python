#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Module that contains the Agent, an extencion of Trainer class.
This classes can be used to play Game with an expecific model.

It contains the following classes:

	Agent
"""

# Local imports
from Game.engine.trainer import Trainer

# General imports
from random import randint, random
from copy import deepcopy as copy

__version__ = '0.5'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'


"""
	Extended class from Trainer that use RL.
"""
class Agent(Trainer):
	def __init__(self, role, pokemon, model, train_mode=False):
		self.model = model
		self.train_mode = train_mode
		Trainer.__init__(self, role, pokemon)

	def set_state(self, state):
		self.actual_state = state
		if self.train_mode: self.last_state = copy(state)

	def _random_choise(self):
		return randint(0, 3),randint(0, 1)

	def _predict_choise(self):
		return self.model.predict(self.actual_state, self.role)

	def choice_action(self):
		if self.train_mode: self._idmove,self._target = self._random_choise()
		else:
			self._idmove, self._target = self._predict_choise()
			str = 'Agent {} choice action: ({},{})'
			print(str.format( self.role, self._idmove, self._target))

	def recive_results(self, attacks, choices, done):
		if self.train_mode:
			state = self.last_state
			next_state = self.actual_state
			self.model.remember(state,self.role,attacks,choices,next_state,done)
			self.last_state = copy(self.actual_state)
