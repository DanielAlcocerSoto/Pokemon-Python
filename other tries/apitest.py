import pokebase as pb


charmander = pb.pokemon('charmander')  # Quick lookup.
print (charmander.height)
for m in charmander.moves:
	mo = pb.move(m.move.name)
	print (mo.name)