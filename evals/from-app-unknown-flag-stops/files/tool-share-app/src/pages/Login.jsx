import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { signIn } from "../auth.js";

export default function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");

  function submit(e) {
    e.preventDefault();
    signIn(email);
    navigate("/tools");
  }

  return (
    <main>
      <h1>Sign in to ToolShare</h1>
      <form onSubmit={submit}>
        <label>Email <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} /></label>
        <label>Password <input type="password" /></label>
        <button type="submit">Sign in</button>
      </form>
    </main>
  );
}
