#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Module that contains the Trainer and the TrainerRandom classes.
This classes are used to set the acctions that will be made by the pokemon.

It contains the following classes:

	Trainer
	TrainerRandom
"""

# Local imports
from .core.pokemon import Pokemon

# General imports
from random import randint

__version__ = '1.0'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'


"""
	Generic trainer with basic funcions.
"""
class Trainer:
	def __init__(self, role, pokemon):
		"""
			Args:
				role ('str'): The role of this trainer
							  [Ally_0,Ally_1,Foe_0,Foe_1]
				pokemon (class:'Pokemon'): The Pokemon of the trainer.

			Action:
				Create a 'Trainer' of the team 'team' with a pokemon 'pokemon'.
		"""
		self.role= role
		self._pk = pokemon

	"""
		Return the pokemon of the trainer.
		('' --> class:'Pokemon')
	"""
	def pokemon(self):
		return self._pk

	"""
		Return True if the trainer is in the Ally team.
		('' --> 'bool')
	"""
	def is_ally(self):
		return "A" in self.role

	"""
		Return the ally role.
		('' --> 'str')
	"""
	def ally_role(self):
		r = self.role.split('_')
		return r[0]+'_'+str((int(r[1])+1)%2)

	"""
		Return the actual _idmove and _target.
	"""
	def raw_action(self):
		"""
			Args: -

			Return  (class:'int', 'int'):
				The actual row action.
		"""
		return self._idmove, self._target
	"""
		Return the action setted using the choice_action function.
	"""
	def action(self):
		"""
			Args: -

			Return  (class:'Move', 'int'):
				The move object of the choiced move, and the index of the target.
		"""
		target = self._target + 2 if self.is_ally() else self._target
		return (self._pk.moves()[self._idmove], target)

	"""
		Set the next action that the pokemon will do.
	"""
	def choice_action(self):
		"""
			Args: -

			Action:
				Set the value of the attribute self._idmove [0,3]
				and the value of the attribute self._target [0, 1],
				which represents the action that the pokemon will perform on
				next turn.
		"""
		raise NotImplementedError

	def set_state(self, state):
		pass

	def recive_results(self, attacks, choices, done):
		pass

"""
	Extended class from Trainer that implements the choice_action function
	as a random choice.
"""
class TrainerRandom(Trainer):
	"""
		Implementation of choice_action funcion of the Trainer class.
	"""
	def choice_action(self):
		self._idmove = randint(0, 3)
		self._target = randint(0, 1)
