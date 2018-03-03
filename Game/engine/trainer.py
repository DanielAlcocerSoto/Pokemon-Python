#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Module that contains the Trainer and the TrainerRandom classes.
This classes are used to set the acctions that will be made by the pokemon.

It contains the following classes:

	Trainer
	TrainerRandom

And the usefull constants:

	ALLY
	FOE
"""

# Local imports
from .core.pokemon import Pokemon

# General imports
from random import randint

__version__ = '1.0'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'


# Constant that represent a Ally trainer
ALLY = True

# Constant that represent a Foe trainer
FOE = False

"""
	Generic trainer with basic funcions.
"""
class Trainer:
	def __init__(self, team, pokemon):
		"""
			Args:
				team ('bool'): The team to which the trainer belongs.
				pokemon (class:'Pokemon'): The Pokemon of the trainer.

			Action:
				Create a 'Trainer' of the team 'team' with a pokemon 'pokemon'.
		"""
		self._team=team
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
		return self._team == ALLY

	"""
		Return the moves that pokemon can do.
		('' --> 'list of class:Move')
	"""
	def num_moves_can_use(self):
		return len(self._pk.moves_can_use())

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
		return (self._pk.moves_can_use()[self._idmove], target)

	"""
		Set the next action that the pokemon will do.
	"""
	def choice_action(self):
		"""
			Args: -

			Action:
				Set the value of the attribute self._idmove [0,
				self.num_moves_can_use()-1]
				and the value of the attribute self._target [0, 1],
				which represents the action that the pokemon will perform on
				next turn.
		"""
		raise NotImplementedError

	def set_state(self, state):
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
		self._idmove = randint(0, self.num_moves_can_use()-1)
		self._target = randint(0, 1)
