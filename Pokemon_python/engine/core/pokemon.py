#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

"""

from Pokemon_python.utils_data_base import Object_Info, load_json
from Pokemon_python.sittings import Directory
from .move import Move
from .type import Type

from random import randint, sample
from math import floor

__version__ = '1.0'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'


def possible_pokemons_names():
		return list(load_json(Directory['POKE_FILE']).keys())

class Pokemon(Object_Info):
	def __init__(self, name, level):
		Object_Info.__init__(self, name, Directory['POKE_FILE'])
		self._level= max(min(level,100),1)
		self._types = [Type(x) for x in self._info['types']]
		self._moves = [Move(x) for x in sample(self._info['moves'],min(4,len(self._info['moves'])))]
		self._stats = self._info['stats']
		for stat in self._stats.values():
			stat['individual_value'] = randint(0, 31)
		self._health = self.get_stat('hp')

	def get_stat(self, stat): # "hp", "attack", "special-attack", "defense", "special-defense", "speed"
		#PS: 10 + { Nivel / 100 x [ (Stat Base x 2) + IV + PE/4 ] } + Nivel
		#OTHER:( 5 + { Nivel / 100 x [ (Stat Base x 2) + IV + PE/4 ] } ) x "Naturaleza" --> no usado
		st = self._stats[stat]
		precalc = floor(self._level/100 * ((st['base_stat']*2) + st['individual_value'] + floor(st['effort']/4)))
		if stat == 'hp': return precalc + self._level + 10
		else: return precalc + 5

	def health(self):
		return self._health
	def level(self):
		return self._level
	def types(self):
		return self._types
	def moves(self): #use for get info
		return self._moves
	def moves_can_use(self): #use for get moves to use
		ret = [move for move in self._moves if move.can_use()]
		if len(ret) == 0 : return [Move('struggle')]
		else: return ret

	def is_fainted(self):
		return self._health <=0

	def hurt(self, damage):
		self._health -= damage
		if self.is_fainted(): self._health=0
