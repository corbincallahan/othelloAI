from OthelloEngine import get_all_moves
import random

class Othello_AI:
    def __init__(self, team_type, board_size=8, time_limit=2.0):
        self.team_type = team_type
        if(team_type == 'B'):
            self.enemy = 'W'
        else:
            self.enemy = 'B'

    def get_move(self, board_state):
        moves = get_all_moves(board_state, self.team_type)
        if len(moves) > 0:
            return random.choice(moves)
        return (self.team_type, None)
      
    def get_team_name(self):
        return "Min bot"

    def choose_move(self, board_state, moves):
        max = float("-inf")
        maxIndex = -1
        # if(getMoveNumber(board_state) > 47):
        #     depth = 60
        # else:
        #     depth = 6
        for i in range(len(moves)):
            new_board = update_board(board_state.copy(), moves[i])
            node = self.minimax(new_board, 6, float("-inf"), float("inf"), False)
            if(node > max):
                maxIndex = i
                max = node
        return moves[maxIndex]

    # Credit to Sebastian Lague for the psuedocode of this function, https://www.youtube.com/watch?v=l-hh51ncgDI
    # Call with maximizingPlay as true when turn == self.team_type
    def minimax(self, position, depth, alpha, beta, maximizingPlayer):
        if depth == 0:
            return self.evaluate(position)

        endgame = check_end(position)
        if endgame:
            if(endgame == self.team_type):
                return float("inf")
            if(endgame == self.enemy):
                return float("-inf")
            return 0 # ??? How should tying be considered? Not likely to occur, but useful
    
        if maximizingPlayer:
            maxEval = float("-inf")
            for move in get_all_moves(position, self.team_type):
                child = update_board(position.copy(), move)
                eval = self.minimax(child, depth - 1, alpha, beta, False)
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return maxEval
        else:
            minEval = float("inf")
            for move in get_all_moves(position, self.enemy):
                child = update_board(position.copy(), move)
                eval = self.minimax(child, depth - 1, alpha, beta, True)
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return minEval

    # Returns higher values when board_state favors the player
    def evaluate(self, board_state):
        return sum([row.count(self.enemy) for row in board_state]) - sum([row.count(self.team_type) for row in board_state])

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