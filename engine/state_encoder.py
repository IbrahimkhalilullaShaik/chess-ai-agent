import chess
import numpy as np

class StateEncoder:
    @staticmethod
    def encode(board: chess.Board):
        planes = np.zeros((12, 8, 8), dtype=np.float32)

        piece_map = {
            chess.PAWN: 0,
            chess.KNIGHT: 1,
            chess.BISHOP: 2,
            chess.ROOK: 3,
            chess.QUEEN: 4,
            chess.KING: 5
        }

        for square, piece in board.piece_map().items():
            idx = piece_map[piece.piece_type]
            if piece.color == chess.BLACK:
                idx += 6
            row = 7 - (square // 8)
            col = square % 8
            planes[idx, row, col] = 1

        return planes