#!/usr/bin/python3
"""
Module to
"""
from pokeAPI import load_json, print_dict, POKE_FILE, TYPE_FILE, MOVE_FILE
from random import randint, uniform, sample
from math import floor

__version__ = '0.7'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'

class Type:
	def __init__(self, name):
		self.name = name
		typesInfo = load_json(TYPE_FILE)
		self._info = typesInfo[name]
		self.multiplierTo = {}
		for key in typesInfo.keys():
			if key in self._info['no_damage_to']: self.multiplierTo[key] = 0
			elif key in self._info['half_damage_to']: self.multiplierTo[key] = 0.5
			elif key in self._info['double_damage_to']: self.multiplierTo[key] = 2
			else: self.multiplierTo[key] = 1

	def getMultiplierTo(self, listTypes):
		mult = 1
		for Type in listTypes: mult*self.multiplierTo[Type.name]
		return mult
	def getBonification(self, listTypes):
		if any([x.name==self.name for x in listTypes]): return 1.5
		else: return 1

class Move:
	def __init__(self, name):
		self.name = name
		self._info = load_json(MOVE_FILE)[name]
		self._pp = self._info['pp']
		self._type = Type(self._info['type'])

	def get_power(self):
		return self._info['power']
	def get_max_pp(self):
		return self._info['pp']
	def get_act_pp(self):
		return self._pp
	def get_type(self):
		return self._type
	def get_accuracy(self):
		return self._info['accuracy']
	def get_priority(self):
		return self._info['priority']
	def get_damage_class(self):
		return self._info['damage_class']
	def prob_critic(self): #GenVII
		if self._info['crit_rate'] == 0: return 0.0416667 #(1/24)
		elif self._info['crit_rate'] == 1: return 0.125 #(1/8)
		elif self._info['crit_rate'] == 2: return 0.5
		else: return 1

	def use(self):
		self._pp-=1
	def can_use(self):
		return 0 < self._pp

class Pokemon: 
	def __init__(self, name, level):
		self.name = name
		self.level= level
		self._info = load_json(POKE_FILE)[name]
		self._types = [Type(x) for x in self._info['types']]
		self._moves = [Move(x) for x in sample(self._info['moves'],4)]
		self._stats = self._info['stats']
		for stat in self._stats.values():
			stat['individual_value'] = randint(0, 31)
		self._Health = self.get_Stat('hp')

	def get_Stat(self, name): # "hp", "attack", "special-attack", "defense", "special-defense", "speed"
		#PS: 10 + { Nivel / 100 x [ (Stat Base x 2) + IV + PE/4 ] } + Nivel
		#OTHER:( 5 + { Nivel / 100 x [ (Stat Base x 2) + IV + PE/4 ] } ) x "Naturaleza" --> no usado
		st = self._stats[name]
		precalc = floor(self.level/100 *( (st['base_stat']*2) + st['individual_value'] + floor(st['effort']/4) ))
		if name == 'hp': return precalc + self.level + 10 
		else: return precalc + 5

	def get_Health(self):
		return self._Health

	def hurt(self, damage):
		self._Health -= damage
		return self.is_fainted()

	def is_fainted(self):
		return self._Health <=0

	def getTypes(self):
		return self._types

	def getMoves(self):
		return self._moves

	def useAtack(self, id_atack):
		move = self._moves[id_atack]
		move.use()
		return move


class Atack:	
	def __init__(self, poke_attacker, poke_defender, id_atack, _USE_VARABILITY = True, _USE_CRITIC = True):
		self.USE_VARABILITY = _USE_VARABILITY
		self.USE_CRITIC = _USE_CRITIC

		used_move = poke_attacker.useAtack(id_atack) 
		self.calc_damage(poke_attacker, poke_defender, used_move)
		poke_defender.hurt(self.dmg)

	def calc_damage(self,poke_attacker, poke_defender, used_move):
		sp = 'special-' if used_move.get_damage_class() == 'special' else ''
		a = (0.2*poke_attacker.level+1) * poke_attacker.get_Stat(sp+'attack') * used_move.get_power()
		d = 25*poke_defender.get_Stat(sp+'defense')
		typeMove = used_move.get_type()
		efectivity = typeMove.getMultiplierTo(poke_defender.getTypes())
		bonification  = typeMove.getBonification(poke_attacker.getTypes())
		self.dmg = (a/d + 2) * efectivity * bonification

		if self.USE_VARABILITY:
			varability = randint(85,100)
			self.dmg *=  (0.01*varability) 
		if self.USE_CRITIC: 
			self.is_critic = uniform(0,1) < used_move.prob_critic()# (<) alway at least 0.01% of not critic
			if self.is_critic: self.dmg *= 1.5 #Gen VI

		self.dmg = floor(self.dmg)






if __name__ == '__main__':

	print('bulbasaur:')
	pk1=Pokemon('bulbasaur',50)
	print(pk1.get_Health())
	print(pk1.get_Stat('attack'))
	print(pk1.getMoves()[0].name)

	print('\ncharmander:')
	pk2=Pokemon('charmander',50)
	print(pk2.get_Health())
	print(pk2.get_Stat('attack'))
	print(pk2.getMoves()[0].name)

	a1=Atack(pk1,pk2,0)
	print('\nbulbasaur vs. charmander')
	print(a1.dmg)
	print(a1.is_critic)
	print(pk2.get_Health())

	a2=Atack(pk2,pk1,0)
	print('\ncharmander vs. bulbasaur')
	print(a2.dmg)
	print(a2.is_critic)
	print(pk1.get_Health())