
#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Module that contains the Agent, an extencion of Trainer class.
This classes is a test of use a RL method in Game.

It contains the following classes:

	Agent
"""
# Local import
from Game.engine.core.type import possible_type_names

# 3rd party imports
from keras.utils import to_categorical

# General imports
from numpy import argmax, array


__version__ = '0.5'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'


"""
	Class to encode variables.
"""
class Categorical_variable:
	def __init__(self, alphabet):
		self.lenght = len(alphabet)
		self.type_alphabet = dict((c, i) for i, c in enumerate(alphabet))

	def encode_values(self, data): "return array"
		if not isinstance(data, list): data=[data]
		integer_encoded = [self.type_alphabet[type] for type in data]
		return to_categorical(integer_encoded,num_classes=len(self.type_alphabet))

	#not used
	def decode_values(self, encoded_type):
		return list(self.type_alphabet.keys())[argmax(encoded_type)]


class Encoder:
	def __init__(self):
		self.type = Categorical_variable(possible_type_names())
		self.state_size = 45

	def _poke_to_list(self, poke): #'6'+2+3 =11
		n = ["hp", "attack", "special-attack", "defense", \
			 "special-defense", "speed"]
		stats = [poke.get_stat(s) for s in n]
		types = self.type.encode_values(poke.types())
		types = types[0].extend([0]*self.type.lenght if len(types)==1 else types[1])
		return stats + types + [poke.health(), poke.level(), poke.is_fainted()]

	def _move_to_list(self, move): #3
		return [self.type.encode_values(move.type().name()), \
				move.actual_pp(), move.power()]

	def encode_state(self, state):# 3*4 + 11*3
		#TODO  index-->value
		#my_pokemon_data
		ret = self._poke_to_list(state['Ally_1'])
		moves=state['Ally_1'].moves()
		for i in range(4):
			if i < len(moves): ret+= self._move_to_list(moves[i])
			else: ret+= [0]*3#numero_de_datos_de_move
		for j in range(2):
			ret+=self._poke_to_list(state['Foe_'+str(j)])
		# enemies_data
		return ret
