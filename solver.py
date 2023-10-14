import collections
import copy

def solve_puzzle(queue):
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

def get_puzzle(file):
	lines = []
	with open(file) as data:
		line = data.readline()
		while line != '':
			lines.append(line)
			line = data.readline()
	height = len(lines)-1
			
	map = []
	width = len(lines[0]) - 1
	for i, line in enumerate(lines):
		for char in line:
			if char != '\n':
				map.append(char)
	return {'map': map, 'width': width, 'height': height}

class Puzzle:
	def __init__(self, puzz, moves=0):
		self.map = copy.deepcopy(puzz)
		self.moves = moves

	def __hash__(self):
		return hash(tuple(self.map))

	def swap(self, i, j):
		self.map[j] = self.map[i]
		self.map[i] = ' '
		return

	def print_map(self):
		for i, char in enumerate(self.map):
			print(char, end='')
			if (i+1) % width == 0 and i != 0:
				print("")
		print("")

	def get_next_moves(self) -> list:
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
				if i != 0 and (width % i) != 0:
					if self.map[i-1] == ' ':
						new_puzzle = Puzzle(self.map, self.moves+1)
						new_puzzle.swap(i, i-1)
						if hash(new_puzzle) not in visited:
							valid_moves.append(new_puzzle)
							visited.add(hash(new_puzzle))


			if char == '|':
				#Not top of map
				if  not (i - width < 0):
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


queue = collections.deque()
visited = set()
found = False
data = get_puzzle('unsat5x7.bugs')
width = data.get('width')
height = data.get('height')
puzzle = Puzzle(data.get('map'))
visited.add(hash(puzzle))
puzzle.print_map()
moves = puzzle.get_next_moves()



if moves[0] == True:
		print('Puzzled solved in 0 steps')
for move in moves:
	queue.append(move)

found = solve_puzzle(queue)

if found == False:
	print('unsat')
