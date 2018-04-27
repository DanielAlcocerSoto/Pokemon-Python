#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Module that contains the Double_Battle class.
This class is the principal class to execute a battle in the game.

It contains the following class:

	Double_Battle
"""

# Local imports
from Configuration.settings import Sentence, Display_Config
from Game.display.window import Window
from .core.pokemon import Pokemon
from .trainer import TrainerRandom
from .trainerInput import TrainerInput
from .attack import Attack

__version__ = '0.7'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'


"""
	Class to make a double battle.
"""
class Double_Battle:
	def __init__(self, constructor_trainerA1 = TrainerInput,
					   constructor_trainerA2 = TrainerRandom,
					   constructor_trainerF1 = TrainerRandom,
					   constructor_trainerF2 = TrainerRandom,
					   pokemon_trainerA1 = None,
					   pokemon_trainerA2 = None,
				   	   pokemon_trainerF1 = None,
					   pokemon_trainerF2 = None,
				 	   base_level = 50,
					   varability_level = 50):
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
		if pokemon_trainerA1==None:
			pokemon_trainerA1 = Pokemon.Random(base_level, varability_level)
		trainerA1 = constructor_trainerA1("Ally_0", pokemon_trainerA1)
		if pokemon_trainerA2==None:
			pokemon_trainerA2 = Pokemon.Random(base_level, varability_level)
		trainerA2 = constructor_trainerA2("Ally_1", pokemon_trainerA2)
		if pokemon_trainerF1==None:
			pokemon_trainerF1 = Pokemon.Random(base_level, varability_level)
		trainerF1 = constructor_trainerF1("Foe_0", pokemon_trainerF1)
		if pokemon_trainerF2==None:
			pokemon_trainerF2 = Pokemon.Random(base_level, varability_level)
		trainerF2 = constructor_trainerF2("Foe_1", pokemon_trainerF2)

		self._trainers = [trainerA1,trainerA2,trainerF1,trainerF2]
		self.state = {t.role: t.pokemon() for t in self._trainers}
		self.show_message = None
		for t in self._trainers:
			t.set_state(self.state)
			if isinstance(t, TrainerInput):	self.show_message = t.show_message

	"""
		Function to play the battle
	"""
	def play(self):
		print("-------------- NEW BATTLE --------------")
		self.show('START', *[t.pokemon().name() for t in self._trainers])
		while not self.is_finished():
			print("--------------- NEW TURN ---------------")
			self.doTurn()
		print("------------- BATTLE ENDED -------------")
		self.show_result()


	"""
		Function to display a message
	"""
	def show(self, name, *args, time=2):
		text = Sentence[name].format(*args)
		print(text) # To have a "log"
		if self.show_message != None: self.show_message(text,time)


	"""
		Function to display as a message the result of an attack
	"""
	def show_attack(self, attack):
		p = attack.poke_attacker
		if not p.is_fainted():
			eb = attack.poke_defender
			ea = attack.poke_defender_after
			name_p = p.name()
			name_e = eb.name()
			self.show('USE_ATTACK', name_p, attack.move.name(), name_e)
			if eb.is_fainted(): self.show('TARGET_FAINTED', name_e)
			elif attack.missed_attack: self.show('MISS_ATTACK', name_p)
			else: # Show results of the attack
				if   attack.efectivity == 4: self.show('EFECTIVITY_x4')
				elif attack.efectivity == 2: self.show('EFECTIVITY_x2')
				elif attack.efectivity == 0.5: self.show('EFECTIVITY_x05')
				elif attack.efectivity == 0.25: self.show('EFECTIVITY_x025')
				elif attack.efectivity == 0: self.show('EFECTIVITY_x0')
				if attack.is_critic: self.show('CRITIC_ATTACK')
				if ea.is_fainted(): self.show('DEAD_POKEMON', name_e)

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
		fainteds = list(map(lambda tr:tr.pokemon().is_fainted(),self._trainers))
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
			# choice actions
			live_trainers = []
			for trainer in self._trainers:
				if not trainer.pokemon().is_fainted():
					trainer.choice_action()
					live_trainers.append(trainer)

			tr_sort = sorted(live_trainers, key=self.attack_order, reverse=True)
			self.last_attacks = {}

			# do actions
			for trainer in tr_sort:
				if self.is_finished(): break
				poke = trainer.pokemon()
				if not poke.is_fainted(): # If fainted during this turn
					move, target = trainer.action()
					pk_enemy = self._trainers[target].pokemon()
					attack = Attack(poke, pk_enemy, move)
					self.last_attacks[trainer.role]=attack
					self.show_attack(attack)
