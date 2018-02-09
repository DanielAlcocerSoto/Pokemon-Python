#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Module to interact with the pokeAPI
to generate the information
(making requests to the API)
and to save it into a files
"""
import requests
import json
import shutil
import argparse

__version__ = '0.9'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'

##################################CONSTANTS####################################

API = 'http://pokeapi.co/api/v2/'
DIR_DB = 'DataBase/'
DIR_JSON = DIR_DB+'JSon/'
DIR_IMAGES = DIR_DB+'Images/'
DIR_SPRITES = DIR_IMAGES+'Sprites/'

POKE_FILE = 'pokemonDB'
TYPE_FILE = 'typeDB'
MOVE_FILE = 'moveDB'

N_POKE = 151
N_TYPE = 18
N_MOVE = 719

####################################UTILS######################################

def print_dict(d, sort=False):
	print(json.dumps(d, indent=4, sort_keys=sort))

def load_json(name_file):
	with open(DIR_JSON+name_file+'.json', 'r') as file:
		obj = json.load(file)
	return obj

def save_json(name_file, obj):
	with open(DIR_JSON+name_file+'.json', 'w') as file:
		json.dump(obj, file, indent=4)

def download_image(url,name_file):
	response = requests.get(url, stream=True)
	with open(get_sprite_path(name_file), 'wb') as file:
		shutil.copyfileobj(response.raw, file)

def get_sprite_path(name_file):
	return DIR_SPRITES+name_file+'.png'
def get_image_path(name_file):
	return DIR_IMAGES+name_file+'.png'

def get(url):
	response = requests.get(url)
	if response.ok: return response.json()
	else:
		print('Error in requests_get: '+str(response.status_code) +': '+ str(response.reason))
		response.raise_for_status()

def search(attr, args={}):
	response = requests.get(API+attr+'/', params = args)
	if response.ok: return response.json().get('results',[])
	else:
		print('Error in requests_search: '+str(response.status_code) +': '+ str(response.reason))
		response.raise_for_status()

###################################POKEMON#####################################

def generate_pokemons():

	movesList = load_json(MOVE_FILE).keys()

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
		download_image(pokemon['sprites']['front_default'], name_file+'front')
		download_image(pokemon['sprites']['back_default'], name_file+'back')
		return {'front':name_file+'front', 'back':name_file+'back'}

	def filter_pokemon_info(pokemon):
		print(pokemon['name'])
		return {'types':filter_types(pokemon['types']),
				'stats':filter_stats(pokemon['stats']),
				'moves':filter_moves(pokemon['moves']),
				'sprites':filter_sprites(pokemon)}

	pokedex = { pokemon['name']:
				filter_pokemon_info(get(pokemon['url']))
				for pokemon in search('pokemon', args = {'limit':N_POKE})}
	save_json(POKE_FILE, pokedex)

####################################TYPES######################################

def generate_types():
	def filter_type_info(ty):
		print(ty['name'])
		return {relation: [t['name'] for t in types]
				for relation, types in ty['damage_relations'].items()
				if relation.split('_')[2] == 'to'}

	typedex = { ty['name']:
				filter_type_info(get(ty['url']))
				for ty in search('type', args = {'limit':N_TYPE})}
	save_json(TYPE_FILE, typedex)

####################################MOVES######################################

def generate_moves(start=0, ITER = 7):#Max 405 start with 1
	def bucle (result):
		movedex = load_json(MOVE_FILE)
		for r in result:
			move = get(r['url'])
			if move['power'] != None:
				print (move['name'])
				movedex[move['name']] = {
					'power':move['power'],
					'pp':move['pp'],
					'type':move['type']['name'],
					'accuracy':move['accuracy'],
					'priority':move['priority'],
					'damage_class':move['damage_class']['name'],
					'crit_rate':move['meta']['crit_rate']
				}
		save_json(MOVE_FILE, movedex)

	if start == 0: save_json(MOVE_FILE, {})
	for i in range(start,ITER): #too many info, maybe some problem appear
		print ('new try....................'+str(N_MOVE//ITER*i)+'/'+str(N_MOVE))
		bucle(search('move', args = {'limit':N_MOVE//ITER, 'offset':N_MOVE//ITER*i}))
	bucle(search('move', args = {'limit':N_MOVE%ITER, 'offset':N_MOVE//ITER*ITER})) # total 719 = N_MOVE

#####################################MAIN######################################

def main(args):
	if  args.move or args.all:
		print('Generating moves info...')
		generate_moves()
	if  args.poke or args.all:
		print('Generating pokemons info...')
		generate_pokemons()
	if  args.type or args.all:
		print('Generating types info...')
		generate_types()
	if  not (args.poke or args.move or args.type or args.all):
		print('Specify that you want to generate: --move, --poke, --type or --all')


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--move', '-m', action='store_true')
	parser.add_argument('--poke', '-p', action='store_true')
	parser.add_argument('--type', '-t', action='store_true')
	parser.add_argument('--all' , '-a', action='store_true')
	main(parser.parse_args())
