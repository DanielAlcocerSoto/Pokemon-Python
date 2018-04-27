#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Module that contains an extension of the 'Object_Info' class to manage the
information of the types.

This module contains the following class:

	Type
"""

# Local imports
from Configuration.settings import Directory
from .object_info import Object_Info, load_info

__version__ = '1.0'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'


"""
	Class with information about a type.
"""
class Type(Object_Info):
	"""
		Returns the name of all types in the database.
	"""
	@staticmethod
	def possible_names():
		"""
			Args: -

			Return ('list of str'):
				The name (key) of all the types in the database.
		"""
		return list(load_info(Directory['TYPE_FILE']).keys())

	def __init__(self, name):
		"""
			Args:
				name ('str'): The name (key of the dictionary) of the type.

			Action:
				Create a Type with the information of 'name' type.
		"""
		Object_Info.__init__(self, name, Directory['TYPE_FILE'])
		self._multiplierTo = {}
		for key in Type.possible_names():
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
