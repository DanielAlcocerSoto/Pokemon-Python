#!/usr/bin/python3
# -*- coding: utf-8 -*-

from urllib.request import urlopen
from bs4 import BeautifulSoup

WIKI = 'http://es.pokemon.wikia.com'
URL = WIKI+'/wiki/Primera_generaci%C3%B3n'
GEN = 4

def rootOf(url):
	return BeautifulSoup(urlopen(url), 'html.parser')

def getTypes(pokeHTML):
	try:
		ty = pokeHTML.find('aside')('section')[3].find_all('div', attrs = {'class':'pi-item pi-data pi-item-spacing pi-border-color'})[2].div
	except : #Charmander
		ty = pokeHTML('div',  attrs={'class':'pi-data-value pi-font'})[2]

	Types = [t.get('title').split(' ')[1] for t in ty('a') if t.get('title') != None]#if por las referencias
	return Types

def getStats(pokeHTML):
	table = pokeHTML.find('table', attrs={'class':'estadisticas'})
	def getRow(idx): return [int(pe.text[1:-1].split(' ')[0]) for pe in table('tr')[idx]('td')]
	PE = getRow(1)
	Base = getRow(2)
	Max = getRow(4)
	return (PE,Base,Max)

def getMoves(pokeHTML): #4ª gen
	table1 = pokeHTML.find('table', attrs={'class':'movnivel'})
	mov1 = [row('td')[8].text[1:-1] for row in table1('tr')[1:] if len(row('td')[GEN-1].text) != 1 ]
	try : #maybe pk not can learn MT
		table2 = pokeHTML.find('div', attrs={'class':'tabbertab', 'title':str(GEN)+'ª gen.'}).table
		mov2 = [row('td')[1].a.get('title') for row in table2('tr')[1:] ]
	except:
		mov2 = []

	return list(set(mov1+mov2))

def getInfoOf(poke):
	pokeHTML = rootOf(WIKI+poke)
	types = getTypes(pokeHTML)
	PE,Base,Max = getStats(pokeHTML)
	moves = getMoves(pokeHTML)
	return (types,PE,Base,Max,moves)

def createPokemonDB ():
	table = rootOf(URL).find('table', attrs={'class':'tabpokemon'})
	file = open('pokemon.db', 'w')
	for pk in table('tr')[1:]:
		pkID = pk('td')[0].text[1:-1]
		poke = pk('td')[1].a.get('href')
		print(pkID, poke)
		types,PE,Base,Max,moves = getInfoOf(poke)
		info="ID:"+pkID+"~Types:"+str(types)+"~PE:"+str(PE)+"~Base"+str(Base)+"~Max"+str(Max)+"~Moves:"+str(moves)
		if pkID != '001': file.write('\n'+info)
		else: file.write(info)
		#print (info)
	file.close() 

createPokemonDB()
#getInfoOf('/wiki/Mewtwo')
#/wiki/Charmander
#/wiki/Caterpie
#/wiki/Nidoking 
#/wiki/Clefairy
#/wiki/Mewtwo

	
	
	
	
