import { useState } from "react";
import { Link } from "react-router-dom";
import { myLoans, markReturned } from "../store.js";
import { currentUser } from "../auth.js";

const labels = { requested: "Requested", "deposit-paid": "Deposit paid", returned: "Returned" };

export default function MyLoans() {
  const user = currentUser();
  const [loans, setLoans] = useState(myLoans(user));

  async function returned(id) {
    await markReturned(user, id);
    setLoans(myLoans(user));
  }

  return (
    <main>
      <h1>My loans</h1>
      {loans.length === 0 && <p>You have no loans yet.</p>}
      <table>
        <thead>
          <tr><th>Tool</th><th>From</th><th>To</th><th>Status</th><th></th></tr>
        </thead>
        <tbody>
          {loans.map((l) => (
            <tr key={l.id}>
              <td>{l.tool?.name}</td>
              <td>{l.from}</td>
              <td>{l.to}</td>
              <td>{labels[l.status]}</td>
              <td>
                {l.borrowerId === user.id && l.status === "requested" && (
                  <Link to={`/loans/${l.id}/deposit`}>Pay deposit</Link>
                )}
                {l.borrowerId === user.id && l.status === "returned" && !l.review && (
                  <Link to={`/loans/${l.id}/review`}>Rate this loan</Link>
                )}
                {l.tool?.ownerId === user.id && l.status !== "returned" && (
                  <button onClick={() => returned(l.id)}>Mark returned</button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </main>
  );
}
