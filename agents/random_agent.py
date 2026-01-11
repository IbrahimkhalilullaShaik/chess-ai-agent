import random
import chess

class RandomAgent:
    def select_move(self, board: chess.Board):
        moves = list(board.legal_moves)
        return random.choice(moves) if moves else None