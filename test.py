
#import os
#print(os.path.exists('Database/Agent/Logs/trash.csv'))
"""
from Configuration.settings import Directory
from Game.engine.core.object_info import load_info

# General imports
from random import randint, sample, choice
from math import floor
from numpy import argmax, amax, max

def get_stats(stats):
    n= ["hp", "attack", "special-attack", "defense", \
        "special-defense", "speed"]
    for name in n:
        stat = stats[name]
        precalc = stat*2 + 31
        precalc = floor(precalc)
        if name == 'hp': stat = precalc + 100 + 10
        else: stat = precalc + 5
    return stats

obj = load_info(Directory['POKE_FILE'])

m = {"hp":0, "attack":0, "special-attack":0, "defense":0, \
    "special-defense":0, "speed":0}
for p in obj.values():
    s=p['stats']
    info=get_stats(s)
    n= ["hp", "attack", "special-attack", "defense", \
        "special-defense", "speed"]
    for stat in n:
        if m[stat] < info[stat]:
            m[stat] = info[stat]
print(m) #maximum stats posibles

def _norm_stats(poke):
    max_st={'hp': 255, 'attack': 165, 'special-attack': 154,
            'defense': 230, 'special-defense': 230, 'speed': 160}
    return {s:poke.get_stat(s)/m for s, m in max_st.items()}

from Game.engine.core.pokemon import Pokemon
print(_norm_stats(Pokemon('arceus',100)))
"""
from DataBase.utils_data_base import load_info
from Configuration.settings import Directory
from numpy import array, argmax, mean
"""
#pokemon-move count
moves_counter = {}
print('num of pokes = ',len(load_info(Directory['POKE_FILE'])))
for pk in load_info(Directory['POKE_FILE']).values():
    for move in pk['moves']:
        if move in moves_counter.keys():
            moves_counter[move] += 1
        else: moves_counter[move] = 1

from numpy import array, argmax, mean
count = array(list(moves_counter.values()))
i_max = argmax(count)
print(max(count), argmax(count), len(count), mean(count))
move = list(moves_counter.keys())[i_max]


print('max count: ', move, moves_counter[move])

print(sorted(moves_counter.items(),key=lambda x: x[1]))

unic_move=[]
for move, count in moves_counter.items():
    if count == 1:
        unic_move.append(move)

moves =  load_info(Directory['MOVE_FILE'])

for name, pk in load_info(Directory['POKE_FILE']).items():
    for move in pk['moves']:
        if move in unic_move:
            print (move, name, moves[move]['power'])

"""
"""
# presision
count = 0
count_2 = 0
for name, move in load_info(Directory['MOVE_FILE']).items():
    if move['accuracy'] != None and move['accuracy'] <= 80:
        print('ac: {}, pow: {},'.format( move['accuracy'], move['power']), name)
        count+=1
        if move['power'] != None and move['power'] < 80: count_2+=1
print (count,count_2)
"""
"""
#PPs
count = 0
count_2 = 0
count_3 = 0
print('num of moves = ',len(load_info(Directory['MOVE_FILE'])))
for name, move in load_info(Directory['MOVE_FILE']).items():
    if move['power'] != None and move['power'] > 100: count_3 +=1
    if move['pp'] != None and move['pp'] == 5:
        print('pp: {}, pow: {},'.format( move['pp'], move['power']), name)
        count+=1
        if move['power'] != None and move['power'] < 100: count_2+=1
print( '#PP=5: {}, #PP=5&p<100: {}, p>100: {}'.format(count,count_2,count_3))
"""
"""
#legendarios
for name, pk in load_info(Directory['POKE_FILE']).items():
    st = 0
    for stat in pk['stats']:
        st += pk['stats'][stat]['base_stat']
    st = st /  len(pk['stats'].keys())
    if st > 95:
        print (name.title())

"""
