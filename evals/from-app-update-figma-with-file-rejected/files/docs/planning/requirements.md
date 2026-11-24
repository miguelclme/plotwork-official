# Requirements & Scope Register — ToolShare

| | |
|---|---|
| **Project key** | TSH |
| **Version** | v2 |
| **Date** | 2026-11-23 |
| **Status** | Approved |

Needs read from the Working screens of the client-approved version of the external prototype are Approved (DEC-2). Needs from the user's answers are Approved through their DEC. Needs that rest on an assumption stay Proposed, covered by their ASM.

## Capability map *(required)*

| ID | Capability | Purpose | Traces to | In scope | Out of scope | Priority | Milestone | Status |
|---|---|---|---|---|---|---|---|---|
| CAP-1 | Resident accounts | Each resident uses ToolShare with their own account | OBJ-3 | Creating an account with an email and a password; signing in; forgotten password and signing out (ASM-2) | Checking that a person lives in the neighbourhood (ASM-1, Q-1) | Must (proposed) | MS-1 | Approved |
| CAP-2 | Tool catalogue | Residents see what their neighbours can lend, and offer their own tools | OBJ-1 | Browsing, searching and filtering tools; a tool's details; offering a tool | Maps of pick-up places (Q-6) | Must (proposed) | MS-1 | Approved |
| CAP-3 | Borrowing and returns | Residents borrow a tool for a short time and the owner gets it back | OBJ-1, OBJ-2 | Asking to borrow for dates; the owner's email; the list of loans; marking a tool returned | The owner accepting or declining a request (ASM-6, Q-7) | Must (proposed) | MS-1 | Approved |
| CAP-4 | Tool deposit | A deposit protects the owner while the tool is away | OBJ-2 | Holding €20 on the borrower's card at collection; releasing it on return | Charging the deposit, for damage or a tool not returned (ASM-4, Q-2) | Must (proposed) | MS-1 | Approved |
| CAP-5 | Messages between neighbours | Neighbours talk to each other in the app | OBJ-1 | To be defined (Q-3) | — | Should (proposed) | MS-2 | Approved |

## Functional requirements *(required)*

| ID | Statement (what, not how) | CAP | Priority | Acceptance measure | Source | Traces to | Status |
|---|---|---|---|---|---|---|---|
| FR-1 | A person can create a resident account with their email address and a password | CAP-1 | Must (proposed) | A new person creates an account and then signs in with it | SRC-4 | OBJ-3, DEC-4 | Approved |
| FR-2 | A resident signs in with their email and password; a wrong password does not sign them in | CAP-1 | Must (proposed) | Only the right email and password open the account | SRC-4; SRC-1 `src/pages/Login.jsx` | OBJ-3, DEC-4 | Approved |
| FR-3 | Only signed-in residents can see and use tools, loans and messages | CAP-1 | Must (proposed) | A person who is not signed in is sent to sign in | SRC-1 `src/main.jsx` | OBJ-3 | Approved |
| FR-4 | A resident who forgot their password can set a new one, and a resident can sign out | CAP-1 | Must (proposed) | A resident regains access without help; after signing out, the account is closed on that device | ASM-2 | OBJ-3 | Proposed |
| FR-5 | A resident sees the tools their neighbours offer, with name, category and condition | CAP-2 | Must (proposed) | Every offered tool appears in the list | SRC-1 `src/pages/ToolList.jsx`; SRC-2 | OBJ-1 | Approved |
| FR-6 | A resident can search tools by name and narrow them by category | CAP-2 | Must (proposed) | The list shows only the tools that match | SRC-1 `src/pages/ToolList.jsx`, `src/store.js`; SRC-2 | OBJ-1 | Approved |
| FR-7 | A resident can open a tool and see its category, condition and where to pick it up | CAP-2 | Must (proposed) | The tool's details show these | SRC-1 `src/pages/ToolDetail.jsx` | OBJ-1 | Approved |
| FR-8 | A resident can offer one of their own tools, with a name, a category, a condition and where to pick it up | CAP-2 | Must (proposed) | The new tool appears in the catalogue, owned by that resident | SRC-1 `src/pages/LendTool.jsx`, `src/store.js`; SRC-2 | OBJ-1 | Approved |
| FR-9 | A resident can ask to borrow a neighbour's tool from a start date to an end date | CAP-3 | Must (proposed) | A valid request is saved and blocks those dates | SRC-1 `src/pages/ToolDetail.jsx`, `src/store.js`; SRC-2 | OBJ-1, OBJ-2 | Approved |
| FR-10 | The tool's owner gets an email when someone asks to borrow it, saying who and for which dates | CAP-3 | Must (proposed) | The owner receives the email for each new request | SRC-4; SRC-1 `src/services/notify.js`; SRC-2 | OBJ-1, DEC-6 | Approved |
| FR-11 | A resident sees their loans, as borrower and as owner, with the tool, the dates and the status | CAP-3 | Must (proposed) | Every loan the resident takes part in is listed | SRC-1 `src/pages/MyLoans.jsx`, `src/store.js`; SRC-2 | OBJ-2 | Approved |
| FR-12 | The tool's owner can mark a loan as returned | CAP-3 | Must (proposed) | The loan shows as returned and its dates are free again | SRC-1 `src/pages/MyLoans.jsx`, `src/store.js`; SRC-2 | OBJ-2 | Approved |
| FR-13 | When the borrower collects the tool, €20 is held on their card as a deposit | CAP-4 | Must (proposed) | The hold is in place before the tool is handed over, and the loan shows it | SRC-4; SRC-1 `src/pages/Deposit.jsx`; ASM-3 | OBJ-2, DEC-5 | Approved |
| FR-14 | The deposit hold is released when the owner marks the tool returned | CAP-4 | Must (proposed) | No money is taken from the borrower once the tool is marked returned | SRC-4 | OBJ-2, DEC-5 | Approved |

