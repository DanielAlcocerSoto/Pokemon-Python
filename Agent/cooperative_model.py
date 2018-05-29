#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Module that contains the Model, main class of RL.

It contains the following class:

	BaseModel
"""

# Local import
from Configuration.settings import Agent_config
from .encoder import Encoder
from .model import BaseModel

# General imports
from numpy import amax, array

__version__ = '0.5'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'

"""

"""
class CoopModel(BaseModel):
	def __init__(self, rebuid=False):
		BaseModel-__init__(self, rebuid)
		self.output_layer_size = 8*8
		self.encoder = CoopEncoder()

	def predict(self, state, role):
		## TODO cambiar para recivir la accion del compañero
		state = array([self.encoder.encode_state(state, role)])
		act_values = self.keras_NN_model.predict(state)
		print('Result of Keras model for {}: {}'.format(role,act_values))
		return self.encoder.decode_action(act_values[0])

	def remember(self, state, role, attacks, choices, next_state, done):
		## TODO cambiar para soportar en nuevo formato de accion
		pass

#private functions
	def _get_reward(self, my_role, attacks):
		## TODO cambiar para mexclar las recomensas
		if my_role in attacks.keys():
			attack=attacks[my_role]
			return attack.dmg
		else: return 0
""""
class CoopEncoder(Encoder):
	def __init__(self):
"""
