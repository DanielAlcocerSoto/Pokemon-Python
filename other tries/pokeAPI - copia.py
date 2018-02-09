#!/usr/bin/python3
"""
Module to interact with the pokeAPI 
both to generate the information 
(making requests to the API) 
and to obtain it 
(from the files that are created)
"""
import requests
import json
import argparse

__version__ = '0.9'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'

##################################CONSTANTS####################################

API = 'http://pokeapi.co/api/v2/'

DIR_JSON = 'DataBase/'

POKE_FILE = 'pokemonDB'
TYPE_FILE = 'typeDB'
MOVE_FILE = 'moveDB'

N_POKE = 151
N_TYPE = 20
N_MOVE = 737

NOT_TYPES = ['shadow', 'unknown']

####################################UTILS######################################

def print_dict(d, sort=False):
	print(json.dumps(d, indent=4, sort_keys=sort))

def save_json(name_file, obj):
	with open(DIR_JSON+name_file+'.json', 'w') as file:
		json.dump(obj, file, indent=4)

def load_json(name_file):
	with open(DIR_JSON+name_file+'.json', 'r') as file:
		obj = json.load(file) 
	return obj

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
	def filter_types(types):
		return [ty["type"]["name"] for ty in types]

	def filter_stats(stats):
		return {st["stat"]["name"]: 
				{"effort": st["effort"],
				"base_stat": st["base_stat"]} 
	            for st in stats }

	def filter_moves(moves):
		return [mo["move"]["name"] for mo in moves]

	def filter_pokemon_info(pokemon):
		return {'types':filter_types(pokemon['types']),
				'stats':filter_stats(pokemon['stats']),
				'moves':filter_moves(pokemon['moves'])}

	pokedex = { pokemon['name']: 
				filter_pokemon_info(get(pokemon['url'])) 
				for pokemon in search('pokemon', args = {'limit':N_POKE})}
	save_json(POKE_FILE, pokedex)

def get_pokemon(name):
	return load_json(POKE_FILE)[name]

####################################TYPES######################################

def generate_types():
	def filter_type_info(ty):
		return {relation: [t['name'] for t in types] 
				for relation, types in ty['damage_relations'].items()}

	typedex = { ty['name']: 
				filter_type_info(get(ty['url']))
				for ty in search('type', args = {'limit':N_TYPE})
				if get(ty['url'])['name'] not in NOT_TYPES }
	save_json(TYPE_FILE, typedex)

def get_type(name):
	return load_json(TYPE_FILE)[name]

####################################MOVES######################################

def generate_moves():
	mt=0
	def filter_move_info(move):
		print ('MT'+str(mt)+' '+move['name'])
		print_dict (move['meta'])
		return {'power':move['power'],
				'pp':move['pp'],
				'type':move['type']['name'],
				'accuracy':move['accuracy'],
				'priority':move['priority'],
				'damage_class':move['damage_class']['name'],
				'crit_rate':move['meta']['crit_rate']}

	movedex = { move['name']: 
				filter_move_info(get(move['url']))
				for move in search('move', args = {'limit':N_MOVE}) 
				if get(move['url'])['type']['name'] not in NOT_TYPES}
	save_json(MOVE_FILE, movedex)

def get_move(name):
	return load_json(MOVE_FILE)[name]

#####################################MAIN######################################

def main(args):
	if  args.poke or args.all:
		print('Generating pokemons info...')
		generate_pokemons()
	if  args.move or args.all:
		print('Generating moves info...')
		generate_moves()
	if  args.type or args.all:
		print('Generating types info...')
		generate_types()
	if  not (args.poke or args.move or args.type or args.all):
		print('Specify that you want to generate: --poke, --move, --type or --all')

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--poke', '-p', action='store_true')
	parser.add_argument('--move', '-m', action='store_true')
	parser.add_argument('--type', '-t', action='store_true')
	parser.add_argument('--all' , '-a', action='store_true') 
	main(parser.parse_args() )	