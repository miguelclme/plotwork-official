# Decision & RAID Log — ToolShare

| | |
|---|---|
| **Project key** | TSH |
| **Version** | v2 |
| **Date** | 2026-11-23 |

## Decisions *(required)*

| ID | Decision | Date | Rationale | Decided by (role) | Supersedes | Status |
|---|---|---|---|---|---|---|
| DEC-1 | ADO process: Agile | 2026-11-23 | Stated by the user (SRC-4) | Product Owner | — | Active |
| DEC-2 | Version 1 of the external prototype (`tool-share-app`, 2026-11-14) is the version the client approved. The needs read from its Working screens are Approved | 2026-11-23 | Stated by the user (SRC-4) | Product Owner | — | Active |
| DEC-3 | The team builds the product new, using the external prototype as the reference. Nothing is built yet and nothing is in Azure DevOps | 2026-11-23 | Stated by the user (SRC-4) | Product Owner | — | Active |
| DEC-4 | Sign-in is real: residents create an account with their email and a password | 2026-11-23 | The prototype's sign-in checks no password (SRC-1 `src/auth.js`); the user answered (SRC-4) | Product Owner | — | Active |
| DEC-5 | The €20 deposit is real: held on the borrower's card when they collect the tool, and released when the owner marks it returned | 2026-11-23 | The prototype's deposit charges nothing (SRC-1 `src/pages/Deposit.jsx`); the user answered (SRC-4) | Product Owner | — | Active |
| DEC-6 | The email to the owner on a new request is really sent | 2026-11-23 | The prototype sends no email (SRC-1 `src/services/notify.js`); the user answered (SRC-4) | Product Owner | — | Active |
| DEC-7 | Messages between neighbours come in a later release, not the first | 2026-11-23 | The prototype's Messages page is a placeholder (SRC-1 `src/pages/Messages.jsx`); the user answered (SRC-4) | Product Owner | — | Active |
| DEC-8 | `AGENTS.md` in the prototype is an old note for the platform's AI assistant and is ignored | 2026-11-23 | Stated by the user (SRC-4) | Product Owner | — | Active |

## Assumptions *(required)*

| ID | Assumption | Why it is needed | Affects | Accepted on | Status |
|---|---|---|---|---|---|
| ASM-1 | Anyone with an email address can create an account; the first release does not check that they live in the neighbourhood | Nothing says how residents are recognised (Q-1) | CAP-1, FR-1, TSH-FT-001 | 2026-11-23 | Open |
| ASM-2 | Real sign-in includes setting a new password after forgetting it, and signing out | The prototype shows neither: it has no password and no way to sign out | CAP-1, FR-4, TSH-FT-001 | 2026-11-23 | Open |
| ASM-3 | The borrower places the deposit hold from their loan when they collect the tool, as the prototype's "Pay deposit" step does, and the loan then shows the deposit as held | The prototype records no collection, and the user said the hold starts at collection | CAP-4, FR-13, TSH-FT-007 | 2026-11-23 | Open |
| ASM-4 | In the first release the deposit is only held and released. A tool returned damaged, or not returned, is settled outside the app | The user said only how the deposit is held and released (Q-2) | CAP-4, TSH-FT-007 | 2026-11-23 | Open |
| ASM-5 | Office hours are Monday to Friday, 09:00 to 18:00, local time | The user said office-hours availability is fine, without hours (Q-5) | NFR-3 | 2026-11-23 | Open |
| ASM-6 | A request blocks the dates at once; the owner does not accept or decline it, as in the approved prototype | The prototype has no step for the owner to answer (Q-7) | CAP-3, FR-9, TSH-FT-005 | 2026-11-23 | Open |

## Open questions *(required)*

