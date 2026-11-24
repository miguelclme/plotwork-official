<!-- generated-from: work-breakdown.yaml version=1.0 sha256=05c67d564a7951cfbacc6291f1c303509ac2aa924f59f3221f22cf9c51545671 -->
# ToolShare — Work breakdown v1.0 (Agile)

> Generated from `work-breakdown.yaml` v1.0 on 2026-11-23 by `render_review.py`. **Do not edit**: change the YAML and regenerate.

## 1. Summary

| Epics | Features | Ready | Needs elaboration | Blocked | Low confidence |
|---|---|---|---|---|---|
| 2 | 8 | 9 | 1 | 0 | 1 |

- **Process:** Agile · **Status:** approved · **Rigor:** Rigorous
- **Global constraints:** NFR-1, NFR-2, NFR-3, NFR-4, NFR-5
- **Open questions:** AQ-1, AQ-2, Q-1, Q-2, Q-3, Q-4, Q-6, Q-7, Q-8
- **In Azure DevOps:** 10 of 10 items

## 2. Hierarchy

```text
TSH-EP-001 Neighbourhood tool library                         Must · ready · ADO #4101
  TSH-FT-001 Resident accounts and sign-in                    MS-1 · rank 1 · Must · ready · ADO #4102
  TSH-FT-002 Tool catalogue                                   MS-1 · rank 2 · Must · ready · depends_on TSH-FT-001 · ADO #4103
  TSH-FT-003 Offer a tool                                     MS-1 · rank 3 · Must · ready · depends_on TSH-FT-001 · ADO #4104
  TSH-FT-004 Accessibility conformance check                  MS-1 · rank 7 · Must · ready · depends_on TSH-FT-001, TSH-FT-002, TSH-FT-003, TSH-FT-005, TSH-FT-006, TSH-FT-007 · ADO #4105
TSH-EP-002 Borrowing and returning tools                      Must · ready · ADO #4106
  TSH-FT-005 Borrow requests                                  MS-1 · rank 4 · Must · ready · depends_on TSH-FT-002, DEP-1 · ADO #4107
  TSH-FT-006 Loans and returns                                MS-1 · rank 5 · Must · ready · depends_on TSH-FT-005 · ADO #4108
  TSH-FT-007 Tool deposit                                     MS-1 · rank 6 · Must · ready · depends_on TSH-FT-006, DEP-2 · ADO #4109
  TSH-FT-008 Messages between neighbours                      MS-2 · rank 1 · Should · needs-elaboration · depends_on TSH-FT-001 · ADO #4110
```

## 3. Feature cards

### TSH-FT-001 — Resident accounts and sign-in

**ADO #4102** · Epic ADO #4101

| Epic | Milestone | Rank | Priority | Nature | Readiness | Confidence | Size |
|---|---|---|---|---|---|---|---|
| TSH-EP-001 | MS-1 | 1 | Must | user-facing | ready | medium | M |

Residents create their own account with an email address and a password, and sign in with it to use ToolShare. People who are not signed in can't see the neighbourhood's tools or loans.

- **In scope:** creating an account with an email address and a password (FR-1); signing in with the email and password (FR-2); keeping people who are not signed in out of tools and loans (FR-3); setting a new password after forgetting it, and signing out (FR-4, ASM-2)
- **Out of scope:** checking that a person lives in the neighbourhood (ASM-1, Q-1); deleting an account and its data, until Q-4 is answered

**Acceptance criteria**

1. A person can create a resident account with their email address and a password.
2. A resident can sign in only with the right email address and password.
3. A person who is not signed in can't see tools or loans, and is asked to sign in.
4. A resident who forgot their password can set a new one, and a resident can sign out.

