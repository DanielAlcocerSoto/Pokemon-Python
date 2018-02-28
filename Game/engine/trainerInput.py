#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Module that implements a trainer that choice its action from a input of a real
user. In this case is from a graphic interface (class:Window).

It contains the following class:

	TrainerInput
"""

# Local imports
from .trainer import Trainer

__version__ = '0.5'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'


"""
	Extended class from Trainer that implements the choice_action function and
	allows to choose the action through the graphic input.
"""
class TrainerInput(Trainer):
	"""
		Set the windows where is displayed the battle.
	"""
	def set_input_method(self, window):
		"""
			Args:
				window (class:'Window'): The windows where is displayed the
										 battle.

			Action:
				Set the windows where is displayed the battle.
		"""
		self.window = window

	"""
		Implementation of choice_action funcion of the Trainer class
	"""
	def choice_action(self):
		self.window.show("ASK_MOVE",self._pk.name(),time=0)
		self._idmove, self._target = self.window.get_action()
