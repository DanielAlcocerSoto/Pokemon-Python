#!/usr/bin/python3
"""
Module that contains the definition of the main classes
that contain information from the database
"""
from GeneratorDB import load_json, POKE_FILE, TYPE_FILE, MOVE_FILE
from random import randint, sample
from math import floor

__version__ = '0.7'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'


def possible_pokemons_names():
		return list(load_json(POKE_FILE).keys())


class Object_Info:
	def __init__(self, name, file):
		fileDict = load_json(file)
		self._keys = list(fileDict.keys())
		self._name = name
		if self._name in self._keys:
			self._info = fileDict[name]
		else : raise Exception('Name "'+name+'" does not exist in '+file)

	def name(self):
		return self._name


class Type(Object_Info):
	def __init__(self, name):
		Object_Info.__init__(self, name, TYPE_FILE)
		self._multiplierTo = {}
		for key in self._keys:
			if   key in self._info['no_damage_to']:     self._multiplierTo[key] = 0
			elif key in self._info['half_damage_to']:   self._multiplierTo[key] = 0.5
			elif key in self._info['double_damage_to']: self._multiplierTo[key] = 2
			else: self._multiplierTo[key] = 1

	def multiplier(self, listTypes):
		mult = 1
		for Type in listTypes: mult*=self._multiplierTo[Type._name]
		return mult
	def bonification(self, listTypes):
		if any([x._name==self._name for x in listTypes]): return 1.5
		else: return 1


class Move(Object_Info):
	def __init__(self, name):
		Object_Info.__init__(self, name, MOVE_FILE)
		self._pp = self._info['pp']
		self._type = Type(self._info['type'])

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

	def can_use(self):
		return 0 < self._pp


class Pokemon(Object_Info): 
	def __init__(self, name, level):
		Object_Info.__init__(self, name, POKE_FILE)
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



if __name__ == '__main__':

	print('bulbasaur:')
	pk1=Pokemon('bulbasaur',50)
	print(pk1.health())
	print(pk1.get_stat('attack'))
	print(pk1.moves()[0].name())

	print('\ncharmander:')
	pk2=Pokemon('charmander',50)
	print(pk2.health())
	print(pk2.get_stat('attack'))
	print(pk2.moves()[0].name())

	print('\nditto:')
	pk3=Pokemon('ditto',50)
	print(pk3.health())
	print(pk3.get_stat('attack'))
	for move in pk3.moves_can_use():
		print(move.name())