- **Constraints:** none of its own · global: NFR-1, NFR-2, NFR-3, NFR-4, NFR-5
- **Depends on:** none
- **Traces to:** OBJ-3, CAP-1, FR-1, FR-2, FR-3, FR-4, DEC-4 · **Sources:** SRC-4, SRC-1 src/pages/Login.jsx, SRC-1 src/auth.js, SRC-1 src/main.jsx
- **Open questions:** Q-1, Q-4 · **Downstream notes:** The prototype's sign-in screen asks for an email and a password, but checks no password and signs in as a sample resident (SRC-1 src/auth.js). The product's sign-in is real (DEC-4).; The prototype can sign out, but no screen offers it (SRC-1 src/auth.js).; The owner's email names the borrower (SRC-1 src/services/notify.js), and the sample residents have a name and a street (SRC-1 src/demoData.js): confirm with the association which details an account holds.

### TSH-FT-002 — Tool catalogue

**ADO #4103** · Epic ADO #4101

| Epic | Milestone | Rank | Priority | Nature | Readiness | Confidence | Size |
|---|---|---|---|---|---|---|---|
| TSH-EP-001 | MS-1 | 2 | Must | user-facing | ready | high | M |

Signed-in residents see the tools their neighbours offer, find one by name or category, and open it to see its details and where to pick it up.

- **In scope:** the list of offered tools, with name, category and condition (FR-5); searching by name and narrowing by category (FR-6); a tool's details, with category, condition and pick-up place (FR-7)
- **Out of scope:** a map of pick-up places (Q-6); offering a tool (TSH-FT-003); asking to borrow a tool (TSH-FT-005)

**Acceptance criteria**

1. A resident sees every tool their neighbours offer, with its name, category and condition.
2. A resident can find tools by part of their name, and narrow the list to one category.
3. A resident can open a tool and see its category, its condition and where to pick it up.

- **Constraints:** none of its own · global: NFR-1, NFR-2, NFR-3, NFR-4, NFR-5
- **Depends on:** TSH-FT-001
- **Traces to:** OBJ-1, CAP-2, FR-5, FR-6, FR-7 · **Sources:** SRC-1 src/pages/ToolList.jsx, SRC-1 src/pages/ToolDetail.jsx, SRC-1 src/store.js, SRC-2 What a resident can do
- **Open questions:** Q-6 · **Downstream notes:** The prototype's search matches part of a tool's name, ignoring upper and lower case, and says when no tool matches (SRC-1 src/store.js, src/pages/ToolList.jsx).; The prototype starts from four sample tools (SRC-1 src/demoData.js). There is no data to migrate (SRC-4).; The prototype keeps tools only in each browser (SRC-1 src/store.js): in the product, every resident sees the same tools.

### TSH-FT-003 — Offer a tool

**ADO #4104** · Epic ADO #4101

| Epic | Milestone | Rank | Priority | Nature | Readiness | Confidence | Size |
|---|---|---|---|---|---|---|---|
| TSH-EP-001 | MS-1 | 3 | Must | user-facing | ready | high | S |

A resident offers one of their own tools to the neighbourhood, so that neighbours can find it and ask to borrow it.

- **In scope:** offering a tool with a name, a category, a condition and a pick-up place (FR-8); the checks on an offered tool (BR-1, BR-2)
- **Out of scope:** changing or withdrawing an offered tool, until Q-8 is answered

**Acceptance criteria**

1. A resident can offer a tool with a name, a category, a condition and where to pick it up, and it then appears in the catalogue as theirs.
2. A tool can't be offered without a name, a category and a pick-up place.
3. A tool's category and condition come from fixed lists.

- **Constraints:** none of its own · global: NFR-1, NFR-2, NFR-3, NFR-4, NFR-5
- **Depends on:** TSH-FT-001
- **Traces to:** OBJ-1, CAP-2, FR-8, BR-1, BR-2 · **Sources:** SRC-1 src/pages/LendTool.jsx, SRC-1 src/store.js, SRC-1 src/demoData.js, SRC-2 What a resident can do
- **Open questions:** Q-8 · **Downstream notes:** The prototype's categories are Garden, Power tools, Hand tools, Ladders and Cleaning; its conditions are Like new, Good and Worn, with Good as the default (SRC-1 src/demoData.js, src/pages/LendTool.jsx).; In the prototype, the pick-up place is free text (SRC-1 src/pages/LendTool.jsx).

