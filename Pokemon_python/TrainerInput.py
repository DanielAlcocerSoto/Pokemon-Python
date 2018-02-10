#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

"""

from Pokemon_python.core.pokemon import Pokemon
from Pokemon_python.core.type import Type
from Pokemon_python.core.move import Move
from Pokemon_python.trainer import Trainer

__version__ = '0.5'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'


class TrainerInput(Trainer):
	def choice_action(self, info):
		def while_input_in_range(text, max_nume_elem):
			idx = -1
			while(idx not in range(0, max_nume_elem)):
				raw_inp = input(text+" [0-"+str(max_nume_elem-1)+"] ")
				try :
					idx = int(raw_inp)
					if idx not in range(0, max_nume_elem): raise Exception()
				except:
					print('Error: incorrect number')
			return idx
		print('\nWhat should '+self._pk.name()+' do?')
		for move in self._pk.moves():
			name = move.name()
			num = 'This move can not be used'
			for i,can_move in enumerate(self._pk.moves_can_use()):
				if can_move.name() == name:
					num='Move '+str(i)
					break
			print(num+': '+name+' ('+str(move.type().name())+')')
			print('\tPP: '+str(move.actual_pp())+'/'+str(move.max_pp())+' (Power: '+str(move.power())+')')
		self._idmove = while_input_in_range("\nWhat movement do you want to use?", self.num_moves_can_use())
		print('')
		targets = []
		for name, poke in info.items():
			if poke['ally'] != self.is_ally():
				if not poke['fained']:
					targets.append(name)
		if len(targets) == 2:
			print ('Posibles targets:')
			for name in sorted(targets, key=lambda name : info[name]['pos']):
				print ('\t'+str(info[name]['pos'])+': '+name )
			self._target = while_input_in_range("Against whom you want to use it?", 2)
		else:
			self._target = info[targets[0]]['pos']
		print('')
