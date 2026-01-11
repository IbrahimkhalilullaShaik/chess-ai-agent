from engine.board_manager import BoardManager
from agents.random_agent import RandomAgent

class GameController:
    def __init__(self):
        self.board_manager = BoardManager()
        self.ai = RandomAgent()

    def human_move(self, move_uci: str):
        self.board_manager.push_move(move_uci)

        if self.board_manager.is_game_over():
            return None

        ai_move = self.ai.select_move(self.board_manager.board)
        if ai_move:
            self.board_manager.board.push(ai_move)
            return ai_move.uci()

        return None

    def get_fen(self):
        return self.board_manager.get_fen()