### TSH-FT-005 — Borrow requests

**ADO #4107** · Epic ADO #4106

| Epic | Milestone | Rank | Priority | Nature | Readiness | Confidence | Size |
|---|---|---|---|---|---|---|---|
| TSH-EP-002 | MS-1 | 4 | Must | user-facing | ready | high | M |

A resident asks to borrow a neighbour's tool for a start and an end date. The request is checked against the lending rules, blocks those dates, and the owner gets an email about it.

- **In scope:** asking to borrow a tool from a start date to an end date (FR-9); the lending rules on a request (BR-3, BR-4, BR-5, BR-6); the request blocking its dates at once (ASM-6); the email to the tool's owner for each new request (FR-10)
- **Out of scope:** the owner accepting or declining a request (ASM-6, Q-7); other emails, such as reminders (not in SRC-1 or SRC-4)

**Acceptance criteria**

1. A resident can ask to borrow a neighbour's tool from a start date to an end date, and the request is saved as requested.
2. A request for more than 14 days, counting the first and the last day, is refused.
3. A resident can't ask to borrow their own tool.
4. A request whose end date is before its start date is refused.
5. A request is refused when its dates overlap a loan of the same tool that is not returned yet.
6. For each new request, the tool's owner receives an email naming the borrower and the requested dates.

- **Constraints:** none of its own · global: NFR-1, NFR-2, NFR-3, NFR-4, NFR-5
- **Depends on:** TSH-FT-002, DEP-1
- **Traces to:** OBJ-1, OBJ-2, CAP-3, FR-9, FR-10, BR-3, BR-4, BR-5, BR-6, DEC-6 · **Sources:** SRC-1 src/pages/ToolDetail.jsx, SRC-1 src/store.js, SRC-1 src/store.test.js, SRC-1 src/services/notify.js, SRC-2 Notes from the workshops, SRC-4
- **Open questions:** Q-7 · **Downstream notes:** The prototype's rules and their messages are in SRC-1 src/store.js; its automated tests state four of them (SRC-1 src/store.test.js).; The prototype only writes the owner's email to the console (SRC-1 src/services/notify.js). The product really sends it (DEC-6), through DEP-1.

### TSH-FT-006 — Loans and returns

**ADO #4108** · Epic ADO #4106

| Epic | Milestone | Rank | Priority | Nature | Readiness | Confidence | Size |
|---|---|---|---|---|---|---|---|
| TSH-EP-002 | MS-1 | 5 | Must | user-facing | ready | high | M |

Borrowers and owners see the loans they take part in, and the owner marks a tool returned when it comes back.

- **In scope:** the resident's loans, as borrower and as owner, with the tool, the dates and the status (FR-11); the owner marking a loan returned (FR-12, BR-7)
- **Out of scope:** the deposit hold and its release (TSH-FT-007)

**Acceptance criteria**

1. A resident sees every loan they take part in, as borrower or as owner, with the tool, the dates and the status.
2. The tool's owner can mark a loan returned, and nobody else can.
3. Once a loan is marked returned, its dates are free for new requests.

- **Constraints:** none of its own · global: NFR-1, NFR-2, NFR-3, NFR-4, NFR-5
- **Depends on:** TSH-FT-005
- **Traces to:** OBJ-2, CAP-3, FR-11, FR-12, BR-6, BR-7 · **Sources:** SRC-1 src/pages/MyLoans.jsx, SRC-1 src/store.js, SRC-1 src/store.test.js, SRC-2 What a resident can do
- **Open questions:** none · **Downstream notes:** In the prototype a loan is requested, then returned (SRC-1 src/store.js).; The prototype lets the owner mark a loan returned while it is still only requested (SRC-1 src/pages/MyLoans.jsx).

