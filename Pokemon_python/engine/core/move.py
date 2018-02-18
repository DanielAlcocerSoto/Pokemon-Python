#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Module that contains the move class
"""

from Pokemon_python.utils_data_base import Object_Info
from Pokemon_python.sittings import Directory
from .type import Type

__version__ = '1.0'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'

class Move(Object_Info):
	def __init__(self, name):
		Object_Info.__init__(self, name, Directory['MOVE_FILE'])
		self._pp = self._info['pp']
		self._type = Type(self._info['type'])

	def name(self):
		return  self._info['es_name']
	def power(self):
		return self._info['power']
	def accuracy(self):
		return self._info['accuracy']
	def priority(self):
		return self._info['priority']
	def damage_class(self):
		return self._info['damage_class']
	def max_pp(self):
		return self._info['pp']
	def actual_pp(self):
		return self._pp
	def type(self):
		return self._type

	def prob_critic(self): #GenVII
		if   self._info['crit_rate'] == 0: return 4.167 #(1/24) * 100
		elif self._info['crit_rate'] == 1: return 12.5 #(1/8) * 100
		elif self._info['crit_rate'] == 2: return 50
		else: return 100

	def use(self):
		self._pp-=1
		self._pp = max(self._pp,0)

	def can_use(self):
		return 0 < self._pp
