from Pokemon_python.generator_data_base import generate_pokemons, generate_types, generate_moves

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
