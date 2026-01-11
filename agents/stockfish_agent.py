import chess
from stockfish import Stockfish
import os

class StockfishAgent:
    def __init__(self, skill_level=12):
        self.stockfish = Stockfish(
            path=os.getenv("STOCKFISH_PATH", "stockfish")
        )
        self.set_skill(skill_level)

    def set_skill(self, level):
        self.stockfish.update_engine_parameters({
            "Skill Level": int(level)
        })

    def select_move(self, board):
        self.stockfish.set_fen_position(board.fen())
        move = self.stockfish.get_best_move()
        return None if move is None else board.parse_uci(move)

    def evaluate(self, board):
        self.stockfish.set_fen_position(board.fen())
        eval = self.stockfish.get_evaluation()
        if eval["type"] == "cp":
            return eval["value"] / 100.0
        return 0