## Non-functional requirements *(conditional: quality attributes are relevant)*

| ID | Statement | Quality attribute | Applies to | D11 pattern | Priority | Target / acceptance measure | Source | Traces to | Status |
|---|---|---|---|---|---|---|---|---|---|
| NFR-1 | Residents can use every part of the app on a phone and on a computer | Compatibility | Global | Constraint | Must (proposed) | Every flow works on current phone and computer browsers | SRC-4 | OBJ-3 | Approved |
| NFR-2 | The app serves the residents of one neighbourhood, about 300 people | Performance efficiency | Global | Constraint | Must (proposed) | About 300 accounts with normal use and no slowdown | SRC-4 | OBJ-1 | Approved |
| NFR-3 | The app is available during office hours; it may be down outside them | Reliability | Global | Constraint | Must (proposed) | Available during office hours (ASM-5) | SRC-4 | OBJ-1 | Approved |
| NFR-4 | Residents' personal data is stored and processed only in the EU | Security | Global | Constraint | Must (proposed) | No personal data is kept or processed outside the EU, by ToolShare or by the services it uses | SRC-4 | OBJ-3 | Approved |
| NFR-5 | The app meets WCAG 2.1 level AA | Usability | Global | Constraint · Verification | Must (proposed) | Every user-facing flow of a release passes a WCAG 2.1 AA check | SRC-4 | OBJ-3 | Approved |

## Business rules *(conditional: domain rules exist)*

| ID | Rule | CAP | Source | Status |
|---|---|---|---|---|
| BR-1 | A tool needs a name, a category and a pick-up place | CAP-2 | SRC-1 `src/store.js` | Approved |
| BR-2 | A tool's category comes from a fixed list, and its condition is Like new, Good or Worn | CAP-2 | SRC-1 `src/demoData.js`, `src/pages/LendTool.jsx` | Approved |
| BR-3 | A loan lasts 14 days at most, counting the first and the last day | CAP-3 | SRC-1 `src/store.js`, `src/store.test.js`; SRC-2 "Notes from the workshops" | Approved |
| BR-4 | Nobody may borrow their own tool | CAP-3 | SRC-1 `src/store.js`, `src/store.test.js`; SRC-2 "Notes from the workshops" | Approved |
| BR-5 | A loan's end date can't be before its start date | CAP-3 | SRC-1 `src/store.js` | Approved |
| BR-6 | A tool can't be asked for dates that overlap a loan of it that is not returned yet | CAP-3 | SRC-1 `src/store.js`, `src/store.test.js` | Approved |
| BR-7 | Only the tool's owner can mark a loan of it returned | CAP-3 | SRC-1 `src/store.js`, `src/store.test.js` | Approved |
| BR-8 | The deposit is €20 per loan | CAP-4 | SRC-4; SRC-1 `src/pages/Deposit.jsx` | Approved |

## Constraints *(required: "None known" is allowed)*

None known. The user imposed no technology. The external prototype is the reference for what the product does, not for how it is built (DEC-3).

## Glossary *(conditional: domain terms are ambiguous)*

| Term | Meaning |
|---|---|
| Resident | A person with a ToolShare account |
| Owner | The resident who offered a tool |
| Borrower | The resident who asked to borrow a tool |
| Loan | One borrowing of one tool, from a start date to an end date |
| Hold | €20 reserved on the borrower's card. It is not taken, and it is released when the tool is returned |

## G2 review

| Gate | Proposed result | Your decision | Date |
|---|---|---|---|
| G2 | Ready with documented assumptions | Approved, together with the work breakdown at G3 | 2026-11-23 |

## Changelog

| Version | Date | Type | Summary | Ref |
|---|---|---|---|---|
| v1 | 2026-11-23 | New decision | First register | SRC-1, SRC-4 |
| v2 | 2026-11-23 | Clarification | G2 approved with the work breakdown v1.0 at G3 | — |
