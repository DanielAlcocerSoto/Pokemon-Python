#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

"""

from Pokemon_python.utils_data_base import TYPE_FILE, Object_Info

__version__ = '1.0'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'

class Type(Object_Info):
	def __init__(self, name):
		Object_Info.__init__(self, name, TYPE_FILE)
		self._multiplierTo = {}
		for key in self._keys:
			if   key in self._info['no_damage_to']:     self._multiplierTo[key] = 0
			elif key in self._info['half_damage_to']:   self._multiplierTo[key] = 0.5
			elif key in self._info['double_damage_to']: self._multiplierTo[key] = 2
			else: self._multiplierTo[key] = 1

	def multiplier(self, listTypes):
		mult = 1
		for Type in listTypes: mult*=self._multiplierTo[Type._name]
		return mult
	def bonification(self, listTypes):
		if any([x._name==self._name for x in listTypes]): return 1.5
		else: return 1
