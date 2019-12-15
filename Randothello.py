from OthelloEngine import get_all_moves
import random

class Othello_AI:
    def __init__(self, team_type, board_size=8, time_limit=2.0):
        self.team_type = team_type

    def get_move(self, board_state):
        moves = get_all_moves(board_state, self.team_type)
        if len(moves) > 0:
            return random.choice(moves)
        return (self.team_type, None)
      
    def get_team_name(self):
        return "Random bot"