import torch
import chess
import chess.pgn
from models.neural_net import ChessNet
from engine.state_encoder import StateEncoder
from agents.stockfish_agent import StockfishAgent

class SupervisedTrainer:
    def __init__(self):
        self.model = ChessNet()
        self.engine = StockfishAgent(skill_level=20)
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=1e-3)
        self.loss_fn = torch.nn.MSELoss()

    def train(self, pgn_path, epochs=1):
        for _ in range(epochs):
            with open(pgn_path) as pgn:
                while game := chess.pgn.read_game(pgn):
                    board = game.board()
                    for move in game.mainline_moves():
                        state = StateEncoder.encode(board)
                        eval_score = self.engine.evaluate(board)

                        x = torch.tensor(state).unsqueeze(0)
                        target = torch.tensor([[eval_score]])

                        _, value = self.model(x)
                        loss = self.loss_fn(value, target)

                        self.optimizer.zero_grad()
                        loss.backward()
                        self.optimizer.step()

                        board.push(move)

        torch.save(self.model.state_dict(), "models/checkpoints/ml.pth")
print("Model saved to models/checkpoints/ml.pth")