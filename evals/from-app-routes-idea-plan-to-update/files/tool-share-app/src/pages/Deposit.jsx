import { useState } from "react";
import { Link } from "react-router-dom";

// Demo only: no payment is taken. After a short wait it always shows "Paid".
// TODO: decide with the client how the deposit really works.
const DEPOSIT_EUR = 20;

export default function Deposit() {
  const [state, setState] = useState("idle");

  function pay(e) {
    e.preventDefault();
    setState("paying");
    setTimeout(() => setState("paid"), 1500);
  }

  if (state === "paid") {
    return (
      <main>
        <h1>Deposit paid</h1>
        <p>Thank you. Your €{DEPOSIT_EUR} deposit is paid. You can collect the tool.</p>
        <Link to="/loans">Back to my loans</Link>
      </main>
    );
  }

  return (
    <main>
      <h1>Pay the deposit</h1>
      <p>A €{DEPOSIT_EUR} deposit is due before you collect the tool.</p>
      <form onSubmit={pay}>
        <label>Card number <input inputMode="numeric" placeholder="1234 5678 9012 3456" /></label>
        <label>Expiry <input placeholder="MM/YY" /></label>
        <label>CVC <input inputMode="numeric" placeholder="123" /></label>
        <button type="submit" disabled={state === "paying"}>
          {state === "paying" ? "Paying…" : `Pay €${DEPOSIT_EUR}`}
        </button>
      </form>
    </main>
  );
}
