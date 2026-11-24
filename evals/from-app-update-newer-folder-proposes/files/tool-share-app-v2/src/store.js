// Tools, loans and reviews, kept in the browser's storage.
import { demoTools } from "./demoData.js";
import { notifyOwner } from "./services/notify.js";
import { releaseDeposit } from "./services/payments.js";

export const MAX_LOAN_DAYS = 14;
const KEY = "toolshare.data";

function load() {
  const saved = localStorage.getItem(KEY);
  const data = saved ? JSON.parse(saved) : { tools: demoTools, loans: [] };
  data.reviews ??= [];
  return data;
}

function save(data) {
  localStorage.setItem(KEY, JSON.stringify(data));
}

export function listTools({ search = "", category = "" } = {}) {
  const text = search.trim().toLowerCase();
  return load().tools.filter(
    (t) => (!text || t.name.toLowerCase().includes(text)) && (!category || t.category === category)
  );
}

export function getTool(id) {
  return load().tools.find((t) => t.id === id);
}

export function addTool(owner, { name, category, condition, pickup }) {
  if (!name?.trim()) throw new Error("Give the tool a name.");
  if (!category) throw new Error("Choose a category.");
  if (!pickup?.trim()) throw new Error("Say where to pick it up.");
  const data = load();
  const tool = { id: `t${Date.now()}`, ownerId: owner.id, name: name.trim(), category, condition, pickup: pickup.trim() };
  data.tools.push(tool);
  save(data);
  return tool;
}

export function loanDays(from, to) {
  return Math.round((new Date(to) - new Date(from)) / 86400000) + 1;
}

export function requestLoan(borrower, toolId, from, to) {
  const data = load();
  const tool = data.tools.find((t) => t.id === toolId);
  if (!tool) throw new Error("This tool no longer exists.");
  if (tool.ownerId === borrower.id) throw new Error("You can't borrow your own tool.");
  if (new Date(to) < new Date(from)) throw new Error("The end date is before the start date.");
  if (loanDays(from, to) > MAX_LOAN_DAYS) throw new Error(`A loan lasts ${MAX_LOAN_DAYS} days at most.`);
  const busy = data.loans.some(
    (l) => l.toolId === toolId && l.status !== "returned" && !(to < l.from || from > l.to)
  );
  if (busy) throw new Error("Someone has already asked for these dates.");
  const loan = { id: `l${Date.now()}`, toolId, borrowerId: borrower.id, from, to, status: "requested" };
  data.loans.push(loan);
  save(data);
  notifyOwner(tool, borrower, loan);
  return loan;
}

export function getLoan(id) {
  const data = load();
  const loan = data.loans.find((l) => l.id === id);
  return loan && { ...loan, tool: data.tools.find((t) => t.id === loan.toolId) };
}

export function myLoans(user) {
  const data = load();
  return data.loans
    .map((l) => ({
      ...l,
      tool: data.tools.find((t) => t.id === l.toolId),
      review: data.reviews.find((r) => r.loanId === l.id),
    }))
    .filter((l) => l.borrowerId === user.id || l.tool?.ownerId === user.id);
}

export function recordDeposit(loanId, holdId) {
  const data = load();
  const loan = data.loans.find((l) => l.id === loanId);
  loan.status = "deposit-paid";
  loan.depositHoldId = holdId;
  save(data);
}

export async function markReturned(user, loanId) {
  const data = load();
  const loan = data.loans.find((l) => l.id === loanId);
  const tool = data.tools.find((t) => t.id === loan?.toolId);
  if (!loan || tool.ownerId !== user.id) throw new Error("Only the tool's owner can mark it as returned.");
  if (loan.depositHoldId) await releaseDeposit(loan.depositHoldId);
  loan.status = "returned";
  save(data);
}

export function addReview(user, loanId, stars, comment) {
  const data = load();
  const loan = data.loans.find((l) => l.id === loanId);
  if (!loan || loan.borrowerId !== user.id) throw new Error("Only the borrower can rate this loan.");
  if (loan.status !== "returned") throw new Error("You can rate a loan once the tool is returned.");
  if (data.reviews.some((r) => r.loanId === loanId)) throw new Error("You have already rated this loan.");
  if (stars < 1 || stars > 5) throw new Error("Choose from 1 to 5 stars.");
  data.reviews.push({ loanId, toolId: loan.toolId, authorId: user.id, stars, comment: comment.trim().slice(0, 300) });
  save(data);
}
