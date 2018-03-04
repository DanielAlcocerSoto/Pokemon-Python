#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Module that contains the Double_Battle class.
This class is the principal class to execute a battle in the game.

It contains the following class:

	Double_Battle
"""

# Local imports
from Game.settings import Display_Config
from Game.display.window import Window
from .core.pokemon import Pokemon, possible_pokemons_names
from .trainer import TrainerRandom, ALLY, FOE
from .trainerInput import TrainerInput
from .attack import Attack

# General imports
from random import randint, choice

__version__ = '0.7'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'


"""
	Class to make a double battle.
"""
class Double_Battle:
	def __init__(self, trainerA1 = None, trainerA2 = None,
					   trainerF1 = None, trainerF2 = None,
				 	   base_level = 50, varability_level = 50):
		"""
			Args:
				trainerA1 (class:'Trainer'): The allied trainer 1 (the user's
											 trainer).
				trainerA2 (class:'Trainer'): The allied trainer 2.
				trainerF1 (class:'Trainer'): The enemy trainer 1.
				trainerF2 (class:'Trainer'): The enemy trainer 2.
					Note: If any of the trainer is not provided, a TrainerRandom
					 	  will be generated with a random Pokémon, except if
						  trainerA1 is missing. In this case, a TrainerInput is
						  created with a random pokemon.
				base_level ('int'): The base level of the pokemons if necessary
				  					to create them.
				varability_level ('int'): The varaiability of the base level of
										  the pokemons if necessary to create
										  them.

			Action:
				Create and execute the attack and save relevant information
				about it.
		"""
		list_poke = possible_pokemons_names()
		if trainerA1==None:
			lvl = base_level + randint(-varability_level,varability_level)
			trainerA1 = TrainerInput(ALLY, Pokemon(choice(list_poke), lvl))
		if trainerA2==None:
			lvl = base_level + randint(-varability_level,varability_level)
			trainerA2 = TrainerRandom(ALLY,Pokemon(choice(list_poke), lvl))
		if trainerF1==None:
			lvl = base_level + randint(-varability_level,varability_level)
			trainerF1 = TrainerRandom(FOE, Pokemon(choice(list_poke), lvl))
		if trainerF2==None:
			lvl = base_level + randint(-varability_level,varability_level)
			trainerF2 = TrainerRandom(FOE, Pokemon(choice(list_poke), lvl))

		self._trainers = [trainerA1,trainerA2,trainerF1,trainerF2]
		self.state = {
				"Ally_0": trainerA1.pokemon(),
				"Ally_1": trainerA2.pokemon(),
				"Foe_0":  trainerF1.pokemon(),
				"Foe_1":  trainerF2.pokemon()
				}
		for t in self._trainers:
			t.set_state(self.state)
			if isinstance(t, TrainerInput):
				self.show = t.show
				self.show_attack = t.show_attack

		self.show('START', *[t.pokemon().name() for t in self._trainers])

	"""
		Function to show the result of the battle if the battle is finished.
	"""
	def show_result(self):
		if self.is_finished:
			winners = [ tr.pokemon().name()
						for tr in self._trainers
						if not tr.pokemon().is_fainted()]
			if len(winners) == 2: self.show("WINNERS", *winners)
			if len(winners) == 1: self.show("WINNER", *winners)
			self.show("WIN" if self.winners() else "LOSE", time=5)

	"""
		Return True if the battle is finished, False otherwise.
		('' --> 'bool')
	"""
	def is_finished(self):
		fainteds = list(map(lambda tr: tr.pokemon().is_fainted(), self._trainers))
		return (fainteds[0] and fainteds[1]) or (fainteds[2] and fainteds[3])

	"""
		Returns True if the battle is won by the Ally team, False if the battle
		is won by the Foe team, or None otherwise.
		('' --> 'bool')
	"""
	def winners(self):
		if self.is_finished:
			for tr in self._trainers:
				if not tr.pokemon().is_fainted(): return tr.is_ally()
		else: return None

	"""
		Function to obtain the priority of a trainer depending on the selected
		action and the speed of its pokemon.
		(class:'Trainer' --> 'int')
	"""
	def attack_order(self, trainer):
		pk = trainer.pokemon()		# When two moves have the same priority,
		move, _ = trainer.action()	# the users' Speed statistics will determine
		priority = move.priority()	# which one is performed first in a battle
		return priority*1000 + pk.get_stat('speed')

	"""
		Function to do a turn, i.e. Ask for an action (choice_action function)
		for each trainer, and execute the action in the corresponding order.
	"""
	def doTurn(self):
		if not self.is_finished():
			live_trainers = []
			# choice actions
			for trainer in self._trainers:
				if not trainer.pokemon().is_fainted():
					trainer.choice_action()
					live_trainers.append(trainer)

			tr_sort = sorted(live_trainers, key=self.attack_order, reverse=True)
			attacks = []
			# do actions
			for trainer in tr_sort:
				if self.is_finished(): break
				poke = trainer.pokemon()
				if not poke.is_fainted(): # If fainted during this turn
					move, target = trainer.action()
					pk_enemy = self._trainers[target].pokemon()
					if not pk_enemy.is_fainted():
						attack = Attack(poke, pk_enemy, move)
						attacks.append(attack)
						self.show_attack(attack)

			#recive_results
			for trainer in live_trainers:
				trainer.recive_results(attacks)
