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



memory = "RL/Data/log"

"""
	Extended class from Trainer that use RL.
"""
class Agent(Trainer):
	def __init__(self, model = Model()):
		self.gamma = 0.95   # discount rate
		self.model = model

		pokemon_name = choice(possible_pokemons_names())
		Trainer.__init__(self,ALLY,Pokemon(pokemon_name, 50))

	def set_state(self, state):
	    self.actual_state = state
	    self.last_state = copy(state)

	def choice_action(self):
		state = self.actual_state
		self._idmove, self._target = self.model.predict(state)

	def _remember(self, reward, done):
		state = self.last_state
		next_state = self.actual_state
		self.model.remember(state, self._idmove, self._target, \
		 					reward, next_state, done)

	def recive_results(self, attacks):
		#TODO calc reward self.actual_state
		#TODO done as parameter because  gen maybe live!!!
		reward = 5
		self._remember(reward, self.pokemon().is_fainted())
		self.last_state = copy(self.actual_state)
