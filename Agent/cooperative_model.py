#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Module that contains the Model, main class of RL.

It contains the following class:

	BaseModel
"""

# Local import
from Configuration.settings import Agent_config
from .encoder import Encoder, CoopEncoder
from .model import BaseModel

# General imports
from numpy import amax, array

__version__ = '0.5'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'



"""
To learn from an experienced player
"""
class LearnerModel(BaseModel):
	def remember(self, state, role, attacks, choices, next_state, done):
		#my experience
		BaseModel.remember(self, state, role, attacks, choices, next_state, done)
		# ally's experience
		r = role.split('_')
		role_ally = r[0]+'_'+str((int(r[1])+1)%2)
		BaseModel.remember(self, state, role_ally, attacks, choices, next_state,
		 				   done, player = True)


"""

"""
class CoopModel(LearnerModel):
	def __init__(self, model_name = None, rebuid = False):
		self.output_layer_size = 8*8
		self.encoder = CoopEncoder()
		self._init_model(model_name, rebuid)

	def predict(self, state, role):
		state = array([self.encoder.encode_state(state, role)])
		act_values = self.keras_NN_model.predict(state)
		#print('Result of Keras model for {}: {}'.format(role,act_values))
		return self.encoder.decode_best_action(act_values[0])

	def predict_base_on_ally_action(self, state, role, action_ally):
		state = array([self.encoder.encode_state(state, role)])
		act_values = self.keras_NN_model.predict(state)
		#print('Result of Keras model for {}: {}'.format(role,act_values))
		move_ally, target_ally = action_ally
		return self.encoder.decode_action(act_values[0], move_ally, target_ally)

#private functions
	def _get_reward(self, attacks, my_role):
		r = my_role.split('_')
		ally_role = r[0]+'_'+str((int(r[1])+1)%2)
		dmg = LearnerModel._get_reward(self, attacks, my_role)
		dmg += LearnerModel._get_reward(self, attacks, ally_role)
		return dmg
