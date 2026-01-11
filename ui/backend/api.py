from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import chess

from agents.stockfish_agent import StockfishAgent
from agents.ml_agent import MLAgent

app = FastAPI()

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- GAME ----------------
class Game:
    def __init__(self):
        self.board = chess.Board()

        # Hybrid AI
        self.ml_ai = MLAgent()
        self.sf_ai = StockfishAgent(skill_level=12)

        self.history = []
        self.redo_stack = []

    # -------- MOVE MANAGEMENT --------
    def push(self, move):
        self.board.push(move)
        self.history.append(move)
        self.redo_stack.clear()

    def undo(self):
        if self.history:
            m = self.history.pop()
            self.board.pop()
            self.redo_stack.append(m)

    # -------- HYBRID AI LOGIC --------
    def select_ai_move(self):
        # Opening phase → Stockfish
        if self.board.fullmove_number <= 8:
            return self.sf_ai.select_move(self.board)

        # Critical positions → Stockfish
        if self.board.is_check():
            return self.sf_ai.select_move(self.board)

        # Endgame (very rough heuristic) → Stockfish
        if len(self.board.piece_map()) <= 10:
            return self.sf_ai.select_move(self.board)

        # Middlegame → ML agent
        return self.ml_ai.select_move(self.board)

game = Game()

# ---------------- MODELS ----------------
class MoveRequest(BaseModel):
    move: str  # e.g. "e2e4"

class LegalMoveRequest(BaseModel):
    square: str  # e.g. "e2"

# ---------------- HELPERS ----------------
def classify_blunder(before, after):
    diff = after - before
    if diff <= -3.0:
        return "Blunder"
    if diff <= -1.5:
        return "Mistake"
    if diff <= -0.5:
        return "Inaccuracy"
    return "Good"

# ---------------- ENDPOINTS ----------------
@app.get("/state")
def state():
    return {"fen": game.board.fen()}

@app.post("/move")
def move(req: MoveRequest):
    try:
        # Evaluation before move (Stockfish only)
        before_eval = game.sf_ai.evaluate(game.board)

        move = chess.Move.from_uci(req.move)
        if move not in game.board.legal_moves:
            return {"error": "illegal"}

        captured = game.board.is_capture(move)
        game.push(move)

        # Evaluation after move
        after_eval = game.sf_ai.evaluate(game.board)
        judgement = classify_blunder(before_eval, after_eval)

        # AI response
        ai_move = None
        if not game.board.is_game_over():
            ai_move = game.select_ai_move()
            if ai_move:
                game.push(ai_move)

        return {
            "fen": game.board.fen(),
            "ai_move": ai_move.uci() if ai_move else None,
            "evaluation": after_eval,
            "judgement": judgement,
            "captured": captured
        }

    except Exception as e:
        return {"error": str(e)}

@app.post("/legal_moves")
def legal_moves(req: LegalMoveRequest):
    try:
        sq = chess.parse_square(req.square)
    except ValueError:
        return {"moves": []}

    return {
        "moves": [
            chess.square_name(m.to_square)
            for m in game.board.legal_moves
            if m.from_square == sq
        ]
    }

@app.post("/undo")
def undo():
    # Undo AI move
    if game.history:
        game.undo()
    # Undo player move
    if game.history:
        game.undo()
    return {"fen": game.board.fen()}

@app.post("/redo")
def redo():
    if game.redo_stack:
        m = game.redo_stack.pop()
        game.board.push(m)
        game.history.append(m)
    if game.redo_stack:
        m = game.redo_stack.pop()
        game.board.push(m)
        game.history.append(m)
    return {"fen": game.board.fen()}

@app.post("/skill")
def skill(data: dict):
    level = int(data.get("level", 12))
    game.sf_ai.set_skill(level)
    return {"level": level}

@app.post("/reset")
def reset():
    global game
    game = Game()
    return {"status": "reset"}