import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { addTool } from "../store.js";
import { currentUser } from "../auth.js";
import { categories } from "../demoData.js";

const conditions = ["Like new", "Good", "Worn"];

export default function LendTool() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ name: "", category: "", condition: "Good", pickup: "" });
  const [error, setError] = useState("");
  const set = (key) => (e) => setForm({ ...form, [key]: e.target.value });

  function submit(e) {
    e.preventDefault();
    try {
      const tool = addTool(currentUser(), form);
      navigate(`/tools/${tool.id}`);
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <main>
      <h1>Lend a tool</h1>
      <form onSubmit={submit}>
        <label>Name <input value={form.name} onChange={set("name")} /></label>
        <label>Category
          <select value={form.category} onChange={set("category")}>
            <option value="">Choose…</option>
            {categories.map((c) => <option key={c}>{c}</option>)}
          </select>
        </label>
        <label>Condition
          <select value={form.condition} onChange={set("condition")}>
            {conditions.map((c) => <option key={c}>{c}</option>)}
          </select>
        </label>
        <label>Where to pick it up <input value={form.pickup} onChange={set("pickup")} /></label>
        {error && <p className="error">{error}</p>}
        <button type="submit">Offer this tool</button>
      </form>
    </main>
  );
}
