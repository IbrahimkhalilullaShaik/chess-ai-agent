import chess
from stockfish import Stockfish

class StockfishAgent:
    def __init__(self, skill_level=10):
        self.engine = Stockfish(
            path="stockfish",
            parameters={
                "Skill Level": skill_level,
                "Threads": 2,
                "Minimum Thinking Time": 30
            }
        )

    def set_skill(self, level: int):
        self.engine.update_engine_parameters({
            "Skill Level": int(level)
        })

    def select_move(self, board: chess.Board):
        self.engine.set_fen_position(board.fen())
        best = self.engine.get_best_move()
        return chess.Move.from_uci(best) if best else None

    def evaluate(self, board: chess.Board):
        self.engine.set_fen_position(board.fen())
        info = self.engine.get_evaluation()

        if info["type"] == "cp":
            return info["value"] / 100.0
        if info["type"] == "mate":
            return 100 if info["value"] > 0 else -100
        return 0.0