#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Module to interact with the pokeAPI to generate the information
(making requests to the pokeAPI) and save it into a files.

This module contains the following functions to import to another classes:

	generate_types
	generate_moves
	generate_pokemons

It also includes other functions that should not be imported,
because they are to interact with the pokeAPI:

	get
	search
	partitionate_search
"""

# Local imports
from Configuration.settings import Directory, Generate_Config
from .utils_data_base import download_sprite, save_info, load_info

# General imports
import requests
import json

__version__ = '1.0'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'


#####################################UTILS######################################

"""
	Function to get the dictionary of the url.
"""
def get(url):
	"""
		Args:
			url ('str'): A url that contains a dictionary.

		Return ('dict'):
			The dictionary that represents the url 'url'.
	"""
	response = requests.get(url)
	if response.ok: return response.json()
	else:
		print('Error in requests_get: '+str(response.status_code) +': '+ \
										str(response.reason))
		response.raise_for_status()


"""
	Function to serch in the pokeAPI.
"""
def search(attr, args={}):
	"""
		Args:
			attr ('str'): The attribute that want to search (pokemon,move,type).
			args ('dict'): Argunments for the search. The most frequent fields
			 			   are 'limit' and 'offset'.

		Return ('dict'):
			A list of dictionaries with the results. Each dictionary contains
			a field 'name', and a field 'url'.
	"""

	response = requests.get(Generate_Config['POKE_API']+attr+'/', params = args)
	if response.ok: return response.json().get('results',[])
	else:
		print('Error in requests_search: '+ str(response.status_code) +': '+ \
		 									str(response.reason))
		response.raise_for_status()


"""
	Function to generate information in a partitionate way,
	because maybe the connection is rejected by too many requests.
	Used it when the search involves large amounts of results (atleast 100).
"""
def partitionate_search(attr, filter_item, start):
	"""
		Args:
			attr ('str'): Attribute param for the search function.
			filter_item ('func'): Function to filter one result.
								  It must to Return a key (name) and value (info)
								  in a pair format.
			start ('int'): Starter iteration.

		Action:
			Generate a info file for 'attr', but done in iterations.
	"""

	name = attr[:4].upper()
	PATH = Directory[name+'_FILE']
	NUM_ITEMS = Generate_Config['N_'+name]

	def loop (result):
		dex = load_info(PATH)
		for r in result:
			pair = filter_item(get(r['url']))
			if pair != None:
				key, value = pair
				if Generate_Config['PRINT_NAME']: print(key)
				dex[key]=value
		save_info(PATH, dex)

	N_ITER = NUM_ITEMS//100
	SIZE = NUM_ITEMS//N_ITER

	result = search(attr, args = {'limit': NUM_ITEMS})

	if start == 0: save_info(PATH, {})
	for i in range(start,N_ITER):
		print (attr+'....................'+str(SIZE*i)+'/'+str(NUM_ITEMS)+ \
					'.................... iteration: '+str(i))
		loop(result[SIZE*i: SIZE*(i+1)])
	loop(result[SIZE*N_ITER:]) #The remainig

#####################################TYPES######################################

"""
	Function to generate types info file
"""
def generate_types():
	"""
		Args: -

		Action:
			Create a new file with the information of the differents types.
	"""

	"""
		Function to filter the information of a type.
		('dict' --> 'dict')
	"""
	def filter_type_info(ty):
		if Generate_Config['PRINT_NAME']: print(ty['name'])
		return {relation: [t['name'] for t in types]
				for relation, types in ty['damage_relations'].items()
				if relation.split('_')[2] == 'to'}

	typedex = { ty['name']:
				filter_type_info(get(ty['url']))
				for ty in search('type', args = {'limit':Generate_Config['N_TYPE']})}
	save_info(Directory['TYPE_FILE'], typedex)

#####################################MOVES######################################

"""
	Function to generate moves info file
"""
def generate_moves(start_iteration=0):
	"""
		Args:
			start_iteration ('int'): Starter iteration.

		Action:
			Create a new file with the information of the differents moves.
	"""

	"""
		Function to filter the information of a move.
		To use it in the partitionate_search function.
	"""
	def filter_move (move):
		"""
			Args:
				move ('dict'): A dictionary with all information of a move.

			Return ('str', 'dict'):
				The name of the move and a dictionary with the information
				of 'move' filtered.
		"""

		if move['power'] == None:
			return None
		else:
			info = {
				'power':move['power'],
				'pp':move['pp'],
				'type':move['type']['name'],
				'accuracy':move['accuracy'],
				'priority':move['priority'],
				'damage_class':move['damage_class']['name'],
				'crit_rate':move['meta']['crit_rate']
			}
			return (move['name'], info)

	partitionate_search('move', filter_move, start_iteration)

####################################POKEMON#####################################

"""
	Function to generate pokemons info file
"""
def generate_pokemons(start_iteration=0):
	"""
		Args:
			start_iteration ('int'): Starter iteration.

		Action:
			Create a new file with the information of the differents pokemons.
	"""

	movesList = load_info(Directory['MOVE_FILE']).keys()

	"""
		Function to filter the information of the pokemon types.
		('list of dict' --> 'list')
	"""
	def filter_types(types):
		return [ty["type"]["name"] for ty in types]

	"""
		Function to filter the information of the pokemon stats.
		('list of dict' --> 'dict')
	"""
	def filter_stats(stats):
		return {st["stat"]["name"]:
				{"effort": st["effort"],
				"base_stat": st["base_stat"]}
				for st in stats }

	"""
		Function to filter the information of the pokemon moves.
		('list of dict' --> 'list')
	"""
	def filter_moves(moves):
		return [mo["move"]["name"] for mo in moves if mo["move"]["name"] in movesList]

	"""
		Function to filter the information of the pokemon sprite.
		('dict' --> 'dict')
	"""
	def filter_sprites(pokemon):
		name_file = str(pokemon['id'])+'_'+filter_name(pokemon['name'])+'_'
		download_sprite(pokemon['sprites']['front_default'], name_file+'front')
		download_sprite(pokemon['sprites']['back_default'], name_file+'back')
		return {'front':name_file+'front', 'back':name_file+'back'}

	"""
		Function to filter the name of the pokemon.
		('dict' --> 'dict')
	"""
	def filter_name(name):
		if '-' in name:
			name_split = name.split('-')
			words = ['normal', 'plant', 'altered', 'land']
			if name_split[1] in words: return name_split[0]
			else: return name
		else: return name

	"""
		Function to filter the information of a pokemon.
		To use it in the partitionate_search function.
	"""
	def loop_pokemon (pokemon):
		"""
			Args:
				move ('dict'): A dictionary with all information of a pokemon.

			Return ('str', 'dict'):
				The name of the pokemon and a dictionary with the information
				of 'pokemon' filtered.
		"""
		info = {'types':filter_types(pokemon['types']),
				'stats':filter_stats(pokemon['stats']),
				'moves':filter_moves(pokemon['moves']),
				'sprites':filter_sprites(pokemon)}
		if len(info['moves']) < 4: return None
		return (filter_name(pokemon['name']), info)

	partitionate_search('pokemon', loop_pokemon, start_iteration)
