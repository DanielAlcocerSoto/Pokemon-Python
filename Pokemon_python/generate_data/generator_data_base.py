#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Module to interact with the pokeAPI
to generate the information
(making requests to the API)
and to save it into a files
"""

from Pokemon_python.utils_data_base import download_sprite, save_json, load_json
from Pokemon_python.sittings import Directory, Generate_Config

import requests
import json
import argparse

__version__ = '1.0'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'

####################################UTILS######################################

def get(url):
	response = requests.get(url)
	if response.ok: return response.json()
	else:
		print('Error in requests_get: '+str(response.status_code) +': '+ str(response.reason))
		response.raise_for_status()

def search(attr, args={}):
	response = requests.get(Generate_Config['API']+attr+'/', params = args)
	if response.ok: return response.json().get('results',[])
	else:
		print('Error in requests_search: '+str(response.status_code) +': '+ str(response.reason))
		response.raise_for_status()

###################################POKEMON#####################################

def generate_pokemons(start=2, ITER = 4):

	movesList = load_json(Directory['MOVE_FILE']).keys()

	def filter_types(types):
		return [ty["type"]["name"] for ty in types]

	def filter_stats(stats):
		return {st["stat"]["name"]:
				{"effort": st["effort"],
				"base_stat": st["base_stat"]}
				for st in stats }

	def filter_moves(moves):
		return [mo["move"]["name"] for mo in moves if mo["move"]["name"] in movesList]

	def filter_sprites(pokemon):
		name_file = str(pokemon['id'])+'_'+pokemon['name']+'_'
		download_sprite(pokemon['sprites']['front_default'], name_file+'front')
		download_sprite(pokemon['sprites']['back_default'], name_file+'back')
		return {'front':name_file+'front', 'back':name_file+'back'}

	def filter_pokemon_info(pokemon):
		print(pokemon['name'])
		return {'types':filter_types(pokemon['types']),
				'stats':filter_stats(pokemon['stats']),
				'moves':filter_moves(pokemon['moves']),
				'sprites':filter_sprites(pokemon)}

	def bucle (result):
		pokedex = load_json(Directory['POKE_FILE'])
		for r in result:
			pokemon = get(r['url'])
			pokedex[pokemon['name']] = filter_pokemon_info(pokemon)
		save_json(Directory['POKE_FILE'], pokedex)

	if start == 0: save_json(Directory['POKE_FILE'], {})
	N_POKE = Generate_Config['N_POKE']
	for i in range(start,ITER): #too many info, maybe some problem appear
		print ('new try....................'+str(N_POKE//ITER*i)+'/'+str(N_POKE))
		bucle(search('pokemon', args = {'limit':N_POKE//ITER, 'offset':N_POKE//ITER*i}))
	bucle(search('pokemon', args = {'limit':N_POKE%ITER, 'offset':N_POKE//ITER*ITER}))

####################################TYPES######################################

def generate_types():
	def filter_type_info(ty):
		print(ty['name'])
		return {relation: [t['name'] for t in types]
				for relation, types in ty['damage_relations'].items()
				if relation.split('_')[2] == 'to'}

	typedex = { ty['name']:
				filter_type_info(get(ty['url']))
				for ty in search('type', args = {'limit':Generate_Config['N_TYPE']})}
	save_json(TYPE_FILE, typedex)

####################################MOVES######################################

def generate_moves(start=0, ITER = 7):#Max 405 start with 1
	def es_name(move):
		for idiom in move['names']:
			if idiom['language']['name'] == 'es':
				return idiom['name']
		return move['name']

	def bucle (result):
		movedex = load_json(Directory['MOVE_FILE'])
		for r in result:
			move = get(r['url'])
			if move['power'] != None:
				name_move = move['name']
				print (name_move)
				movedex[name_move] = {
					'es_name':es_name(move),
					'power':move['power'],
					'pp':move['pp'],
					'type':move['type']['name'],
					'accuracy':move['accuracy'],
					'priority':move['priority'],
					'damage_class':move['damage_class']['name'],
					'crit_rate':move['meta']['crit_rate']
				}
		save_json(Directory['MOVE_FILE'], movedex)

	if start == 0: save_json(Directory['MOVE_FILE'], {})
	N_MOVE = Generate_Config['N_MOVE']
	for i in range(start,ITER): #too many info, maybe some problem appear
		print ('new try....................'+str(N_MOVE//ITER*i)+'/'+str(N_MOVE))
		bucle(search('move', args = {'limit':N_MOVE//ITER, 'offset':N_MOVE//ITER*i}))
	bucle(search('move', args = {'limit':N_MOVE%ITER, 'offset':N_MOVE//ITER*ITER})) # total 719 = N_MOVE
