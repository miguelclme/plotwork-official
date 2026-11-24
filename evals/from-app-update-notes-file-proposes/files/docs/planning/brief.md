# Project Brief — ToolShare

| | |
|---|---|
| **Project key** | TSH |
| **Version** | v2 |
| **Date** | 2026-11-23 |
| **Status** | Approved |

## Summary *(required)*

ToolShare is an app for the residents of one neighbourhood, built with the Riverside Residents' Association. Residents create an account, offer their own tools, find their neighbours' tools, and borrow them for up to two weeks. The owner gets an email for each request, the borrower's card holds a €20 deposit while they have the tool, and the hold is released when the owner marks it returned. The team builds the product new, using the client-approved external prototype as the reference. Messages between neighbours come in a later release. Out: data migration, other neighbourhoods, and anything the prototype doesn't show and the user didn't ask for, such as maps.

## Purpose / problem statement *(required)*

Neighbours each buy their own tools. ToolShare lets them lend and borrow tools instead [Fact · SRC-2 "ToolShare"].

## Objectives *(required)*

| ID | Objective / desired outcome | Success criterion (qualitative is fine) | Label |
|---|---|---|---|
| OBJ-1 | Neighbours lend and borrow tools instead of each buying their own | Residents find, borrow and lend tools through the app | [Fact · SRC-2 "ToolShare"] |
| OBJ-2 | Tools keep moving and come back to their owners | Loans stay short, and a deposit is held until the tool is returned | [Fact · SRC-2 "Notes from the workshops"; Decision · DEC-5] |
| OBJ-3 | Every resident can use it, on a phone or a computer, with their own account | Residents sign in with their own account; the app meets WCAG 2.1 AA | [Fact · SRC-4] |

## Primary users *(required)*

| User | Main goal | Label |
|---|---|---|
| Resident (borrower) | Find a neighbour's tool and borrow it for a few days | [Fact · SRC-1 `src/pages/ToolDetail.jsx`; SRC-2] |
| Resident (tool owner) | Offer a tool, know who asks for it, and get it back | [Fact · SRC-1 `src/pages/LendTool.jsx`, `src/pages/MyLoans.jsx`; SRC-2] |

## In-scope capabilities *(required)*

- Resident accounts and sign-in [Decision · DEC-4]
- Tool catalogue: browse, search and offer tools [Fact · SRC-1]
- Borrowing and returning tools, with an email to the owner [Fact · SRC-1; Decision · DEC-6]
- Tool deposit held on the borrower's card [Decision · DEC-5]
- Messages between neighbours, in a later release [Decision · DEC-7]

## Out of scope *(required)*

- Moving data from the prototype or any other system: there is none to move [Fact · SRC-4]
- Maps of pick-up places, until Q-6 is answered [Open · Q-6]
- Other neighbourhoods: the app serves one neighbourhood [Fact · SRC-4]

## Success criteria *(required)*

- Residents lend and borrow tools through the app, and tools come back within the loan period [Recommendation]

## Known constraints *(required: "None known" is allowed)*

None known. The user imposed no technology.

## Other stakeholders *(conditional: anyone other than you is affected or decides)*

| Stakeholder | Interest or role | Label |
|---|---|---|
| Riverside Residents' Association | The client: approved the external prototype | [Fact · SRC-4] |
| Functional team | Built the external prototype with the association | [Fact · SRC-4; SRC-2] |

## Non-functional expectations *(conditional: quality attributes shape scope)*

- About 300 residents of one neighbourhood [Fact · SRC-4] → NFR-2
- Works on phones and computers [Fact · SRC-4] → NFR-1
- Available during office hours [Fact · SRC-4] → NFR-3
- Personal data stays in the EU [Fact · SRC-4] → NFR-4
- Meets WCAG 2.1 AA [Fact · SRC-4] → NFR-5

## Compliance / regulatory *(conditional: regulated data or domain)*

- Residents' personal data stays in the EU [Fact · SRC-4]. Other data-protection duties are open [Open · Q-4]
- Card holds must follow the card payment rules of the payment service used [Recommendation] → AQ-2

## External dependencies and integrations *(conditional: other systems are involved)*

- An email service, to send the owner an email on each request [Decision · DEC-6] → DEP-1
- A card payment service that can hold and release €20 on a card [Decision · DEC-5] → DEP-2

## Milestones / deadlines *(conditional: timing or staged releases matter; and required, as a table, when there is no roadmap)*

The milestones are in `roadmap.md`. There is no deadline yet [Fact · SRC-4].

## G1 review

| Gate | Proposed result | Your decision | Date |
|---|---|---|---|
| G1 | Pass with assumptions | Approved, together with the work breakdown at G3 | 2026-11-23 |

## Changelog

| Version | Date | Type | Summary | Ref |
|---|---|---|---|---|
| v1 | 2026-11-23 | New decision | First brief | SRC-1, SRC-4 |
| v2 | 2026-11-23 | Clarification | G1 approved with the work breakdown v1.0 at G3 | — |
