#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Module that contains the Agent, an extencion of Trainer class.
This classes is a test of use a RL method in Game.

It contains the following classes:

	Agent
"""

# Local imports
from Game.engine.trainer import Trainer

__version__ = '0.5'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'



memory = "RL/Data/log"

"""
	Extended class from Trainer that use RL.
"""
class TrainerIA(Trainer):
	def __init__(self, role, pokemon, model):
		self.model = model
		Trainer.__init__(self, role, pokemon)

	def set_state(self, state):
	    self.actual_state = state

	def choice_action(self):
		self._idmove, self._target = self.model.predict(self.actual_state)