### TSH-FT-007 — Tool deposit

**ADO #4109** · Epic ADO #4106

| Epic | Milestone | Rank | Priority | Nature | Readiness | Confidence | Size |
|---|---|---|---|---|---|---|---|
| TSH-EP-002 | MS-1 | 6 | Must | user-facing | ready | medium | L |

When a borrower collects a tool, €20 is held on their card as a deposit. The hold is released when the owner marks the tool returned.

- **In scope:** placing the €20 hold from the loan when the borrower collects the tool (FR-13, BR-8, ASM-3); the loan showing that the deposit is held (ASM-3); releasing the hold when the owner marks the tool returned (FR-14)
- **Out of scope:** taking the deposit for a damaged tool or one not returned (ASM-4, Q-2)

**Acceptance criteria**

1. When collecting a tool, the borrower can have €20 held on their card from their loan.
2. The loan shows that the deposit is held.
3. When the owner marks the tool returned, the hold is released and no money is taken from the borrower.

- **Constraints:** none of its own · global: NFR-1, NFR-2, NFR-3, NFR-4, NFR-5
- **Depends on:** TSH-FT-006, DEP-2
- **Traces to:** OBJ-2, CAP-4, FR-13, FR-14, BR-8, DEC-5 · **Sources:** SRC-4, SRC-1 src/pages/Deposit.jsx, SRC-1 src/pages/MyLoans.jsx
- **Open questions:** Q-2, AQ-1, AQ-2 · **Downstream notes:** The prototype's deposit screen asks for a card number, an expiry date and a security code, charges nothing, and always shows the deposit as paid after a short wait (SRC-1 src/pages/Deposit.jsx). The product holds the deposit instead of taking it (DEC-5).

### TSH-FT-004 — Accessibility conformance check

**ADO #4105** · Epic ADO #4101

| Epic | Milestone | Rank | Priority | Nature | Readiness | Confidence | Size |
|---|---|---|---|---|---|---|---|
| TSH-EP-001 | MS-1 | 7 | Must | verification | ready | high | M |

For the association and every resident, proof that every user-facing flow delivered by MS-1 meets WCAG 2.1 AA (NFR-5) on phones and computers (NFR-1), before the first release.

- **In scope:** checking every user-facing flow delivered by MS-1 against WCAG 2.1 AA, on a phone and on a computer; checking again the failures once they are fixed
- **Out of scope:** flows delivered after MS-1, which get their own check

**Acceptance criteria**

1. Every user-facing flow delivered by MS-1 has been checked against WCAG 2.1 AA, on a phone and on a computer.
2. Every failure found has been fixed and checked again before the first release.

- **Constraints:** none of its own · global: NFR-1, NFR-2, NFR-3, NFR-4, NFR-5
- **Depends on:** TSH-FT-001, TSH-FT-002, TSH-FT-003, TSH-FT-005, TSH-FT-006, TSH-FT-007
- **Traces to:** OBJ-3, NFR-5, NFR-1 · **Sources:** SRC-4
- **Open questions:** none · **Downstream notes:** none

### TSH-FT-008 — Messages between neighbours

**ADO #4110** · Epic ADO #4106

| Epic | Milestone | Rank | Priority | Nature | Readiness | Confidence | Size |
|---|---|---|---|---|---|---|---|
| TSH-EP-002 | MS-2 | 1 | Should | user-facing | needs-elaboration | low | — |

Residents send messages to each other in the app. What messages must do is not defined yet (Q-3).

- **In scope:** messages between neighbours, as the answer to Q-3 defines them
- **Out of scope:** the first release (DEC-7)

**Acceptance criteria**

_None yet._

