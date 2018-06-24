
#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Module that contains the Agent, an extencion of Trainer class.
This classes is a test of use a RL method in Game.

It contains the following classes:

	Agent
"""
# Local import
from Game.engine.core.type import Type
from Game.engine.core.move import Move
from Game.engine.core.pokemon import Pokemon

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
		self.alphabet = dict((c, i) for i, c in enumerate(alphabet))

	def encode(self, data): #return array"
		if not isinstance(data, list): data=[data]
		integer_encoded = [self.alphabet[type] for type in data]
		ret = to_categorical(integer_encoded,num_classes=len(self.alphabet))
		ret = [list([int(x) for x in var]) for var in ret]
		if len(ret)==1: return ret[0]
		return ret

	#not used
	def decode_values(self, encoded_type):
		return list(self.alphabet.keys())[argmax(encoded_type)]


class Encoder:
	def __init__(self):
		Types = [t.title() for t in Type.possible_names()]
		self.encoder_type = Categorical_variable(Types)#18
		self.encoder_dmg = Categorical_variable(['physical','special'])#2
		#self.max_st  = {'hp': 1, 'attack': 1, 'special-attack': 1,
		#				'defense': 1, 'special-defense': 1, 'speed': 1}
		self.max_st={'hp': 255, 'attack': 165, 'special-attack': 154,
					'defense': 230, 'special-defense': 230, 'speed': 160}
		#len_poke_enc = 2*self.encoder_type.lenght+6+3 #6 stats,health,level,fainted
		self.len_move_enc = len(self._move_to_list(Move('pound')))#self.encoder_type.lenght+2 #actual_pp,power """+self.encoder_dmg.lenght"""
		self.len_poke_def_enc = len(self._poke_to_list(Pokemon('bulbasaur',50)))#2*self.encoder_type.lenght+2
		self.len_poke_atk_enc = len(self._poke_to_list(Pokemon('bulbasaur',50), ally_poke = True))
		self.state_size = self.len_poke_def_enc*2 + self.len_poke_atk_enc + self.len_move_enc*4#3 pokemon and 4 moves

	"""
	def _calc_max_stats(self,state):
		if self.max_st['hp']== 1:
			for role in ['Ally_0', 'Ally_1','Foe_0', 'Foe_1']:
				poke = state[role]
				for stat in self.max_st.keys():
					s = poke.get_stat(stat)
					if self.max_st[stat] < s: self.max_st[stat] = s
	"""

	def _norm_stats(self, poke):
		return {s:poke.get_stat(s)/m for s, m in self.max_st.items()}

	def _poke_to_list(self, poke, ally_poke = False):
		stats = self._norm_stats(poke)
		types = self.encoder_type.encode([t.name() for t in poke.types()])
		if not isinstance(types[0], list):
			types = [types, [0]*self.encoder_type.lenght]
		types = types[0] + types[1]
		# Return
		basic_l  = types + [int(poke.is_fainted())]
		damage_l = [poke.level()/100]
		if ally_poke:
			damage_l += [stats['attack'], stats['special-attack']]
			#health_l = []
		else:
			damage_l += [stats['defense'], stats['special-defense']]
			#health_l = [poke.health()/poke.get_stat('hp')] # not good results; ,stats['hp']]
		#order_l  = [stats['speed']]
		return basic_l + damage_l

	def _move_to_list(self, move):
		t_name = move.type().name()
		if move.accuracy() == None : acc = 1
		else: acc = move.accuracy()/100
		# Return
		basic_l  = self.encoder_type.encode(t_name) + [int(move.can_use())]
		damage_l = [move.power()] + self.encoder_dmg.encode(move.damage_class())
		# not good results; order_l  = [move.priority()/3]
		#random_l = [acc,move.prob_critic()]
		return  basic_l + damage_l

	def encode_state(self, state, my_role):
		#self._calc_max_stats(state)
		ret=[]
		# enemies_data
		enemy_role = 'Foe_' if 'Ally_' in my_role else 'Ally_'
		for j in range(2): ret+=self._poke_to_list(state[enemy_role+str(j)])
		#my_pokemon_data
		ret += self._poke_to_list(state[my_role], ally_poke = True)
		moves=state[my_role].moves()
		for i in range(4): ret += self._move_to_list(moves[i])
		#print('encode state = {}'.format(ret))
		return ret

	def _encode_action(self, move, target):
		return target*4 + move

	def encode_action(self, choices, role):
		return self._encode_action(*choices[role])

	def decode_action(self, list_Q):
		action = argmax(list_Q)
		return action%4, action//4 # return move, target



class CoopEncoder(Encoder):
	def __init__(self):
		Encoder.__init__(self)
		self.state_size += self.len_poke_atk_enc + self.len_move_enc*4

	def encode_state(self, state, my_role):
		ret=Encoder.encode_state(self,state,my_role)
		#my_ally_data
		r = my_role.split('_')
		ally_role = r[0]+'_'+str((int(r[1])+1)%2)
		ret += self._poke_to_list(state[ally_role], ally_poke = True)
		moves=state[ally_role].moves()
		for i in range(4): ret += self._move_to_list(moves[i])
		return ret

	def encode_action(self, choices, role):
		r = role.split('_')
		ally_role = r[0]+'_'+str((int(r[1])+1)%2)
		action = self._encode_action(*choices[role])
		if ally_role in choices.keys():
			action_ally = self._encode_action(*choices[ally_role])
		else: action_ally = 0 #cualquier accion
		return action*8+action_ally

	def decode_action(self, list_Q, move_ally, target_ally):
		action_ally = Encoder._encode_action(self, move_ally, target_ally)
		indexes = array(range(0,64))%8 == action_ally
		list_Q_ally = list_Q[indexes]
		action = argmax(list_Q_ally)
		return action%4, action//4

	def decode_best_action(self, list_Q):
		action = argmax(list_Q)//8
		return action%4, action//4