| ID | Question | Severity | Affects | Needed by | Asked on | Answer | Status |
|---|---|---|---|---|---|---|---|
| Q-1 | Must ToolShare check that a new account belongs to a resident of the neighbourhood, and if so, how? Proposed: no check in the first release (ASM-1) | Material | CAP-1, TSH-FT-001 | MS-1 | 2026-11-23 | — | Open |
| Q-2 | What happens to the deposit when a tool comes back damaged, or not at all? Proposed: the first release only holds and releases it; such cases are settled outside the app (ASM-4) | Material | CAP-4, TSH-FT-007 | MS-1 | 2026-11-23 | — | Open |
| Q-3 | What must messages between neighbours do: who can write to whom, about what, and are they told of a new message? Proposed: a borrower and an owner can write to each other about a loan, and get an email for a new message | Material | CAP-5, TSH-FT-008 | MS-2 | 2026-11-23 | — | Open |
| Q-4 | Besides keeping data in the EU, what must the first release do for data protection: a privacy notice at sign-up, letting a resident delete their account and data? Proposed: a privacy notice at sign-up, and the association deletes an account on request | Material | CAP-1, NFR-4, TSH-FT-001 | MS-1 | 2026-11-23 | — | Open |
| Q-5 | Which hours are "office hours"? Proposed: Monday to Friday, 09:00 to 18:00, local time (ASM-5) | Minor | NFR-3 | MS-1 | 2026-11-23 | — | Open |
| Q-6 | Should a tool's pick-up place show on a map? The prototype holds a maps key that nothing uses. Proposed: no map in the first release | Minor | CAP-2, TSH-FT-002 | MS-1 | 2026-11-23 | — | Open |
| Q-7 | Should the owner accept or decline each request before the loan goes ahead? Proposed: no, a request blocks the dates at once, as in the approved prototype (ASM-6) | Minor | CAP-3, TSH-FT-005 | MS-1 | 2026-11-23 | — | Open |
| Q-8 | Should an owner be able to change or withdraw a tool they offered? The approved prototype can't. Proposed: yes, in the first release; if yes, it is added to the Offer a tool Feature | Minor | CAP-2, TSH-FT-003 | MS-1 | 2026-11-23 | — | Open |

## Risks *(conditional: material risks exist)*

| ID | Risk | Likelihood | Impact | Mitigation | Owner (role) | Status |
|---|---|---|---|---|---|---|
| RSK-1 | A maps API key sits in the prototype's files (`tool-share-app/.env`). If it is real, anyone with the files can use it | Medium | Medium | Replace the key before any real use, and never reuse it in the product | Product Owner | Open |
| RSK-2 | A card hold may lapse before a 14-day loan ends, leaving the owner without a deposit | Medium | Medium | Answer AQ-1 before the deposit is built | Tech Lead | Open |

## External dependencies *(conditional: something outside the project is needed)*

| ID | Dependency | On whom / what | Affects | Status |
|---|---|---|---|---|
| DEP-1 | An email service that sends ToolShare's emails to residents, keeping personal data in the EU (NFR-4) | Provider to be chosen | FR-10, TSH-FT-005 | Open |
| DEP-2 | A card payment service that can hold €20 on a card and release it, keeping personal data in the EU (NFR-4) | Provider to be chosen | FR-13, FR-14, TSH-FT-007 | Open |

## Architectural questions *(conditional: open "how" questions exist)*

| ID | Question | Why it matters | Affects (CAP / items) | Needed by | Status |
|---|---|---|---|---|---|
| AQ-1 | How does the €20 hold stay valid for a loan of up to 14 days? | Card holds can lapse sooner, depending on the payment service (RSK-2) | CAP-4, TSH-FT-007 | MS-1 | Open |
| AQ-2 | How are card details taken and held so that ToolShare meets the card payment security rules? | The product handles real cards (DEC-5) | CAP-4, TSH-FT-007 | MS-1 | Open |

## Changelog *(required)*

| Version | Date | Type | Summary | Ref |
|---|---|---|---|---|
| v1 | 2026-11-23 | New decision | First log | DEC-1 to DEC-8 |
| v2 | 2026-11-23 | New decision | Work breakdown v1.0 approved by the Product Owner at G3, with its assumptions ASM-1 to ASM-6 and its proposed priorities | work-breakdown.yaml v1.0 |
