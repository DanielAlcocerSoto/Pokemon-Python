#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Module that contains the Song class.
This class allows to play a  random background therme song.

It contains the following class:

	Song
"""

# Local imports
from Configuration.settings import Directory,  Music_Config

# 3rd party imports
from pygame.mixer import music

# General imports
from random import choice

__version__ = '0.7'
__author__  = 'Daniel Alcocer (daniel.alcocer@est.fib.upc.edu)'


"""
    Class to play a song.
"""
class Song:
    def __init__(self):
        """
            Args: -

            Action:
                Create a Song that can be played.
        """
        name_song = choice(Music_Config['NAME_MUSIC'])+'_'+\
					choice(Music_Config['NAME_GEN'])
        music.load(Directory['DIR_MUSIC']+name_song+Music_Config['EXTENSION'])
        music.set_volume(Music_Config['VOLUME']/100)

    """
        Funcion to play the song.
    """
    def play(self):
        music.play(-1)
