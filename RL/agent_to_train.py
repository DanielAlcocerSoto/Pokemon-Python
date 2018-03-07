#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Module that contains the Agent, an extencion of Trainer class.
This classes is a test of use a RL method in Game.

It contains the following classes:

	Agent
"""

# Local imports
from Game.engine.trainer import Trainer, ALLY, FOE
from Game.engine.core.pokemon import Pokemon, possible_pokemons_names
from .agent_to_play import Agent
from .model import Model

# 3rd party imports
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.optimizers import Adam

# General imports
from random import randint, choice, random, sample
from numpy import argmax, amax, array
from copy import deepcopy as copy
from ast import literal_eval
from pandas import read_csv
import csv


__version__ = '0.5'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'



file_model = "model_test"

"""
	Extended class from Trainer that use RL.
"""
class AgentTrain(Agent):
	def __init__(self, model = Model(), epsilon_min = 0.01, epsilon_decay = 0.995):
		self.epsilon = 1.0  # exploration rate
		self.epsilon_min = epsilon_min
		self.epsilon_decay = epsilon_decay
		Agent.__init__(self, model)
		self.replay()

	def choice_action(self):
		if random() <= self.epsilon:
			self._idmove = randint(0, self.num_moves_can_use()-1)
			self._target = randint(0, 1)
		else:
			Agent.choice_action(self)

	# train the agent with the experience of the episode
	def replay(self):
		self.model.train()

		if self.epsilon > self.epsilon_min:
			self.epsilon *= self.epsilon_decay

		#reset trainer
		pokemon_name = choice(possible_pokemons_names())
		self._pk=Pokemon(pokemon_name, 50)

	def save_model(self):
		self.model.save(file_model)
