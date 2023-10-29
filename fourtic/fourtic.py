import argparse
import copy


def read_board(board_name: str) -> list: 
	with open(board_name, 'r') as file:
		raw_board = file.read().splitlines()
	print(raw_board)
	board = [list(line) for line in raw_board]
	print(board)
	return board

def add_tuples(x, y):
	return (x[0] + y[0], x[1]+y[1])

def score_move(move):
	if move == MAX:
		return (1, 0)
	elif move == MIN:
		return (0, 1)
	return (0, 0)

def score_line(row):
	'''
	Scores a set of moves
	'''
	MAX_score = 0
	MIN_score = 0
	for move in row:
		if move == MAX:
			MAX_score = MAX_score + 1
			if MIN_score < 3:
				MIN_score = 0
		elif move == MIN:
			MIN_score = MIN_score + 1
			if MAX_score < 3:
				MAX_score = 0

	
	if MAX_score == 3:
		return (3, 0)
	elif MAX_score == 4:
		return (6, 0)
	if MIN_score == 3:
		return (0, 3)
	elif MIN_score == 4:
		return (0, 6)
	return (0, 0)
	
def score_edges(board):
	score = (0, 0)
	#score top and bottom
	for move in board[0]:
		score = add_tuples(score, score_move(move))
	for move in board[3]:
		score = add_tuples(score, score_move(move))

	#middle edges
	score = add_tuples(score, score_move(board[1][0])) 
	score = add_tuples(score, score_move(board[2][0])) 
	score = add_tuples(score, score_move(board[1][3])) 
	score = add_tuples(score, score_move(board[2][3])) 
	return score

def score_board(board) -> int:
	score = (0,0)
	#rows
	for row in board:
		score = add_tuples(score, score_line(row))
	#columns
	for i in range(4):
		score = add_tuples(score, score_line([board[0][i], board[1][i], board[2][i], board[3][i]]))
	#diags
	score = add_tuples(score, score_line([board[0][1], board[1][2], board[2][3]]))
	score = add_tuples(score, score_line([board[1][0], board[2][1], board[3][2]]))

	score = add_tuples(score, score_line([board[0][0], board[1][1], board[2][2], board[3][3]]))
	score = add_tuples(score, score_line([board[3][0], board[2][1], board[1][2], board[0][3]]))

	score = add_tuples(score, score_line([board[1][3], board[2][2], board[3][1]]))
	score = add_tuples(score, score_line([board[2][0], board[1][1], board[0][2]]))

	score = add_tuples(score, score_edges(board))
	return score
	
def valid_moves(board):
	moves = []
	for i, row in enumerate(board):
		for j, move in enumerate(board[i]):
			if move == '.':
				moves.append((i,j))
	return moves

def first_move(board):
	dots = 0
	for row in board:
		for spot in row:
			if spot == '.':
				dots = dots + 1
	if dots % 2 == 0:
		return 'X'
	return 'O'


def minimax(board, player, opponent):
	moves = valid_moves(board)

	if len(moves) == 0:
		final_children.append(copy.deepcopy(board))
		scores = score_board(board)
		final_scores.append(scores)
		return scores[0] - scores[1]
	
	max_score = -9999
	min_score = 9999

	for move in moves:
		board[move[0]][move[1]] = player
		score = minimax(board, opponent, player)
		board[move[0]][move[1]] = '.'
		if score > max_score:
			max_score = score
		if score < min_score:
			min_score = score

	if player == MAX:
		return max_score
	return min_score


MAX = 'X'
MIN = 'O'

parser = argparse.ArgumentParser(prog='fourtic.py', description='Solves instances of fourtic.')
parser.add_argument('file', type=str, help='File containing the bug rush puzzle')
args = parser.parse_args()
equal_score = score_board([['O', 'O', 'X', 'X'],['O', 'O', 'X', 'X'],['O', 'O', 'X', 'X'],['O', 'O', 'X', 'X']])
assert equal_score == (18,18)
starting_board = read_board(args.file)
player = first_move(starting_board)
opponent = 'O'
if player == 'O':
	opponent = 'X'
final_children = []
final_scores = []
result = minimax(starting_board, player, opponent)
if player == MIN:
	result = -result
print(f'{player} {result}')



	