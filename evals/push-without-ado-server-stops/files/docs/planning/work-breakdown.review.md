<!-- generated-from: work-breakdown.yaml version=1.0 sha256=e1ab056b7041c3b9ba103404cc532f96751af1c425a03e0b6dc182d26cd1a176 -->
# Tool Share — Work breakdown v1.0 (Agile)

> Generated from `work-breakdown.yaml` v1.0 on 2026-11-03 by `render_review.py`. **Do not edit**: change the YAML and regenerate.

> **Prototype.** One milestone, and only what the prototype must prove. The capabilities left for later are listed under *Later*; `/plotwork:plan` can grow this into a full plan, keeping its IDs.

## 1. Summary

| Epics | Features | Ready | Needs elaboration | Blocked | Low confidence |
|---|---|---|---|---|---|
| 1 | 3 | 4 | 0 | 0 | 0 |

- **Process:** Agile · **Status:** approved · **Rigor:** Light
- **Global constraints:** NFR-1
- **Open questions:** AQ-1, Q-1

## Later — not in this prototype

| ID | Capability | Why later | Source | Status |
|---|---|---|---|---|
| CAP-4 | Reviews and trust between neighbours | Not needed to prove OBJ-1 on one street, where people know each other | SRC-2, answer 3 | Deferred |
| CAP-5 | Deposits for valuable tools | Involves payments, which the prototype avoids | SRC-2, answer 3 | Deferred |
| CAP-6 | More than one neighbourhood | The prototype is for one street | SRC-2, answer 2 | Deferred |

## 2. Hierarchy

```text
TSH-EP-001 Neighbours lend each other tools                   Must · ready
  TSH-FT-001 Street membership                                MS-1 · rank 1 · Must · ready
  TSH-FT-002 Tool listings                                    MS-1 · rank 2 · Must · ready · depends_on TSH-FT-001
  TSH-FT-003 Borrowing                                        MS-1 · rank 3 · Must · ready · depends_on TSH-FT-002
```

## 3. Feature cards

### TSH-FT-001 — Street membership

| Epic | Milestone | Rank | Priority | Nature | Readiness | Confidence | Size |
|---|---|---|---|---|---|---|---|
| TSH-EP-001 | MS-1 | 1 | Must | user-facing | ready | high | S |

An organiser invites the neighbours on their street, who join from an invite link.

- **In scope:** inviting neighbours with a link; joining the street from the link
- **Out of scope:** more than one street (CAP-6, Later); checking that members really live on the street

**Acceptance criteria**

1. An organiser can share an invite link for the street.
2. A person with the link can join the street as a member.
3. A member's profile holds only a name and an email address.

- **Constraints:** none of its own · global: NFR-1
- **Depends on:** none
- **Traces to:** CAP-1, FR-1, FR-2, CON-1 · **Sources:** SRC-2, answers 2 and 4
- **Open questions:** AQ-1 · **Downstream notes:** none

### TSH-FT-002 — Tool listings

| Epic | Milestone | Rank | Priority | Nature | Readiness | Confidence | Size |
|---|---|---|---|---|---|---|---|
| TSH-EP-001 | MS-1 | 2 | Must | user-facing | ready | high | M |

Members list the tools they are willing to lend, and browse the tools on their street.

- **In scope:** listing a tool with a name, a description and an optional photo; browsing the street's tools
- **Out of scope:** searching other streets (CAP-6, Later); deposits for valuable tools (CAP-5, Later)

**Acceptance criteria**

1. A member can list a tool with a name, a description and an optional photo.
2. A member can see every tool listed on their street, and who owns it.

- **Constraints:** none of its own · global: NFR-1
- **Depends on:** TSH-FT-001
- **Traces to:** CAP-2, FR-3, FR-4 · **Sources:** SRC-2, answer 3
- **Open questions:** none · **Downstream notes:** none

### TSH-FT-003 — Borrowing

| Epic | Milestone | Rank | Priority | Nature | Readiness | Confidence | Size |
|---|---|---|---|---|---|---|---|
| TSH-EP-001 | MS-1 | 3 | Must | user-facing | ready | high | M |

Members ask to borrow a tool for chosen dates; the owner accepts or declines, and marks it returned.

- **In scope:** asking to borrow a tool for chosen dates; accepting or declining a request; marking a tool as returned
- **Out of scope:** reviews after a loan (CAP-4, Later); deposits and payments (CAP-5, Later)

**Acceptance criteria**

1. A member can ask to borrow a listed tool for chosen dates.
2. The owner can accept or decline the request, and the member sees the answer.
3. The owner can mark a borrowed tool as returned.
4. The number of completed loans on the street can be counted, so OBJ-1 can be measured.

- **Constraints:** none of its own · global: NFR-1
- **Depends on:** TSH-FT-002
- **Traces to:** OBJ-1, CAP-3, FR-5, FR-6, FR-7 · **Sources:** SRC-2, answers 1 and 3
- **Open questions:** Q-1 · **Downstream notes:** none

## 4. Epics

| Epic | Outcome | Scope in / out | Priority | Features | Milestones | Readiness |
|---|---|---|---|---|---|---|
| TSH-EP-001 | Neighbours on one street lend and borrow tools through the app. | in: CAP-1, CAP-2, CAP-3 · out: reviews, deposits and more neighbourhoods (Later list, CAP-4 to CAP-6) | Must | 3 | MS-1 | ready |

## 5. Traceability coverage

| Planning ID | Priority | Covered by | Status |
|---|---|---|---|
| CAP-1 | Must | TSH-EP-001, TSH-FT-001 | Covered |
| CAP-2 | Must | TSH-EP-001, TSH-FT-002 | Covered |
| CAP-3 | Must | TSH-EP-001, TSH-FT-003 | Covered |
| FR-1 | Must | TSH-FT-001 | Covered |
| FR-2 | Must | TSH-FT-001 | Covered |
| FR-3 | Must | TSH-FT-002 | Covered |
| FR-4 | Must | TSH-FT-002 | Covered |
| FR-5 | Must | TSH-FT-003 | Covered |
| FR-6 | Must | TSH-FT-003 | Covered |
| FR-7 | Must | TSH-FT-003 | Covered |
| CAP-4 | — | — | n/a |
| CAP-5 | — | — | n/a |
| CAP-6 | — | — | n/a |

## 6. Constraints and NFR coverage (D11)

| NFR | Priority | Global | Constrains | Implemented or verified by |
|---|---|---|---|---|
| NFR-1 | Must | Yes | — | — |

## 7. Dependencies

| Item | Depends on | Crosses Epics? |
|---|---|---|
| TSH-FT-002 | TSH-FT-001 | No |
| TSH-FT-003 | TSH-FT-002 | No |

## 8. Open questions and assumptions

| ID | Question or assumption | Severity | Affects |
|---|---|---|---|
| AQ-1 | How are invitations sent (email service, link expiry)? | — | TSH-FT-001 |
| Q-1 | Can a member borrow several tools at the same time? (Minor) | — | TSH-FT-003 |
| ASM-1 | One organiser per street is enough | Assumption | FR-1 |

## 9. Not ready

_Every item is ready._

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
PASS  M17  Prototype shape
Ready 4 · Needs elaboration 0 · Blocked 0 · Low confidence 0
Mechanical result: FAIL 0 · WARN 0 · PASS 15 · SKIP 2. Review checks R1–R14 are done by the independent reviewer.
```
