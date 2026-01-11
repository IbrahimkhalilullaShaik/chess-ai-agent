import chess

class BoardManager:
    def __init__(self):
        self.board = chess.Board()

    def push_move(self, move_uci: str):
        move = chess.Move.from_uci(move_uci)
        if move not in self.board.legal_moves:
            raise ValueError("Illegal move")
        self.board.push(move)

    def get_fen(self):
        return self.board.fen()

    def is_game_over(self):
        return self.board.is_game_over()