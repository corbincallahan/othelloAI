from OthelloInterface import Othello_AI
from OthelloEngine import get_all_moves
from OthelloEngine import get_adjacencies
import random

class Robothello(Othello_AI):
    def init(self, team_type, board_size=8, time_limit=2.0):
        # team_type will be either 'W' or 'B', indicating what color you are
        # board_size and time_limit will likely stay constant, but if you want this can add different challanges
        self.team_type = team_type
      
    def get_move(self, board_state):
        # board state will be an board_size by board_size array with the current state of the game.
        #       Possible values are: 'W', 'B', or '-'
        # Return your desired move (If invalid, instant loss)
        # Example move: ('W', (1, 6))
        moves = get_all_moves(board_state, self.team_type)
        if len(moves) > 0:
            return choose_move(board_state, moves)
        return None
      
    def get_team_name(self):
        # returns a string containing your team name
        return "Default bot"

def choose_move(board_state, moves): #This is incorrect for now, should be based upon minimax algorithm
    max = 0
    maxIndex = -1
    for i in range(len(moves)):
        new_state = update_board(board_state, moves[i])
        value = evaluate(new_state)
        if(value > max):
            max = value
            maxIndex = i
    return moves[maxIndex]

#Make an minimax function that takes board state, who's turn it is, and depth. Recursively call the function with decreasing depth, utilizing pruning to reduce branching
def minimax(board_state, turn, depth):
    if(turn == 'B'):
        enemy = 'W'
    else:
        enemy = "B"
    for move in get_all_moves(board_state, turn):
        new_state = update_board(board_state, move)
        for oppMove in get_all_moves(new_state, enemy):
            evaluate(new_state, oppMove)

def evaluate(board_state, move):
    return -1

def mobility(board_state, player):
    return len(get_all_moves(board_state, player))

def total_value(board_state, moves):
    sum = 0
    for move in moves:
        sum += evaluate(board_state, move)
    return sum

# def update_board(board_state, move): # Returns the state of the board after a move is made, assumes the move is legal
#     color = move[0]
#     if(color == 'B'):
#         enemy = 'W'
#     else:
#         enemy = 'B'
#     x = move[1][0]
#     y = move[1][1]
#     board_state[x][y] = color
#     for ajacency in get_ajacencies():
#         dx = ajacency[0]
#         dy = ajacency[1]
#         if(board_state[x + dx][y + dy] == enemy):

# Perform move
def update_board(board_state, move): # This is long and ugly and I want to write my own version
    # move format: ('B', (i, j)) or ('B', None)
    # update the board state given the current move
    # if the move is None, do nothing
    # Assume that is a valid move, no need for extra error checking
    if move is not None:
        r = move[1][0]
        c = move[1][1]
        color = move[0]

        #left
        i = r
        j = c - 1
        while j >= 0:
            if board_state[i][j] != color and board_state[i][j] != '-':
                #it's opposite color, keep checking
                j -= 1
            else:
                if board_state[i][j] == color:
                    #it's the same color, go back and change till we are at c-1
                    for index in range(c - j - 1):
                        board_state[i][j + index + 1] = color
                #end the loop
                break

        #left-up direction
        i = r - 1
        j = c - 1
        while i >= 0 and j >= 0:
            if board_state[i][j] != color and board_state[i][j] != '-':
                #it's opposite color, keep checking
                i -= 1
                j -= 1
            else:
                if board_state[i][j] == color:
                    #it's the same color, go back and change till we are at c-1, r-1
                    for index in range(c - j - 1):
                        board_state[i + index + 1][j + index + 1] = color
                #end the loop
                break

        #up
        i = r -1
        j = c
        while i >= 0:
            if board_state[i][j] != color and board_state[i][j] != '-':
                #it's opposite color, keep checking
                i -= 1
            else:
                if board_state[i][j] == color:
                    #it's the same color, go back and change till we are at r-1
                    for index in range(r - i - 1):
                        board_state[i + index + 1][j] = color
                #end the loop
                break

        #right-up direction
        i = r - 1
        j = c + 1
        while i >= 0 and j < len(board_state):
            if board_state[i][j] != color and board_state[i][j] != '-':
                #it's opposite color, keep checking
                i -= 1
                j += 1
            else:
                if board_state[i][j] == color:
                    #it's the same color, go back and change till we are at r-1, c+1
                    for index in range(r - i - 1):
                        board_state[i + index + 1][j - index - 1] = color
                #end loop
                break

        #right direction
        i = r
        j = c + 1
        while j < len(board_state):
            if board_state[i][j] != color and board_state[i][j] != '-':
                #it's opposite color, keep checking
                j += 1
            else:
                if board_state[i][j] == color:
                    #it's the same color, go back and change till we are at c+1
                    for index in range(j - c - 1):
                        board_state[i][j - index - 1] = color
                #end loop
                break

        #right-down
        i = r + 1
        j = c + 1
        while i < len(board_state) and j < len(board_state):
            if board_state[i][j] != color and board_state[i][j] != '-':
                #it's opposite color, keep checking
                i += 1
                j += 1
            else:
                if board_state[i][j] == color:
                    #it's the same color, go back and change till we are at r+1,c+1
                    for index in range(j - c - 1):
                        board_state[i - index - 1][j - index - 1] = color
                #end loop
                break

        #down
        i = r + 1
        j = c
        while i < len(board_state):
            if board_state[i][j] != color and board_state[i][j] != '-':
                #it's opposite color, keep checking
                i += 1
            else:
                if board_state[i][j] == color:
                    #it's the same color, go back and change till we are at r+1
                    for index in range(i - r - 1):
                        board_state[i - index - 1][j] = color
                #end loop
                break

        #left-down
        i = r + 1
        j = c - 1
        while i < len(board_state) and j >= 0:
            if board_state[i][j] != color and board_state[i][j] != '-':
                #it's opposite color, keep checking
                i += 1
                j -= 1
            else:
                if board_state[i][j] == color:
                    #it's the same color, go back and change till we are at r+1
                    for index in range(i - r - 1):
                        board_state[i - index - 1][j + index + 1] = color
                #end loop
                break

        #set the spot in the game_state
        board_state[r][c] = color
    return board_state

game_state = [['-' for i in range(8)] for j in range(8)]
game_state[0][0] = 'W'
game_state[0][1] = 'B'
game_state[0][2] = 'B'
game_state[0][3] = 'B'
game_state[0][4] = 'B'
game_state[0][5] = 'B'
game_state[0][6] = 'B'
game_state[1][1] = 'B'
white_moves = get_all_moves(game_state, 'W')
for move in white_moves:
    x = move[1][0]
    y = move[1][1]
    game_state[x][y] = 'X'
for i in range(len(game_state)):
    print(game_state[i])