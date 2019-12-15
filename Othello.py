#from OthelloInterface import Othello_AI
from OthelloEngine import get_all_moves
from OthelloEngine import get_adjacencies
import random

class Othello_AI:
    def __init__(self, team_type, board_size=8, time_limit=2.0):
        # team_type will be either 'W' or 'B', indicating what color you are
        # board_size and time_limit will likely stay constant, but if you want this can add different challanges
        self.team_type = team_type
        if(team_type == 'B'):
            self.enemy = 'W'
        else:
            self.enemy = 'B'
      
    def get_move(self, board_state):
        # board state will be an board_size by board_size array with the current state of the game.
        #       Possible values are: 'W', 'B', or '-'
        # Return your desired move (If invalid, instant loss)
        # Example move: ('W', (1, 6))
        moves = get_all_moves(board_state, self.team_type)
        if len(moves) > 0:
            return self.choose_move(board_state, moves)
        return None
      
    def get_team_name(self):
        # returns a string containing your team name
        return "Last place"

    def choose_move(self, board_state, moves):
        max = float("-inf")
        maxIndex = -1
        for i in range(len(moves)):
            new_board = update_board(board_state, moves[i])
            node = self.minimax(new_board, 6, float("-inf"), float("inf"), False) # Wrong?
            if(node > max):
                maxIndex = i
                max = node
        return moves[maxIndex]

    # Credit to Sebastian Lague for the psuedocode of this function, https://www.youtube.com/watch?v=l-hh51ncgDI
    # Call with maximizingPlay as true when turn == self.team_type
    def minimax(self, position, depth, alpha, beta, maximizingPlayer):
        if depth == 0:
            return evaluate(position, self.team_type) # Should this be called with team_type?

        endgame = check_end(position)
        if endgame:
            if(endgame == self.team_type):
                return float("inf")
            if(endgame == self.enemy):
                return float("-inf")
            return 0 # ??? How should tying be considered? Not likely to occur, but useful
    
        if maximizingPlayer:
            maxEval = float("-inf")
            for child in get_all_moves(position, self.team_type):
                eval = self.minimax(child, depth - 1, alpha, beta, False)
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return maxEval
        else:
            minEval = float("inf")
            for child in get_all_moves(position, self.enemy):
                eval = self.minimax(child, depth - 1, alpha, beta, True)
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return minEval

# Returns higher values when board_state favors the player
def evaluate(board_state, player):
    return sum(row.count(player) for row in board_state)
    # moveNumber = getMoveNumber(board_state)
    # esac = ESAC(moveNumber)
    # eStab = edgeStability(board_state, player)
    # iStab = internalStability(board_state, player)
    # cmac = CMAC(moveNumber)
    # cMob = currentMobility(board_state, player)
    # pMob = potentialMobility(board_state, player)
    # return esac * eStab + 36 * iStab + cmac * cMob + 99 * pMob

def check_end(board_state):
      # Check the board to see if the game can continue
      # If the game is over return the winner: 'W', 'B', or 'T'
      # Otherwise, return None

      if len(get_all_moves(board_state, 'W')) != 0 or len(get_all_moves(board_state, 'B')) != 0:
         return None

      white_count = sum(row.count('W') for row in board_state)
      black_count = sum(row.count('B') for row in board_state)

      if white_count == black_count:
         return 'T'
      elif white_count > black_count:
         return 'W'
      else:
         return'B'

def mobility(board_state, player):
    return len(get_all_moves(board_state, player))

def total_value(board_state, moves, team):
    sum = 0
    for move in moves:
        sum += evaluate(update_board(board_state, move), team)
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
def update_board(board_state, move): # This is long and I want to write my own version
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

def getMoveNumber(board_state):
    return 61 - sum(row.count('-') for row in board_state)

# These functions come from Rosenbloom's paper on IAGO
def ESAC(moveNumber):
    return 6.24 * moveNumber + 312

def CMAC(moveNumber):
    if(moveNumber < 26):
        return 2 * moveNumber + 50
    else:
        return moveNumber + 75

def edgeStability(board_state, player):
    pass

def internalStability(board_state, player):
    pass

def currentMobility(board_state, player):
    pass

def potentialMobility(board_state, player):
    pass

# game_state = [['-' for i in range(8)] for j in range(8)]
# game_state[0][0] = 'W'
# game_state[0][1] = 'B'
# game_state[0][2] = 'B'
# game_state[0][3] = 'B'
# game_state[0][4] = 'B'
# game_state[0][5] = 'B'
# game_state[0][6] = 'B'
# game_state[1][1] = 'B'
# white_moves = get_all_moves(game_state, 'W')
# for move in white_moves:
#     x = move[1][0]
#     y = move[1][1]
#     game_state[x][y] = 'X'
# for i in range(len(game_state)):
#     print(game_state[i])