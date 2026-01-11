import torch
import chess
import numpy as np
from models.neural_net import ChessNet
from engine.state_encoder import StateEncoder

class MLAgent:
    def __init__(self, model_path="models/checkpoints/ml.pth"):
        self.model = ChessNet()
        self.model.load_state_dict(torch.load(model_path))
        self.model.eval()

    def select_move(self, board: chess.Board):
        state = StateEncoder.encode(board)
        state = torch.tensor(state).unsqueeze(0)

        with torch.no_grad():
            policy, _ = self.model(state)

        legal_moves = list(board.legal_moves)
        if not legal_moves:
            return None

        move_scores = {}
        for move in legal_moves:
            idx = self._move_to_index(move)
            move_scores[move] = policy[0, idx].item()

        return max(move_scores, key=move_scores.get)

    def _move_to_index(self, move):
        return move.from_square * 64 + move.to_square