#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Module that contains an extension of the 'Object_Info' class to manage the
information of the types.

This module contains the following class:

	Type
"""

# Local imports
from Game.settings import Directory
from Game.utils_data_base import Object_Info

__version__ = '1.0'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'


"""
	Class with information about a type.
"""
class Type(Object_Info):
	def __init__(self, name):
		"""
			Args:
				name ('str'): The name (key of the dictionary) of the type.

			Action:
				Create a Type with the information of 'name' type.
		"""
		Object_Info.__init__(self, name, Directory['TYPE_FILE'])
		self._multiplierTo = {}
		for key in self._keys:
			if   key in self._info['no_damage_to']:     self._multiplierTo[key] = 0
			elif key in self._info['half_damage_to']:   self._multiplierTo[key] = 0.5
			elif key in self._info['double_damage_to']: self._multiplierTo[key] = 2
			else: self._multiplierTo[key] = 1

	"""
		Returns the multiplier factor of this type.
	"""
	def multiplier(self, listTypes):
		"""
			Args:
				listTypes ('list of class:Type'): List of types of the pokemon
												  from which you want to obtain
												  the multiplier.

			Return ('int'):
				The acumulated multiplier factor according to the damage
				relations of this type.
		"""
		mult = 1
		for Type in listTypes: mult*=self._multiplierTo[Type._name]
		return mult

	"""
		Returns the bonification factor depending on the params.
	"""
	def bonification(self, listTypes):
		"""
			Args:
				listTypes ('list of class:Type'): List of types of the pokemon
												  from which you want to obtain
												  the bonification.

			Return (class:'pygame.Surface'):
				The coresponding bonification factor depending on the 'listTypes'.
		"""
		if any([x._name==self._name for x in listTypes]): return 1.5
		else: return 1
