# Assessment Record — ToolShare

| | |
|---|---|
| **Project key** | TSH |
| **Version** | v2 |
| **Date** | 2026-11-23 |
| **Status** | Reviewed at G0 |

## 1. Project state and artifacts *(required)*

**Scenario:** D — External prototype

The project is new: nothing is being built and there is nothing in Azure DevOps [Fact · SRC-4]. The team will build the product new, using the external prototype as the reference [Decision · DEC-3]. The external prototype is not the product (D20).

| ID | Source (title or file) | Date or version | Stated status | Covers (§6.3 dimensions) | Trust notes |
|---|---|---|---|---|---|
| SRC-1 | External prototype `tool-share-app` (screens, rules, tests, sample data) | Version 1, 2026-11-14 (its own files say 0.1.0, in `package.json`) | Approved by the client [Decision · DEC-2] | People who use it, scope, functional needs, rules | Read without running it. Sign-in, deposit and the owner email are Mocked; Messages is a Placeholder. Data is kept only in each browser. See `app-inventory.md` |
| SRC-2 | `tool-share-app/README.md` | Undated, part of version 1 | Unknown | Purpose, functional needs, rules, workshop notes | Written by the functional team after two workshops with the association |
| SRC-3 | `tool-share-app/AGENTS.md` | Undated | Ignored, on the user's instruction [Decision · DEC-8] | None | Holds instructions to AI planners. Not followed |
| SRC-4 | The user's request of 2026-11-23 | 2026-11-23 | Product Owner's answers | Process, version, build approach, real services, release scope, users, NFRs, migration, deadlines | Answers every G0 question in advance |

## 2. Reusable information and approved decisions *(required)*

- ToolShare lets neighbours lend and borrow tools instead of each buying their own [Fact · SRC-2 "ToolShare"].
- The client is the Riverside Residents' Association [Fact · SRC-4].
- Version 1 of the external prototype, from 14 November 2026, is the version the client approved [Decision · DEC-2].
- The team builds the product new, with the external prototype as the reference [Decision · DEC-3].
- Residents browse, search and filter tools, offer their own tools, ask to borrow for dates, see their loans, and owners mark tools returned [Fact · SRC-1 Working screens, see `app-inventory.md`].
- Loans last 14 days at most, nobody borrows their own tool, and requests can't overlap [Fact · SRC-1 `src/store.js`, `src/store.test.js`; SRC-2 "Notes from the workshops"].
- Sign-in must be real: residents create an account with their email and a password [Decision · DEC-4].
- The €20 deposit must be real: held on the borrower's card at collection, released when the owner marks the tool returned [Decision · DEC-5].
- The email to the owner on a new request must really be sent [Decision · DEC-6].
- Messages between neighbours come later, not in the first release [Decision · DEC-7].
- About 300 residents of one neighbourhood, on phones and computers; office-hours availability is enough; personal data stays in the EU; the app meets WCAG 2.1 AA [Fact · SRC-4].
- No data to migrate, and no deadline yet [Fact · SRC-4].
- ADO process: Agile [Decision · DEC-1].

## 3. Missing or ambiguous information *(required)*

| Gap | Area (CAP or dimension) | Severity | Proposed handling |
|---|---|---|---|
| Whether a new account must belong to a resident of the neighbourhood | CAP-1 | Material | ASM-1, Q-1 |
| Account basics the prototype doesn't show: a forgotten password, signing out | CAP-1 | Material | ASM-2 |
| Data-protection duties beyond keeping data in the EU (privacy notice, deleting an account) | CAP-1, NFR-4 | Material | Q-4 |
| What happens to the deposit when a tool comes back damaged, or not at all | CAP-4 | Material | ASM-4, Q-2 |
| When and how the deposit hold is placed at collection; the prototype records no collection | CAP-4 | Material | ASM-3 |
| How a card hold stays valid for a loan of up to 14 days | CAP-4 | Material | AQ-1, RSK-2 |
| Whether the owner accepts or declines a request | CAP-3 | Minor | ASM-6, Q-7 |
| What messages between neighbours must do | CAP-5 | Material — MS-2 | Q-3 |
| What "office hours" means | NFR-3 | Minor | ASM-5, Q-5 |
| Whether a map of pick-up places is intended (an unused maps key exists) | CAP-2 | Minor | Q-6 |
| Whether an owner can change or withdraw a tool they offered; the prototype can't | CAP-2 | Minor | Q-8 |

## 4. Contradictions, risks and blockers *(required)*

| Conflict or risk | Sources | Proposed resolution | Logged as (defined in `decisions-raid.md`) |
|---|---|---|---|
| The prototype says the deposit is "paid" before collection; the user says it is held at collection and released on return | SRC-1 `src/pages/Deposit.jsx`, SRC-2 "What a resident can do" vs SRC-4 | The user's answer wins: hold and release, no payment [Decision · DEC-5] | DEC-5 |
| `AGENTS.md` says the client approved everything, every Feature is Must, and no review or questions are needed | SRC-3 vs SRC-2 "Notes from the workshops" (deposit and messages are demo only) | Not followed; the user said to ignore the file [Decision · DEC-8] | DEC-8 |
| An API key sits in the prototype's files | SRC-1 `.env` | Treat it as exposed: replace it before any real use, and never reuse it [Recommendation] | RSK-1 |
| A card hold may lapse before a 14-day loan ends | SRC-4, SRC-1 `src/store.js` | Architects choose how the hold stays valid [Recommendation] | RSK-2, AQ-1 |

## 5. ADO process *(required)*

Agile — DEC-1

## 6. Recommended route *(required)*

- **Route:** Stage 0 → Stage 1 → Stage 2 → Stage 3, because the code shows what the product does, but the Brief, the Register and the Roadmap must be written from it and from the user's answers.
- **Skipped stages:** none.
- **Rigor profile:** Rigorous, because the product keeps residents' personal data and holds money on their cards, and must meet EU data residency and WCAG 2.1 AA (§12).

## Maturity rubric *(optional for Light)*

| Dimension | Rating | Notes |
|---|---|---|
| Purpose & objectives | Sufficient | SRC-2, SRC-4 |
| People who use it & stakeholders | Sufficient | Residents of one neighbourhood; the association |
| Scope | Decomposition-ready | Working screens, plus the user's answers on every Mocked and Placeholder screen |
| Functional needs | Decomposition-ready | Except messages (Q-3) |
| Non-functional needs | Sufficient | SRC-4 |
| Constraints & dependencies | Sufficient | Email and card services needed |
| Risks & assumptions | Partial | Deposit edge cases (Q-2, AQ-1) |
| Priorities & milestones | Partial | Two releases, no dates |

## G0 review

| Gate | Proposed result | Your decision | Date |
|---|---|---|---|
| G0 | Pass with assumptions | Approved in advance by the user ("go straight to the breakdown"). The external prototype was read by Claude, without the app-reader agent | 2026-11-23 |

## Changelog

| Version | Date | Type | Summary | Ref |
|---|---|---|---|---|
| v1 | 2026-11-23 | New decision | First assessment | SRC-1, SRC-4 |
| v2 | 2026-11-23 | Clarification | Wording only: dimension names | — |
