import React, { useState } from "react";
import ChessBoard from "./components/chessboard";

const API = "http://127.0.0.1:8000";

const App = () => {
  const [status, setStatus] = useState("Your move");
  const [analysis, setAnalysis] = useState("");

  return (
    <div style={styles.page}>
      <h1>Chess AI</h1>
      <p>{status}</p>
      <p style={styles.analysis}>{analysis}</p>

      <ChessBoard
        onStatusChange={setStatus}
        onMoveResult={(data) => {
          if (data.judgement) {
            setAnalysis(`${data.judgement} (Eval: ${data.evaluation})`);
          }
        }}
      />
    </div>
  );
};

const styles = {
  page: {
    minHeight: "100vh",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    fontFamily: "Arial"
  },
  analysis: {
    fontWeight: "bold",
    color: "red"
  }
};

export default App;