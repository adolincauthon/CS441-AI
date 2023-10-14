import argparse
import collections
import copy
import sys

def solve_puzzle(queue: collections.deque):
	'''
	Solves a  instance of a puzzle and displays solution and number of moves required
	:param queue: dequeue instance containing all valid moves from start of puzzle
	'''
	while queue:
		move = queue.popleft()
		if move == True:
			solution = queue.popleft()
			print(f'Found solution in {solution.moves} moves.')
			solution.print_map()
			return True
		for puzz in move.get_next_moves():
			queue.append(puzz)	
	return False

def get_puzzle(file: str) -> dict:
	'''
	Parses file and extracts puzzle into a list, capturing the width of the puzzle.
	:param file: Name of file to extract puzzle fromfound = solve_puzzle(queue)
	:returns
	:raises FileNotFoundException: If the file is not valid
	:returns dict: Contains puzzle instance and width of puzzle
	'''
	lines = []
	with open(file) as data:
		line = data.readline()
		while line != '':
			lines.append(line)
			line = data.readline()
			
	map = []
	width = len(lines[0]) - 1
	for i, line in enumerate(lines):
		if i == 0: 
			continue
		for char in line:
			if char != '\n':
				map.append(char)
	return {'map': map, 'width': width}

class Puzzle:
	'''
	Instance of a bug rush puzzle
	'''
	def __init__(self, puzz: list, moves: int = 0):
		'''
		:param puzz:  List containing an instance of a puzzle
		:param moves: Number of moves this instance is from the starting puzzle 
		'''
		self.map = copy.deepcopy(puzz)
		self.moves = moves

	def __hash__(self):
		'''
		Returns a hash of the puzzle instane
		'''
		return hash(tuple(self.map))

	def swap(self, i, j):
		'''
		Swaps two elements on the board
		:param i: position of element that is being moved
		:param j: position element is being moved to
		'''
		self.map[j] = self.map[i]
		self.map[i] = ' '

	def print_map(self):
		'''
		Prints the puzzle instance
		'''
		for i, char in enumerate(self.map):
			print(char, end='')
			if (i+1) % width == 0 and i != 0:
				print("")
		print("")

	def get_next_moves(self) -> list:
		'''
		Retrieves a list of all the valid next moves
		:returns: List containing all next moves in a puzzle, or a list with True and current instance of puzzle if solved.
		'''
		valid_moves = []
		for i, char in enumerate(self.map):
			if char == '>':
				#right edge of map
				if (i + 1) % width == 0:
					return [True, self]
				
				#not left edge of map
				if i != 0 and (i % width) != 0:
					if self.map[i-1] == ' ':
						new_puzzle = Puzzle(self.map, self.moves+1)
						new_puzzle.swap(i, i-1)
						if hash(new_puzzle) not in visited:
							valid_moves.append(new_puzzle)
							visited.add(hash(new_puzzle))

				if self.map[i+1] == ' ':
						new_puzzle = Puzzle(self.map, self.moves+1)
						new_puzzle.swap(i, i+1)
						if hash(new_puzzle) not in visited:
							valid_moves.append(new_puzzle)
							visited.add(hash(new_puzzle))
				continue
					
			if char == '-':
				#not right edge of map
				if (i + 1) % width != 0:
					if self.map[i+1] == ' ':
						new_puzzle = Puzzle(self.map, self.moves+1)
						new_puzzle.swap(i, i+1)
						if hash(new_puzzle) not in visited:
							valid_moves.append(new_puzzle)
							visited.add(hash(new_puzzle))

				#not left edge of map
				if i != 0 and (i % width) != 0:
					if self.map[i-1] == ' ':
						new_puzzle = Puzzle(self.map, self.moves+1)
						new_puzzle.swap(i, i-1)
						if hash(new_puzzle) not in visited:
							valid_moves.append(new_puzzle)
							visited.add(hash(new_puzzle))
				continue


			if char == '|':
				#Not top of map
				if not (i - width < 0):
					if self.map[i-width] == ' ':
						new_puzzle = Puzzle(self.map, self.moves+1)
						new_puzzle.swap(i, i-width)
						if hash(new_puzzle) not in visited:
							valid_moves.append(new_puzzle)
							visited.add(hash(new_puzzle))

				#not bottom of graph			
				if not ((i + width) > (len(self.map) -1)):
					if self.map[i+width] == ' ':
						new_puzzle = Puzzle(self.map, self.moves+1)
						new_puzzle.swap(i, i+width)
						if hash(new_puzzle) not in visited:
							valid_moves.append(new_puzzle)
							visited.add(hash(new_puzzle))

		return valid_moves


parser = argparse.ArgumentParser(prog='bugrush', description='Solves instances of a bug rush puzzle.')
parser.add_argument('file', type=str, help='File containing the bug rush puzzle')
args = parser.parse_args()

#Create FIFO queue
queue = collections.deque()

#create set of visited positions
visited = set()

#parse puzzle
try:
	data = get_puzzle(args.file)
except FileNotFoundError:
	print(f'{args.file} does not exist')
	sys.exit()

width = data.get('width')
puzzle = Puzzle(data.get('map'))
visited.add(hash(puzzle))
print('Original Puzzle: ')
puzzle.print_map()
moves = puzzle.get_next_moves()



if moves[0] == True:
		print('Puzzled solved in 0 steps')
for move in moves:
	queue.append(move)

found = solve_puzzle(queue)

if found == False:
	print('unsat')
