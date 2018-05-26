#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Module that contains the Double_Battle class.
This class is the principal class to execute a battle in the game.

It contains the following class:

	Double_Battle
"""

# Local imports
from Configuration.settings import Sentence, Display_Config, General_config
from Game.display.window import Window
from .core.pokemon import Pokemon
from .trainer import TrainerRandom
from .trainerInput import TrainerInput
from .attack import Attack
from Agent.agent_to_play import AgentPlay

__version__ = '0.7'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'


"""
	Class to make a double battle.
"""
class Double_Battle:
	"""
		Retuns the dafoauts arguments of de __int__ function as a dictionary.
		Use: Double_Battle(**default_argunents())
	"""
	@staticmethod
	def default_argunents():
		return {'const_A1': TrainerInput,  'poke_A1': None,
				'const_A2': TrainerRandom, 'poke_A2': None,
				'const_F1': TrainerRandom, 'poke_F1': None,
				'const_F2': TrainerRandom, 'poke_F2': None,
				'base_level': 50, 'varability_level': 50}

	def __init__(self, const_A1 = TrainerInput,  poke_A1 = None,
					   const_A2 = TrainerRandom, poke_A2 = None,
					   const_F1 = TrainerRandom, poke_F1 = None,
					   const_F2 = TrainerRandom, poke_F2 = None,
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
		if poke_A1==None:
			poke_A1 = Pokemon.Random(base_level, varability_level)
		trainerA1 = const_A1("Ally_0", poke_A1)
		if poke_A2==None:
			poke_A2 = Pokemon.Random(base_level, varability_level)
		trainerA2 = const_A2("Ally_1", poke_A2)
		if poke_F1==None:
			poke_F1 = Pokemon.Random(base_level, varability_level)
		trainerF1 = const_F1("Foe_0", poke_F1)
		if poke_F2==None:
			poke_F2 = Pokemon.Random(base_level, varability_level)
		trainerF2 = const_F2("Foe_1", poke_F2)

		self._trainers = [trainerA1,trainerA2,trainerF1,trainerF2]
		self.state = {t.role: t.pokemon() for t in self._trainers}
		self.state['use_agent'] = isinstance(trainerA2, AgentPlay)
		self.show_message = None
		self.n_turn = 0
		for t in self._trainers:
			t.set_state(self.state)
			if isinstance(t, TrainerInput):	self.show_message = t.show_message

	"""
		Function to play the battle
	"""
	def play(self):
		if General_config['BATTLE_VERBOSE']:
			print("-------------- NEW BATTLE --------------")
		self.show('START', *[t.pokemon().name() for t in self._trainers],\
					time=Display_Config['FIRST_TIME_STEP'])
		while not self.is_finished():
			if General_config['BATTLE_VERBOSE']:
				print("--------------- NEW TURN: {} ---------------".format(self.n_turn))
			self.doTurn()
		if General_config['BATTLE_VERBOSE']:
			print("------------- BATTLE ENDED -------------")
		self.show_result()


	"""
		Function to display a message
	"""
	def show(self, name, *args, time=Display_Config['TIME_STEP']):
		text = Sentence[name].format(*args)
		if General_config['BATTLE_VERBOSE']: print(text) # To have a "log" in terminal
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
			name_m = attack.move.name()
			self.show('USE_ATTACK', name_p, name_m, name_e)
			if eb.is_fainted(): self.show('TARGET_FAINTED', name_e)
			elif not attack.has_pp: self.show('NO_PP_LEFT', name_p, name_m)
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
		if self.is_finished():
			if self.winners() == None:
				self.show("DEAD_HEAT",time=Display_Config['LAST_TIME_STEP'])
			else:
				winners = [ tr.pokemon().name()
							for tr in self._trainers
							if not tr.pokemon().is_fainted()]
				if len(winners) == 2: self.show("WINNERS", *winners)
				if len(winners) == 1: self.show("WINNER", *winners)
				self.show("WIN" if self.winners() else "LOSE", \
							time=Display_Config['LAST_TIME_STEP'])

	"""
		Return True if the battle is finished, False otherwise.
		('' --> 'bool')
	"""
	def is_finished(self):
		#check only one team live
		fainteds = list(map(lambda tr:tr.pokemon().is_fainted(),self._trainers))
		end_battle = (fainteds[0] and fainteds[1]) or (fainteds[2] and fainteds[3])
		#check pp
		pk = list(map(lambda tr:tr.pokemon(),self._trainers))
		moves_can_not_use = [not m.can_use() for p in pk if not p.is_fainted() for m in p.moves()]
		dead_heat = all(moves_can_not_use) or self.n_turn>General_config['MAX_NUM_TURN']
		return end_battle or dead_heat


	"""
		Returns True if the battle is won by the Ally team, False if the battle
		is won by the Foe team, or None otherwise (also if had had a Dead Heat).
		('' --> 'bool')
	"""
	def winners(self):
		if self.is_finished():
			fainteds = list(map(lambda tr:tr.pokemon().is_fainted(),self._trainers))
			if (fainteds[0] and fainteds[1]) or (fainteds[2] and fainteds[3]):
				for tr in self._trainers:
					if not tr.pokemon().is_fainted(): return tr.is_ally()
			else: return None
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
			self.n_turn+=1
			# choice actions
			live_trainers = []
			last_choices = {}
			for trainer in self._trainers:
				if not trainer.pokemon().is_fainted():
					trainer.choice_action()
					last_choices[trainer.role]=trainer.raw_action()
					live_trainers.append(trainer)

			tr_sort = sorted(live_trainers, key=self.attack_order, reverse=True)
			last_attacks = {}

			# do actions
			for trainer in tr_sort:
				if self.is_finished(): break
				poke = trainer.pokemon()
				if not poke.is_fainted(): # If fainted during this turn
					move, target = trainer.action()
					pk_enemy = self._trainers[target].pokemon()
					attack = Attack(poke, pk_enemy, move)
					last_attacks[trainer.role]=attack
					self.show_attack(attack)

			#recive_results
			for trainer in self._trainers:
			    trainer.recive_results( last_attacks, last_choices,
			                            self.is_finished())
