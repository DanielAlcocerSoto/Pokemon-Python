#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

"""

from .trainer import Trainer

__version__ = '0.5'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'


class TrainerInput(Trainer):
	def set_input_method(self, window):
		self.window = window

	def choice_action(self):
		self.window.show("ASK_MOVE",self._pk.name(),time=0)
		self._idmove, self._target = self.window.get_action()
