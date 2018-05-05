#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Module that contain the generic class useful for create other classes
who need to save information from the database:

	Object_Info
"""

# Local imports
from DataBase.utils_data_base import load_info

__version__ = '1.0'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'


"""
	Generic object with information about one element of the database,
	be it move, type or pokemon.
"""
class Object_Info:
	"""
		Returns all key in the database.
	"""
	@staticmethod
	def possible_names():
		"""
			Args: -

			Return ('list of str'):
				The name (key) of all the items in the database.
		"""
		raise NotImplementedError

	def __init__(self, name, file_name):
		"""
		Args:
			name ('str'): The name (key of the dictionary) of the resource.
			file_name ('str'): The name of the file where is the resource.

		Action:
			Create a 'Object_Info' with the information of 'name' in the
			'file_name' file.
		"""

		file_dict = load_info(file_name)
		self._name = name
		if self._name in list(file_dict.keys()):
			self._info = file_dict[name]
		else : raise Exception('Name "'+name+'" does not exist in '+file_name)

	"""
		Returns the name of the information resource with the first
		characters of all the words are capitalized.
		('' --> 'str')
	"""
	def name(self):
		return self._name.title()
