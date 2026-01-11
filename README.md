# ♟️ Hybrid Chess AI Agent

A full-stack chess application powered by **Stockfish** and a **Machine Learning agent**, built with a clean, scalable architecture.  
The system combines **rule-based chess logic**, **search-based AI**, and **neural networks** to create a strong, explainable, and extensible chess engine.

---

## 🚀 Features

- 🎮 Interactive web-based chessboard (drag & drop)
- ✅ Fully legal move validation (no illegal moves possible)
- 🤖 **Hybrid AI opponent**
  - Stockfish for openings, tactics, and endgames
  - ML agent for fast, human-like middlegame play
- 📊 Move evaluation with **Good / Inaccuracy / Mistake / Blunder** detection
- ⏪ Undo / Redo support
- 🔁 Game state synchronization between frontend & backend
- 🧠 Machine Learning pipeline trained via **knowledge distillation**
- 🔌 Modular architecture (easy to extend with RL, MCTS, multiplayer)

---

## 🧠 How the AI Works (Simple Explanation)

This project uses **three layers of intelligence**:

### 1️⃣ Chess Rule Engine
All chess rules (legal moves, check, checkmate, castling, etc.) are handled by a dedicated chess rules engine.  
This guarantees **100% correctness**.

### 2️⃣ Stockfish Engine
Stockfish is one of the strongest chess engines in the world.  
It uses classic game-theory algorithms like:
- Minimax
- Alpha–Beta Pruning
- Deep position evaluation

Stockfish is used for:
- Opening play
- Tactical and critical positions
- Endgame play
- Evaluating whether a player move is a blunder

### 3️⃣ Machine Learning Agent (Your Own AI)
A neural network is trained to **imitate Stockfish’s evaluations** using supervised learning.  
This approach is called **knowledge distillation**.

The final AI is **hybrid**:
- Stockfish is used when accuracy is critical
- ML agent is used when fast intuition is sufficient

This results in a strong, fast, and explainable AI opponent.

---

## 🧮 Algorithms Used

- **Minimax with Alpha–Beta Pruning** (via Stockfish)
- **Neural Networks (CNN-based)** for board evaluation
- **Supervised Learning** (ML model learns from Stockfish)
- **Hybrid Decision Logic** (dynamic agent selection)

---

## 🛠️ Technologies & Tools

### Frontend
- React.js
- JavaScript
- HTML5 / CSS3
- Vite (development server)

### Backend
- Python
- FastAPI
- Uvicorn

### AI & ML
- Stockfish (chess engine)
- PyTorch
- NumPy
- python-chess

---

---

## ▶️ How to Run

### Backend
```bash
uvicorn ui.backend.api:app --reload

cd ui/frontend
npm install
npm run dev