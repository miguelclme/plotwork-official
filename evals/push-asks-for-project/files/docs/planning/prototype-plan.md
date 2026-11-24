# Prototype Plan — Tool Share

| | |
|---|---|
| **Project key** | TSH |
| **Version** | v2 |
| **Date** | 2026-11-03 |
| **Kind** | Prototype (one milestone, MS-1) |
| **ADO process** | Agile (DEC-1) |

## 1. Assessment

1. **State and artifacts:** Scenario A. The only source is SRC-1, the initial message: "I want a web app where neighbours lend each other tools. Nothing is built yet. Before we plan the whole thing, I want a prototype to see if neighbours actually lend." SRC-2 is the user's answers at G0.
2. **Reusable information and decisions:** the purpose, lending tools between neighbours [Fact · SRC-1]; a new project, nothing built [Fact · SRC-1]; a prototype first [Fact · SRC-1].
3. **Missing or ambiguous:**
   - What the prototype must prove, and who tries it (Blocking). Asked and answered (DEC-3).
   - Which capabilities are in, and which are later (Blocking). Proposed and accepted (DEC-2).
   - Data limits (Material). Asked and answered (CON-1).
4. **Contradictions, risks, blockers:** none. How invitations are sent is handed downstream as AQ-1. Whether a member can borrow several tools at once is Q-1, which is not blocking.
5. **ADO process:** Agile (DEC-1).
6. **Route:** Stage 0 → 3, prototype. Rigor: Light, because the prototype stores only names and email addresses, for one street.

G0: Pass, decided by the user on 2026-11-03.

## 2. What the prototype must prove

**Summary:** A prototype web app for one street, where neighbours list the tools they are willing to lend, and borrow each other's. It must prove that neighbours actually lend through it. Reviews, deposits and more neighbourhoods are later.

| ID | What it must prove | How you'll know it worked |
|---|---|---|
| OBJ-1 | Neighbours lend each other tools through the app | At least 5 loans are completed in the first 4 weeks [Decision · DEC-3] |

- **Who tries it:** about 20 households on the user's street [Decision · DEC-3].
- **Out of the prototype:** everything on the Later list [Decision · DEC-2].
- **Data and compliance limits:** names and email addresses only (CON-1).

## 3. In the prototype

| ID | Capability | Priority | Milestone |
|---|---|---|---|
| CAP-1 | Neighbourhood membership | Must | MS-1 |
| CAP-2 | Tool listings | Must | MS-1 |
| CAP-3 | Borrowing | Must | MS-1 |

| ID | Need (FR) | Capability | Priority |
|---|---|---|---|
| FR-1 | An organiser can invite neighbours with a link | CAP-1 | Must |
| FR-2 | A neighbour can join the street from the invite link | CAP-1 | Must |
| FR-3 | Members can list a tool with a name, a description and an optional photo | CAP-2 | Must |
| FR-4 | Members can browse the tools listed on their street | CAP-2 | Must |
| FR-5 | Members can ask to borrow a tool for chosen dates | CAP-3 | Must |
| FR-6 | Owners can accept or decline a request | CAP-3 | Must |
| FR-7 | Owners can mark a borrowed tool as returned | CAP-3 | Must |

**Non-functional requirements**

| ID | Statement | Applies to | D11 pattern | Priority | Target |
|---|---|---|---|---|---|
| NFR-1 | The app is usable in a phone browser | Global | Constraint | Must | Core screens usable at 360 px width |

**Constraints**

| ID | Statement | Source |
|---|---|---|
| CON-1 | Store only members' names and email addresses | SRC-2, answer 4 |

**Milestone**

| ID | Name | Outcome | Scope |
|---|---|---|---|
| MS-1 | Prototype | The street has completed at least 5 loans through the app | CAP-1, CAP-2, CAP-3 |

## 4. Later

| ID | Capability | Why later | Source | Status |
|---|---|---|---|---|
| CAP-4 | Reviews and trust between neighbours | Not needed to prove OBJ-1 on one street, where people know each other | SRC-2, answer 3 | Deferred |
| CAP-5 | Deposits for valuable tools | Involves payments, which the prototype avoids | SRC-2, answer 3 | Deferred |
| CAP-6 | More than one neighbourhood | The prototype is for one street | SRC-2, answer 2 | Deferred |

## 5. Decisions, assumptions and questions

| ID | Entry | Kind | Affects | Status |
|---|---|---|---|---|
| DEC-1 | ADO process: Agile | Decision | All | Active |
| DEC-2 | Prototype scope: CAP-1 to CAP-3; CAP-4 to CAP-6 are Later | Decision | All | Active |
| DEC-3 | The prototype must prove OBJ-1, with about 20 households on one street | Decision | All | Active |
| ASM-1 | One organiser per street is enough | Assumption | FR-1 | Open |
| Q-1 | Can a member borrow several tools at the same time? (Minor) | Open question | FR-5 | Open |
| AQ-1 | How are invitations sent (email service, link expiry)? | Architectural question | CAP-1 | Handed off |

## Changelog

| Version | Date | Type | Summary | Ref |
|---|---|---|---|---|
| v1 | 2026-11-03 | New decision | First prototype plan, after the G0 answers | DEC-1, DEC-2, DEC-3 |
| v2 | 2026-11-03 | Clarification | Breakdown approved at G3 | — |
