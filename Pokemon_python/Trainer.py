#!/usr/bin/python3
"""
Module
"""
from ClassesDB import Pokemon
from random import randint

__version__ = '0.4'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'

ALLY = True
FOE = False

class Trainer:
	def __init__(self, team, pokemon):
		self._team=team
		self._pk = pokemon

	def pokemon(self):
		return self._pk

	def set_last_attack(self, attack):
		self._attack=attack
	def last_attack(self):
		return self._attack

	def is_ally(self):
		return self._team == ALLY

	def num_moves_can_use(self):
		return len(self._pk.moves_can_use())

	def action(self):
		target = self._target + 2 if self.is_ally() else self._target
		return (self._pk.moves_can_use()[self._idmove], target)
	def choice_action(self, info):
		""" 
		Args:
			state (dict??/obj): contains information about the current state of the game.
		Action:
			set the value of the attribute self._idmove [0, self.num_moves_can_use()-1]
			and the value of the attribute self._target [0, 1], 
			which represents the action that the trainer will perform on next turn.
		"""
		raise NotImplementedError


class TrainerRandom(Trainer):
	def choice_action(self, info): 
		self._idmove = randint(0, self.num_moves_can_use()-1)
		self._target = randint(0, 1)
