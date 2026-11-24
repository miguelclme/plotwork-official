// Holds the deposit on the borrower's card through the payment provider, and releases it.
export const DEPOSIT_EUR = 20;
const API = "https://api.example-payments.test/v1";

export async function chargeDeposit(loanId, card) {
  const response = await fetch(`${API}/holds`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${import.meta.env.VITE_PAYMENTS_KEY}`,
    },
    body: JSON.stringify({ amount: DEPOSIT_EUR * 100, currency: "eur", reference: loanId, card }),
  });
  if (!response.ok) throw new Error("The card was declined. Try another card.");
  return response.json();
}

export async function releaseDeposit(holdId) {
  await fetch(`${API}/holds/${holdId}/release`, {
    method: "POST",
    headers: { Authorization: `Bearer ${import.meta.env.VITE_PAYMENTS_KEY}` },
  });
}
