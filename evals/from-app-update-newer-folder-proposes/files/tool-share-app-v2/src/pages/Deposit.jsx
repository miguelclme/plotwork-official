import { useState } from "react";
import { Link, useParams } from "react-router-dom";
import { chargeDeposit, DEPOSIT_EUR } from "../services/payments.js";
import { recordDeposit } from "../store.js";

export default function Deposit() {
  const { id } = useParams();
  const [state, setState] = useState("idle");
  const [error, setError] = useState("");
  const [card, setCard] = useState({ number: "", expiry: "", cvc: "" });
  const set = (key) => (e) => setCard({ ...card, [key]: e.target.value });

  async function pay(e) {
    e.preventDefault();
    setState("paying");
    setError("");
    try {
      const charge = await chargeDeposit(id, card);
      recordDeposit(id, charge.id);
      setState("paid");
    } catch (err) {
      setError(err.message);
      setState("idle");
    }
  }

  if (state === "paid") {
    return (
      <main>
        <h1>Deposit paid</h1>
        <p>Your €{DEPOSIT_EUR} deposit is held on your card. It is released when the owner marks the tool as returned.</p>
        <Link to="/loans">Back to my loans</Link>
      </main>
    );
  }

  return (
    <main>
      <h1>Pay the deposit</h1>
      <p>A €{DEPOSIT_EUR} deposit is held on your card before you collect the tool.</p>
      <form onSubmit={pay}>
        <label>Card number <input inputMode="numeric" required value={card.number} onChange={set("number")} /></label>
        <label>Expiry <input placeholder="MM/YY" required value={card.expiry} onChange={set("expiry")} /></label>
        <label>CVC <input inputMode="numeric" required value={card.cvc} onChange={set("cvc")} /></label>
        {error && <p className="error">{error}</p>}
        <button type="submit" disabled={state === "paying"}>
          {state === "paying" ? "Paying…" : `Pay €${DEPOSIT_EUR}`}
        </button>
      </form>
    </main>
  );
}
