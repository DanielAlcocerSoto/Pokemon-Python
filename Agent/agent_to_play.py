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

__version__ = '0.5'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'


"""
	Extended class from Trainer that use RL.
"""
class AgentPlay(Trainer):
	def __init__(self, role, pokemon, model):
		self.model = model
		Trainer.__init__(self, role, pokemon)

	def set_state(self, state):
	    self.actual_state = state

	def choice_action(self):
		self._idmove, self._target = self.model.predict(self.actual_state, self.role)
		print('Agent {} choice action: ({},{})'.format( self.role, self._idmove,
		 												self._target))