- **Constraints:** none of its own · global: NFR-1, NFR-2, NFR-3, NFR-4, NFR-5
- **Depends on:** TSH-FT-001
- **Traces to:** OBJ-1, CAP-5, DEC-7 · **Sources:** SRC-1 src/pages/Messages.jsx, SRC-2 Notes from the workshops, SRC-4
- **Open questions:** Q-3 · **Downstream notes:** In the prototype, Messages is a page that says messages are coming soon (SRC-1 src/pages/Messages.jsx).

## 4. Epics

| Epic | Outcome | Scope in / out | Priority | Features | Milestones | Readiness |
|---|---|---|---|---|---|---|
| TSH-EP-001 | Residents of the neighbourhood have their own accounts, and can see and offer the tools their neighbours lend. | in: CAP-1, CAP-2 · out: other neighbourhoods (SRC-4), moving data from the prototype or any other system (none to move, SRC-4) | Must | 4 | MS-1 | ready |
| TSH-EP-002 | Residents borrow a neighbour's tool for up to two weeks with a €20 deposit held on their card, the owner is told by email and marks the tool returned, and later neighbours can message each other. | in: CAP-3, CAP-4, CAP-5 · out: messages in the first release (DEC-7) | Must | 4 | MS-1, MS-2 | ready |

## 5. Traceability coverage

| Planning ID | Priority | Covered by | Status |
|---|---|---|---|
| CAP-1 | Must | TSH-EP-001, TSH-FT-001 | Covered |
| CAP-2 | Must | TSH-EP-001, TSH-FT-002, TSH-FT-003 | Covered |
| CAP-3 | Must | TSH-EP-002, TSH-FT-005, TSH-FT-006 | Covered |
| CAP-4 | Must | TSH-EP-002, TSH-FT-007 | Covered |
| CAP-5 | Should | TSH-EP-002, TSH-FT-008 | Covered |
| FR-1 | Must | TSH-FT-001 | Covered |
| FR-2 | Must | TSH-FT-001 | Covered |
| FR-3 | Must | TSH-FT-001 | Covered |
| FR-4 | Must | TSH-FT-001 | Covered |
| FR-5 | Must | TSH-FT-002 | Covered |
| FR-6 | Must | TSH-FT-002 | Covered |
| FR-7 | Must | TSH-FT-002 | Covered |
| FR-8 | Must | TSH-FT-003 | Covered |
| FR-9 | Must | TSH-FT-005 | Covered |
| FR-10 | Must | TSH-FT-005 | Covered |
| FR-11 | Must | TSH-FT-006 | Covered |
| FR-12 | Must | TSH-FT-006 | Covered |
| FR-13 | Must | TSH-FT-007 | Covered |
| FR-14 | Must | TSH-FT-007 | Covered |

## 6. Constraints and NFR coverage (D11)

| NFR | Priority | Global | Constrains | Implemented or verified by |
|---|---|---|---|---|
| NFR-1 | Must | Yes | — | TSH-FT-004 |
| NFR-2 | Must | Yes | — | — |
| NFR-3 | Must | Yes | — | — |
| NFR-4 | Must | Yes | — | — |
| NFR-5 | Must | Yes | — | TSH-FT-004 |

## 7. Dependencies

| Item | Depends on | Crosses Epics? |
|---|---|---|
| TSH-FT-002 | TSH-FT-001 | No |
| TSH-FT-003 | TSH-FT-001 | No |
| TSH-FT-004 | TSH-FT-001 | No |
| TSH-FT-004 | TSH-FT-002 | No |
| TSH-FT-004 | TSH-FT-003 | No |
| TSH-FT-004 | TSH-FT-005 | Yes |
| TSH-FT-004 | TSH-FT-006 | Yes |
| TSH-FT-004 | TSH-FT-007 | Yes |
| TSH-FT-005 | TSH-FT-002 | Yes |
| TSH-FT-005 | DEP-1 | n/a |
| TSH-FT-006 | TSH-FT-005 | No |
| TSH-FT-007 | TSH-FT-006 | No |
| TSH-FT-007 | DEP-2 | n/a |
| TSH-FT-008 | TSH-FT-001 | Yes |

