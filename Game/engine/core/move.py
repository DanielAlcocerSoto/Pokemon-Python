#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Module that contains an extension of the 'Object_Info' class to manage the
information of the moves.

This module contains the following class:

	Move

"""

# Local imports
from Game.settings import Directory
from Game.utils_data_base import Object_Info
from .type import Type

__version__ = '1.0'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'


"""
	Class with information about a move.
"""
class Move(Object_Info):
	def __init__(self, name):
		"""
		Args:
			name ('str'): The name (key of the dictionary) of the move.

		Action:
			Create a Move with the information of 'name' move.
		"""
		Object_Info.__init__(self, name, Directory['MOVE_FILE'])
		self._pp = self._info['pp']
		self._type = Type(self._info['type'])

	"""
		Return the power of the move.
		('' --> 'int')
	"""
	def power(self):
		return self._info['power']

	"""
		Return the accuracy of the move.
		('' --> 'int')
	"""
	def accuracy(self):
		return self._info['accuracy']

	"""
		Return the priority of the move.
		('' --> 'int')
	"""
	def priority(self):
		return self._info['priority']

	"""
		Return the damage class of the move.
		('' --> 'str')
	"""
	def damage_class(self):
		return self._info['damage_class']

	"""
		Return the maximum of pp (Power Points) that have this move.
		('' --> 'int')
	"""
	def max_pp(self):
		return self._info['pp']

	"""
		Return the remaining pp of this move.
		('' --> 'int')
	"""
	def actual_pp(self):
		return self._pp

	"""
		Return the type of the move.
		('' --> 'class:Type')
	"""
	def type(self):
		return self._type

	"""
		Return the probability of this move to do a critic attack.
		('' --> 'int')
	"""
	def prob_critic(self): # Probabilities of Generation VII
		if   self._info['crit_rate'] == 0: return 4.167 #(1/24) * 100
		elif self._info['crit_rate'] == 1: return 12.5 #(1/8) * 100
		elif self._info['crit_rate'] == 2: return 50
		else: return 100

	"""
		Decrease the amount of pp of the move.
	"""
	def use(self):
		self._pp -= 1
		self._pp = max(self._pp,0)

	"""
		Return True if the move can be done, i.e. it still has pp.
		False otherwise.
		('' --> 'bool')
	"""
	def can_use(self):
		return 0 < self._pp
