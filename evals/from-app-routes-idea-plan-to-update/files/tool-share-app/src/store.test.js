import { describe, it, expect, beforeEach } from "vitest";
import { requestLoan, markReturned, MAX_LOAN_DAYS } from "./store.js";

const ana = { id: "r1", name: "Ana Costa" };
const ben = { id: "r2", name: "Ben Hall" };

describe("loans", () => {
  beforeEach(() => localStorage.clear());

  it("lasts two weeks at most", () => {
    expect(MAX_LOAN_DAYS).toBe(14);
    expect(() => requestLoan(ana, "t2", "2026-12-01", "2026-12-15")).toThrow();
  });

  it("can't be asked for your own tool", () => {
    expect(() => requestLoan(ana, "t1", "2026-12-01", "2026-12-03")).toThrow();
  });

  it("can't overlap another loan of the same tool", () => {
    requestLoan(ana, "t2", "2026-12-01", "2026-12-05");
    expect(() => requestLoan(ana, "t2", "2026-12-04", "2026-12-06")).toThrow();
  });

  it("is marked returned by the owner only", () => {
    const loan = requestLoan(ana, "t2", "2026-12-01", "2026-12-03");
    expect(() => markReturned(ana, loan.id)).toThrow();
    markReturned(ben, loan.id);
  });
});
