import React, { useEffect, useState } from "react";

const API_URL = "http://127.0.0.1:8000";
const SQUARE = 80;

/* Unicode pieces */
const PIECE_MAP = {
  r: "♜", n: "♞", b: "♝", q: "♛", k: "♚", p: "♟",
  R: "♖", N: "♘", B: "♗", Q: "♕", K: "♔", P: "♙"
};

/* Themes */
const THEMES = {
  light: ["#eeeed2", "#769656"],
  dark: ["#b58863", "#3c3c3c"],
  wood: ["#f0d9b5", "#b58863"]
};

/* Sounds */
const moveSound = new Audio("/sounds/move.mp3");
const captureSound = new Audio("/sounds/capture.mp3");

const ChessBoard = ({ onStatusChange, onMove, flipped }) => {
  const [board, setBoard] = useState([]);
  const [turn, setTurn] = useState("w");
  const [dragFrom, setDragFrom] = useState(null);
  const [legalMoves, setLegalMoves] = useState([]);
  const [lastMove, setLastMove] = useState(null);
  const [theme, setTheme] = useState("light");

  /* Load board */
  useEffect(() => {
    fetch(`${API_URL}/state`)
      .then(r => r.json())
      .then(d => updateFromFEN(d.fen));
  }, []);

  const updateFromFEN = (fen) => {
    const parts = fen.split(" ");
    setTurn(parts[1]);

    const rows = parts[0].split("/").map(row => {
      const a = [];
      for (let c of row) isNaN(c) ? a.push(c) : a.push(...Array(+c).fill(""));
      return a;
    });

    setBoard(rows);
  };

  /* Backend-driven legal moves */
  const fetchLegalMoves = async (r, c) => {
    const square =
      `${String.fromCharCode(97 + c)}${8 - r}`;

    const res = await fetch(`${API_URL}/legal_moves`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ square })
    });

    const data = await res.json();
    setLegalMoves(
      data.moves.map(m => ({
        r: 8 - Number(m[1]),
        c: m.charCodeAt(0) - 97
      }))
    );
  };

  const sendMove = async (from, to) => {
    const move =
      `${String.fromCharCode(97 + from.c)}${8 - from.r}` +
      `${String.fromCharCode(97 + to.c)}${8 - to.r}`;

    onStatusChange("AI thinking...");
    setLegalMoves([]);

    const r = await fetch(`${API_URL}/move`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ move })
    });

    const d = await r.json();
    if (d.error) return onStatusChange("Illegal move");

    d.captured ? captureSound.play() : moveSound.play();

    updateFromFEN(d.fen);
    setLastMove({ from, to });
    onMove(move);
    if (d.ai_move) onMove(d.ai_move);

    onStatusChange("Your move");
  };

  const square = (r, c) => {
    const p = board[r]?.[c];
    const dark = (r + c) % 2;
    const colors = THEMES[theme];

    const isLast =
      lastMove &&
      ((lastMove.from.r === r && lastMove.from.c === c) ||
       (lastMove.to.r === r && lastMove.to.c === c));

    const isLegal = legalMoves.some(m => m.r === r && m.c === c);

    return (
      <div
        key={`${r}-${c}`}
        onDragOver={e => e.preventDefault()}
        onDrop={() => dragFrom && sendMove(dragFrom, { r, c })}
        style={{
          ...styles.square,
          background: isLast
            ? "#f6f669"
            : colors[dark]
        }}
      >
        {isLegal && <div style={styles.dot} />}
        {p && (
          <span
            draggable
            onDragStart={() => {
              setDragFrom({ r, c });
              fetchLegalMoves(r, c);
            }}
            style={styles.piece}
          >
            {PIECE_MAP[p]}
          </span>
        )}
      </div>
    );
  };

  const rows = flipped ? [...board].reverse() : board;

  return (
    <div style={styles.center}>
      {/* Theme selector */}
      <select value={theme} onChange={e => setTheme(e.target.value)}>
        <option value="light">Light</option>
        <option value="dark">Dark</option>
        <option value="wood">Wood</option>
      </select>

      <div style={styles.board}>
        {rows.map((row, r) =>
          row.map((_, c) =>
            square(flipped ? 7 - r : r, c)
          )
        )}
      </div>
    </div>
  );
};

const styles = {
  center: {
    minHeight: "100vh",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    gap: "12px"
  },
  board: {
    display: "grid",
    gridTemplateColumns: `repeat(8, ${SQUARE}px)`,
    gridTemplateRows: `repeat(8, ${SQUARE}px)`,
    border: "3px solid #333",
    boxShadow: "0 10px 30px rgba(0,0,0,0.3)"
  },
  square: {
    width: SQUARE,
    height: SQUARE,
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    position: "relative"
  },
  piece: {
    fontSize: "56px",
    cursor: "grab",
    userSelect: "none"
  },
  dot: {
    width: 14,
    height: 14,
    borderRadius: "50%",
    background: "rgba(0,0,0,0.35)",
    position: "absolute"
  }
};

export default ChessBoard;