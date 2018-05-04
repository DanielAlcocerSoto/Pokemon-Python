#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Module that implements a trainer that choice its action from a input of a real
user. In this case is from a graphic interface (class:Window).

It contains the following class:

	TrainerInput
"""

# Local imports
from Configuration.settings import Sentence
from Game.display.window import Window
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
	def set_state(self, state): # only once time
		"""
			Args:
				window (class:'Window'): The windows where is displayed the
										 battle.

			Action:
				Set the windows where is displayed the battle.
		"""
		self.window = Window(state)
		self.show_message = self.window.show

	"""
		Implementation of choice_action funcion of the Trainer class
	"""
	def choice_action(self):
		self.window.show(Sentence["ASK_MOVE"].format(self._pk.name()),\
						time_display=0)
		self._idmove, self._target = self.window.get_action()
