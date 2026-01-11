import os
import torch
import chess
from models.neural_net import ChessNet
from engine.state_encoder import StateEncoder


class MLAgent:
    """
    Machine Learning based chess agent.

    - Loads a trained PyTorch model if available
    - If model file is missing (e.g. on Render), disables itself safely
    - Never crashes the backend
    """

    def __init__(self, model_path="models/checkpoints/ml.pth"):
        self.enabled = False
        self.model_path = model_path

        # If model file does not exist, disable ML agent gracefully
        if not os.path.exists(self.model_path):
            print(
                f"[MLAgent] WARNING: Model file not found at "
                f"'{self.model_path}'. ML agent disabled."
            )
            return

        try:
            self.model = ChessNet()
            self.model.load_state_dict(
                torch.load(self.model_path, map_location="cpu")
            )
            self.model.eval()
            self.enabled = True
            print("[MLAgent] ML model loaded successfully.")
        except Exception as e:
            print(f"[MLAgent] ERROR loading model: {e}")
            self.enabled = False

    def select_move(self, board: chess.Board):
        """
        Select the best move according to the ML policy network.
        Returns:
            chess.Move | None
        """

        if not self.enabled:
            return None

        # Encode board state
        state = StateEncoder.encode(board)
        state_tensor = torch.tensor(state, dtype=torch.float32).unsqueeze(0)

        with torch.no_grad():
            policy_logits, _ = self.model(state_tensor)

        legal_moves = list(board.legal_moves)
        if not legal_moves:
            return None

        best_move = None
        best_score = float("-inf")

        for move in legal_moves:
            index = move.from_square * 64 + move.to_square
            score = policy_logits[0, index].item()

            if score > best_score:
                best_score = score
                best_move = move

        return best_move