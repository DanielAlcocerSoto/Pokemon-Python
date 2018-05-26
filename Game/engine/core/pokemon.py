#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Module that contains an extension of the 'Object_Info' class to manage the
information of the pokemons.

This module contains the following class:

	Pokemon

"""

# Local imports
from Configuration.settings import Directory, General_config, Attack_Config
from .object_info import Object_Info, load_info
from .type import Type
from .move import Move

# General imports
from random import randint, sample, choice
from math import floor

__version__ = '0.9'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'

"""
	Class with information about a pokemon.
"""
class Pokemon(Object_Info):
	"""
		Retuns a random pokemon with level = base_level +-varability_level.
	"""
	@staticmethod
	def Random(base_level = 50, varability_level = 50):
		"""
			Args:
				base_level ('int'): Base level to apply varaiability.
				varability_level ('int'): The varaiability of the base level.

			Return (class:'Pokemon'):
				Random pokemon with level between base_level-varability_level
				and base_level+varability_level.
		"""
		lvl = base_level + randint(-varability_level,varability_level)
		return Pokemon(choice(Pokemon.possible_names()), lvl)

	"""
		Returns the name of all pokemons in the database.
	"""
	@staticmethod
	def possible_names(generations=General_config['GENERATIONS']):
		"""
			Args: -

			Return ('list of str'):
				The name (key) of all the pokemons in the database.
		"""
		all_poke_name =list(load_info(Directory['POKE_FILE']).keys())
		possible_names = []
		for gen in generations:
			if gen == 1: first_p = 0
			else: first_p = General_config['END_GEN_{}'.format(gen-1)]
			last_p = General_config['END_GEN_{}'.format(gen)]
			possible_names += all_poke_name[first_p:last_p]
		return possible_names

	def __init__(self, name, level):
		"""
			Args:
				name ('str'): The name (key of the dictionary) of the pokemon.

			Action:
				Create a Pokemon with the information of 'name' pokemon.
		"""
		Object_Info.__init__(self, name, Directory['POKE_FILE'])
		self._level= min(max(level,1),100)
		self._types = [Type(x) for x in self._info['types']]
		self._moves = [Move(x) for x in sample(self._info['moves'], 4)]
		self._stats = self._info['stats']
		for stat in self._stats.values():
			if Attack_Config['USE_IV']: 
				stat['individual_value'] = randint(0, 31)
			else:
				stat['individual_value'] = 15
		self._health = self.get_stat('hp')

	"""
		Returns the final value of a statistic.
	"""
	def get_stat(self, stat):
		"""
			Args:
				stat ('str'): The name of the stadistic that you want to obtain.
					Note: Possible names: "hp", "attack", "special-attack",
										  "defense", "special-defense", "speed"

			Returns ('int'):
				The final value of the 'stat' stadistic
		"""
		n= ["hp", "attack", "special-attack", "defense", \
			"special-defense", "speed"]
		if stat in n:
			# Formulas:
			# PS: 10 + { Nivel / 100 x [ (Stat Base x 2) + IV + PE/4 ] } + Nivel
			# OTHER:( 5 + { Nivel / 100 x [ (Stat Base x 2) + IV + PE/4 ] } )
			#		x "Naturaleza" --> not used/ not implemented
			st = self._stats[stat]
			precalc = st['individual_value'] + floor(st['effort']/4)
			precalc = st['base_stat']*2 + precalc
			precalc = floor(self._level/100 * precalc)
			if stat == 'hp': return precalc + self._level + 10
			else: return precalc + 5
		else: return None

	"""
		Return the actual health of this pokemon.
		('' --> 'int')
	"""
	def health(self):
		return self._health

	"""
		Return the level of this pokemon.
		('' --> 'int')
	"""
	def level(self):
		return self._level

	"""
		Return True if the pokemon is fainted, False otherwise.
		('' --> 'bool')
	"""
	def is_fainted(self):
		return self._health <=0

	"""
		Return the types of this pokemon.
		('' --> 'list of class:Type')
	"""
	def types(self):
		return self._types

	"""
		Return the moves of this pokemon.
		('' --> 'list of class:Moves')
	"""
	def moves(self): #use for get info
		return self._moves

	"""
		Function to hurt the pokemon.
	"""
	def hurt(self, damage):
		"""
			Args:
				damage ('int'): Amount of health to decrease.

			Action:
				Decrease the healt of the pokemon in 'damage' healts points.
		"""
		self._health -= damage
		if self.is_fainted(): self._health=0

	"""
		Return the name file where the sprit is.
	"""
	def sprite(self, is_ally):
		"""
			Args:
				is_ally ('bool'): The team to which the pokemon belongs.
					Note: If 'is_ally' id True, this function return the back
						  sprite, and if is False return the front sprite.

			Return (str):
				The name of the image file where the sprite is.
		"""
		name = 'back' if is_ally else 'front'
		return self._info['sprites'][name]
