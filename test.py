from Configuration.settings import Directory
from Game.engine.core.object_info import load_info

# General imports
from random import randint, sample, choice
from math import floor
from numpy import argmax, amax, max

def get_stats(stats):
    n= ["hp", "attack", "special-attack", "defense", \
        "special-defense", "speed"]
    for stat in n:
        # Formulas:
        # PS: 10 + { Nivel / 100 x [ (Stat Base x 2) + IV + PE/4 ] } + Nivel
        # OTHER:( 5 + { Nivel / 100 x [ (Stat Base x 2) + IV + PE/4 ] } )
        #		x "Naturaleza" --> not used/ not implemented
        st = stats[stat]
        precalc = 31 + floor(st['effort']/4)
        precalc = st['base_stat']*2 + precalc
        precalc = floor(precalc)
        if stat == 'hp': stats[stat]= precalc + 100 + 10
        else: stats[stat]= precalc + 5
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
