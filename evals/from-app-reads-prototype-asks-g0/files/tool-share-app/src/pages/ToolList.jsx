import { useState } from "react";
import { Link } from "react-router-dom";
import { listTools } from "../store.js";
import { categories } from "../demoData.js";
import "./ToolList.css";

export default function ToolList() {
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("");
  const tools = listTools({ search, category });

  return (
    <main>
      <h1>Tools near you</h1>
      <div className="filters">
        <input placeholder="Search tools" value={search} onChange={(e) => setSearch(e.target.value)} />
        <select value={category} onChange={(e) => setCategory(e.target.value)}>
          <option value="">All categories</option>
          {categories.map((c) => <option key={c}>{c}</option>)}
        </select>
      </div>
      {tools.length === 0 && <p>No tool matches your search.</p>}
      <ul className="tool-grid">
        {tools.map((t) => (
          <li key={t.id} className="tool-card">
            <Link to={`/tools/${t.id}`}>
              <strong>{t.name}</strong>
              <span>{t.category} · {t.condition}</span>
            </Link>
          </li>
        ))}
      </ul>
    </main>
  );
}
