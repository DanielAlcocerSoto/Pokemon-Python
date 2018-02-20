#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

"""

from .core.pokemon import Pokemon, possible_pokemons_names
from .core.type import Type
from .core.move import Move
from .trainer import TrainerRandom, ALLY, FOE
from .trainerInput import TrainerInput

from random import randint, uniform, choice
from math import floor

from Pokemon_python.sittings import Display_Config
from Pokemon_python.display.window import Window

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
	def __init__(self, trainerA1=None, trainerA2=None, trainerF1=None, trainerF2=None, base_level = 50, varability_level = 50,):
		list_poke = possible_pokemons_names()
		if trainerA1==None: trainerA1 = TrainerInput(ALLY, Pokemon(choice(list_poke), base_level + randint(-varability_level,varability_level)))
		if trainerA2==None: trainerA2 = TrainerRandom(ALLY,Pokemon(choice(list_poke), base_level + randint(-varability_level,varability_level)))
		if trainerF1==None: trainerF1 = TrainerRandom(FOE, Pokemon(choice(list_poke), base_level + randint(-varability_level,varability_level)))
		if trainerF2==None: trainerF2 = TrainerRandom(FOE, Pokemon(choice(list_poke), base_level + randint(-varability_level,varability_level)))
		self._trainers = [trainerA1,trainerA2,trainerF1,trainerF2]
		self.state = {
				Display_Config["Ally_0"]:trainerA1.pokemon(),
				Display_Config["Ally_1"]:trainerA2.pokemon(),
				Display_Config["Foe_0"]:trainerF1.pokemon(),
				Display_Config["Foe_1"]:trainerF2.pokemon()
				}
		self.window = Window(self.state)
		trainerA1.set_input_method(self.window)
		#self.window.show('START', [t.pokemon().name() for t in self._trainers])

	def show_result(self):
		if self.is_finished:
			winners = [tr.pokemon().name() for tr in self._trainers if not tr.pokemon().is_fainted()]
			if len(winners) == 2: self.window.show("WINNERS", winners)
			if len(winners) == 1: self.window.show("WINNER", winners)
			self.window.show("WIN" if self.winners() else "LOSE", time=5)
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

	def doTurn(self):
		if not self.is_finished():
			self.window.visualize()
			live_trainers = []
			for trainer in self._trainers:
				if not trainer.pokemon().is_fainted():
					trainer.choice_action()
					live_trainers.append(trainer)

			for trainer in sorted(live_trainers, key=self.attack_order, reverse=True):
				#dialog... x used a,,,,is efective.... (trainer. talk()???? not por los prints de battle)
				if self.is_finished(): break
				poke = trainer.pokemon()
				if not poke.is_fainted():#fainted during this turn
					move, target = trainer.action()
					pk_enemy = self._trainers[target].pokemon()
					self.window.show('USE_ATTACK',[poke.name(),move.name(),pk_enemy.name()])
					if not pk_enemy.is_fainted():
						if with_prob_of(move.accuracy()):
							attack  = Attack(poke, pk_enemy, move)
							trainer.set_last_attack(attack)
							if attack.efectivity == 4:		self.window.show('EFECTIVITY_x4')
							if attack.efectivity == 2:		self.window.show('EFECTIVITY_x2')
							if attack.efectivity == 0.5: 	self.window.show('EFECTIVITY_x05')
							if attack.efectivity == 0.25: 	self.window.show('EFECTIVITY_x025')
							if attack.efectivity == 0:		self.window.show('EFECTIVITY_x0')
							if attack.is_critic:			self.window.show('CRITIC_ATTACK')
							if pk_enemy.is_fainted(): 		self.window.show('DEAD_POKEMON',[pk_enemy.name()])
						else: self.window.show('MISS_ATTACK',poke.name())
					else : #auto cambiar objetivo???  util para la IA nop
						self.window.show('TARGET_FAINTED',[pk_enemy.name()])

		self.window.visualize()
