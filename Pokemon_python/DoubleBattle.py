#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Module
"""
from Pokemon_python.ClassesDB import Pokemon, Type, Move, possible_pokemons_names
from random import randint, uniform, choice
from math import floor
from Pokemon_python.Trainer import Trainer, TrainerRandom, ALLY, FOE
from Pokemon_python.TrainerInput import TrainerInput

__version__ = '0.4'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'

#prob between 0 and 100
def with_prob_of(prob):
	if prob == None: return True
	return uniform(0,100) < prob


class Attack:
	def __init__(self, poke_attacker, poke_defender, move, _USE_VARABILITY = True, _USE_CRITIC = True):
		self.USE_VARABILITY = _USE_VARABILITY
		self.USE_CRITIC = _USE_CRITIC

		move.use()
		self.calc_damage(poke_attacker, poke_defender, move)
		poke_defender.hurt(self.dmg)

	def calc_damage(self, poke_attacker, poke_defender, used_move):
		sp = 'special-' if used_move.damage_class() == 'special' else ''
		a = (0.2*poke_attacker.level()+1) * poke_attacker.get_stat(sp+'attack') * used_move.power()
		d = 25*poke_defender.get_stat(sp+'defense')
		typeMove = used_move.type()
		self.efectivity = typeMove.multiplier(poke_defender.types())
		bonification  = typeMove.bonification(poke_attacker.types())
		self.dmg = (a/d + 2) * self.efectivity * bonification

		#Randoms
		if self.USE_VARABILITY:
			varability = randint(85,100)
			self.dmg *=  (0.01*varability)
		if self.USE_CRITIC:
			self.is_critic =  with_prob_of(used_move.prob_critic())# (<) alway at least 0.01% of not critic
			if self.is_critic: self.dmg *= 1.5 #Gen VI

		self.dmg = floor(self.dmg)


class Double_Battle:
	def __init__(self, trainerA1=None, trainerA2=None, trainerF1=None, trainerF2=None, base_level = 50, varability_level = 5):
		list_poke = possible_pokemons_names()
		if trainerA1==None: trainerA1 = TrainerInput(ALLY, Pokemon(choice(list_poke), base_level + randint(-varability_level,varability_level)))
		if trainerA2==None: trainerA2 = TrainerRandom(ALLY,Pokemon(choice(list_poke), base_level + randint(-varability_level,varability_level)))
		if trainerF1==None: trainerF1 = TrainerRandom(FOE, Pokemon(choice(list_poke), base_level + randint(-varability_level,varability_level)))
		if trainerF2==None: trainerF2 = TrainerRandom(FOE, Pokemon(choice(list_poke), base_level + randint(-varability_level,varability_level)))
		self._trainers = [trainerA1,trainerA2,trainerF1,trainerF2]
		print('Start Battle: '+trainerA1.pokemon().name()+' and '+trainerA2.pokemon().name()+' vs. '+trainerF1.pokemon().name()+' and '+trainerF2.pokemon().name())

	def is_finished(self):
		fainteds = list(map(lambda tr: tr.pokemon().is_fainted(), self._trainers))
		return (fainteds[0] and fainteds[1]) or (fainteds[2] and fainteds[3])
	def winners(self):
		for tr in self._trainers:
			if not tr.pokemon().is_fainted(): return tr.is_ally()

	def attack_order(self, trainer):
		pk = trainer.pokemon()			# When two moves have the same priority,
		move, _ = trainer.action()		# the users' Speed statistics will determine
		priority = move.priority()		# which one is performed first in a battle
		return priority*1000 + pk.get_stat('speed')

	def generate_print_state(self):
		print('')
		self._state={}
		for i,trainer in enumerate(self._trainers):
			poke = trainer.pokemon()
			poke_info= {'pos': i%2,
						'ally':trainer.is_ally(),
						'lvl': poke.level(),
						'hp': poke.health(),
						'max_hp': poke.get_stat('hp'),
						'fained': poke.is_fainted()}

			types = poke.types()
			if len(types) == 2:
				str_types = types[0].name()+'/'+types[1].name()
				poke_info['types'] = [types[0].name(),types[1].name()]
			else:
				str_types =types[0].name()
				poke_info['types'] = [types[0].name()]

			team = 'Ally' if trainer.is_ally() else 'Foe'
			print(team+' '+str(i%2)+':\t'+str(poke.name())+' lvl:'+str(poke.level())+' ('+str_types+')')
			print('\tHP: '+str(poke.health())+'/'+str(poke.get_stat('hp')))

			self._state[poke.name()]=poke_info

	def doTurn(self):
		if not self.is_finished():
			self.generate_print_state()
			live_trainers = []
			for trainer in self._trainers:
				if not trainer.pokemon().is_fainted():
					trainer.choice_action(self._state)
					live_trainers.append(trainer)

			for trainer in sorted(live_trainers, key=self.attack_order, reverse=True):
				#dialog... x used a,,,,is efective.... (trainer. talk()???? not por los prints de battle)
				if not trainer.pokemon().is_fainted():#fainted during this turn
					move, target = trainer.action()
					pk_enemy = self._trainers[target].pokemon()
					print(trainer.pokemon().name()+' ha usado '+move.name()+' contra '+pk_enemy.name())
					if not pk_enemy.is_fainted():
						if with_prob_of(move.accuracy()):
							attack  = Attack(trainer.pokemon(), pk_enemy, move)
							trainer.set_last_attack(attack)
							if attack.efectivity == 4: print ('\tEs super efectivo')
							if attack.efectivity == 2: print ('\tEs muy efectivo')
							if attack.efectivity == 0.5: print ('\tEs poco efectivo')
							if attack.efectivity == 0.25: print ('\tEs muy poco efectivo')
							if attack.efectivity == 0: print ('\tNo es efectivo')
						else: print('\tEl ataque ha fallado')
					else : #auto cambiar objetivo???  util para la IA nop
						print('\t'+pk_enemy.name()+' ja estaba debilitado')



if __name__ == '__main__':
	"""
	a1=Attack(pk1,pk2,pk1.moves()[0])
	print('\nbulbasaur vs. charmander')
	print(a1.dmg)
	print(a1.is_critic)
	print(pk2.health())

	a2=Attack(pk2,pk1,pk2.moves()[0])
	print('\ncharmander vs. bulbasaur')
	print(a2.dmg)
	print(a2.is_critic)
	print(pk1.health())"""

	#tr0 = TrainerInput(ALLY, Pokemon('bulbasaur', 95))
	#tr2	= TrainerRandom(FOE, Pokemon('seadra',95))


	Battle = Double_Battle(base_level = 95)
	while(not Battle.is_finished()):
		Battle.doTurn()
	print('Allies win? '+str(Battle.winners()))
