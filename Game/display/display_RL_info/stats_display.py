#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Module that contains the Stats_display class.
This class is the principal class to disply stats.

It contains the following classes:

	Stats_display
    Stats_view
"""

# Local imports
from Configuration.settings import Directory, Display_Config, Battle_Config
from Game.display.image import Image, Display
from Game.display.utils_display import scale, shift
from Game.display.font import Font

__version__ = '0.5'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'


"""
	Class to display stats of all pokemon in battle.
"""
class Stats_display(Display):
    def __init__(self, state):
        """
            Args:
                state ('dict of class:Pokemon'): A dictionary with all the
												 information needed to display
												 the a battle.

			Action:
				Create a display to show the moves of 'pokemon'.
		"""
        size = Display_Config['BATTLE_SIZE']
        visualize_items = [ Image(Directory['WATCH_STATS'], (size[0],0)),
            Stats_view(state['Ally_0'], Battle_Config['POS_STATS_A1']),
            Stats_view(state['Ally_1'], Battle_Config['POS_STATS_A2']),
            Stats_view(state['Foe_0'], Battle_Config['POS_STATS_F1']),
            Stats_view(state['Foe_1'], Battle_Config['POS_STATS_F2'])
        ]
        Display.__init__(self, visualize_items)

"""
	Class to display stats of a pokemon.
"""
class Stats_view(Display):
    def __init__(self, pokemon, top_left_pos):
        """
            Args:
                pokemon (class:'Pokemon'): The pokemon which stats will be
                                           displayed.

			Action:
				Display all stats of 'pokemon'.
		"""
        self.pokemon=pokemon
        top_left_pos = shift( (Display_Config['BATTLE_SIZE'][0],0), top_left_pos)
        #name
        text = Font(top_left_pos,Battle_Config['SHIFT_STAT_NAME'])
        text.set_text(pokemon.name(),'BLACK')
        visualize_items = [text]
        #stats
        x,y = Battle_Config['SHIFT_STAT_VALUE']
        self.hp = Font(top_left_pos,(x,y))
        y+=Battle_Config['INTERLINE_VALUE']
        n= ["attack", "special-attack", "defense", "special-defense", "speed"]
        for stat in n:
            text = Font(top_left_pos,(x,y))
            text.set_text(str(pokemon.get_stat(stat)),'BLACK')
            visualize_items.append(text)
            y+=Battle_Config['INTERLINE_VALUE']
        #types
        pattern = Directory['TYPE_IMG_NAME']
        types = [t.name() for t in pokemon.types()]
        for i,t in enumerate(types):
            path = pattern.format(t.lower())
            pos = shift(top_left_pos, Battle_Config['SHIFT_STAT_TYPE_'+str(i)])
            visualize_items.append(Image(path,pos))

        Display.__init__(self, visualize_items)

    """
        Funcion to display info of a pokemon.
    """
    def display(self,SCREEN):
        Display.display(self,SCREEN)
        self.hp.set_text(str(self.pokemon.health())+'/'+\
                        str(self.pokemon.get_stat("hp")),'BLACK')
        self.hp.display(SCREEN)