## 8. Open questions and assumptions

| ID | Question or assumption | Severity | Affects |
|---|---|---|---|
| AQ-1 | How does the €20 hold stay valid for a loan of up to 14 days? | — | TSH-FT-007 |
| AQ-2 | How are card details taken and held so that ToolShare meets the card payment security rules? | — | TSH-FT-007 |
| Q-1 | Must ToolShare check that a new account belongs to a resident of the neighbourhood, and if so, how? Proposed: no check in the first release (ASM-1) | Material | TSH-FT-001 |
| Q-2 | What happens to the deposit when a tool comes back damaged, or not at all? Proposed: the first release only holds and releases it; such cases are settled outside the app (ASM-4) | Material | TSH-FT-007 |
| Q-3 | What must messages between neighbours do: who can write to whom, about what, and are they told of a new message? Proposed: a borrower and an owner can write to each other about a loan, and get an email for a new message | Material | TSH-FT-008 |
| Q-4 | Besides keeping data in the EU, what must the first release do for data protection: a privacy notice at sign-up, letting a resident delete their account and data? Proposed: a privacy notice at sign-up, and the association deletes an account on request | Material | TSH-FT-001 |
| Q-6 | Should a tool's pick-up place show on a map? The prototype holds a maps key that nothing uses. Proposed: no map in the first release | Minor | TSH-FT-002 |
| Q-7 | Should the owner accept or decline each request before the loan goes ahead? Proposed: no, a request blocks the dates at once, as in the approved prototype (ASM-6) | Minor | TSH-FT-005 |
| Q-8 | Should an owner be able to change or withdraw a tool they offered? The approved prototype can't. Proposed: yes, in the first release; if yes, it is added to the Offer a tool Feature | Minor | TSH-FT-003 |
| ASM-1 | Anyone with an email address can create an account; the first release does not check that they live in the neighbourhood | Assumption | CAP-1, FR-1, TSH-FT-001 |
| ASM-2 | Real sign-in includes setting a new password after forgetting it, and signing out | Assumption | CAP-1, FR-4, TSH-FT-001 |
| ASM-3 | The borrower places the deposit hold from their loan when they collect the tool, as the prototype's "Pay deposit" step does, and the loan then shows the deposit as held | Assumption | CAP-4, FR-13, TSH-FT-007 |
| ASM-4 | In the first release the deposit is only held and released. A tool returned damaged, or not returned, is settled outside the app | Assumption | CAP-4, TSH-FT-007 |
| ASM-5 | Office hours are Monday to Friday, 09:00 to 18:00, local time | Assumption | NFR-3 |
| ASM-6 | A request blocks the dates at once; the owner does not accept or decline it, as in the approved prototype | Assumption | CAP-3, FR-9, TSH-FT-005 |

## 9. Not ready

| Item | Readiness | Confidence | Held by |
|---|---|---|---|
| TSH-FT-008 | needs-elaboration | low | Q-3 |

## 10. Validation report

```text
Validation — TSH work breakdown v1.0 (process: Agile) · checks run by render_review.py
PASS  M1   Schema
PASS  M2   Unique IDs
PASS  M3   ID prefix
PASS  M4   Parents
PASS  M5   Dependencies
PASS  M6   References resolve
PASS  M7   Must coverage
PASS  M8   Should and Could coverage
PASS  M9   Open questions are current
PASS  M10  Size signals
SKIP  M11  Milestone load
            - no capacity given (--max-features-per-milestone)
PASS  M12  ADO IDs
SKIP  M13  Review view current
            - checked when the review view is validated, not while it is being generated
PASS  M14  Copied NFR text
PASS  M15  Terminology
PASS  M16  Epics mirror milestones
Ready 9 · Needs elaboration 1 · Blocked 0 · Low confidence 1
Mechanical result: FAIL 0 · WARN 0 · PASS 14 · SKIP 2. Review checks R1–R14 are done by the independent reviewer.
```
