import { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getTool, requestLoan, MAX_LOAN_DAYS } from "../store.js";
import { currentUser } from "../auth.js";

export default function ToolDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const tool = getTool(id);
  const [from, setFrom] = useState("");
  const [to, setTo] = useState("");
  const [error, setError] = useState("");

  if (!tool) return <main><p>This tool no longer exists.</p></main>;

  function submit(e) {
    e.preventDefault();
    try {
      requestLoan(currentUser(), tool.id, from, to);
      navigate("/loans");
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <main>
      <h1>{tool.name}</h1>
      <p>{tool.category} · Condition: {tool.condition}</p>
      <p>Pick up at: {tool.pickup}</p>
      <form onSubmit={submit}>
        <h2>Borrow it</h2>
        <label>From <input type="date" required value={from} onChange={(e) => setFrom(e.target.value)} /></label>
        <label>To <input type="date" required value={to} onChange={(e) => setTo(e.target.value)} /></label>
        <p className="hint">Loans last {MAX_LOAN_DAYS} days at most.</p>
        {error && <p className="error">{error}</p>}
        <button type="submit">Ask to borrow</button>
      </form>
    </main>
  );
}
