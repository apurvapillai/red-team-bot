import { useState } from "react";

export default function App() {
  const [idea, setIdea] = useState("");
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [round, setRound] = useState(1);

  const submit = async () => {
    if (!idea.trim()) return;
    setLoading(true);

    const res = await fetch("http://localhost:8000/redteam", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ idea, round, history }),
    });

    const data = await res.json();

    const newHistory = [
      ...history,
      { role: "user", content: idea },
      { role: "assistant", content: data.response },
    ];

    setHistory(newHistory);
    setRound(round + 1);
    setIdea("");
    setLoading(false);
  };

  return (
    <div style={{ maxWidth: 700, margin: "40px auto", fontFamily: "monospace", padding: 20 }}>
      <h1 style={{ color: "#e53e3e" }}>=4 Red Team Bot</h1>
      <p style={{ color: "#666" }}>Submit your idea. We will destroy it.</p>

      <div style={{ marginBottom: 20 }}>
        {history.map((msg, i) => (
          <div key={i} style={{
            background: msg.role === "user" ? "#f0f0f0" : "#1a1a1a",
            color: msg.role === "user" ? "#000" : "#00ff00",
            padding: 16,
            marginBottom: 10,
            borderRadius: 8,
            whiteSpace: "pre-wrap"
          }}>
            <strong>{msg.role === "user" ? "YOU" : "RED TEAM"}:</strong>
            <br />{msg.content}
          </div>
        ))}
      </div>

      <textarea
        value={idea}
        onChange={e => setIdea(e.target.value)}
        placeholder={round === 1 ? "Describe your idea, plan, or argument..." : "Defend yourself or submit a new idea..."}
        rows={4}
        style={{ width: "100%", padding: 12, fontSize: 14, borderRadius: 8, border: "2px solid #e53e3e" }}
      />
      <br />
      <button
        onClick={submit}
        disabled={loading}
        style={{
          marginTop: 10,
          background: "#e53e3e",
          color: "white",
          border: "none",
          padding: "12px 24px",
          fontSize: 16,
          borderRadius: 8,
          cursor: "pointer"
        }}
      >
        {loading ? "Analyzing..." : `Round ${round}: Attack My Idea`}
      </button>
    </div>
  );
}
