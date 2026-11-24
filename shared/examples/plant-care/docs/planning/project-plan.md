# Project Plan — Plant Care Reminder

| | |
|---|---|
| **Project key** | PLT |
| **Version** | v2 |
| **Date** | 2026-11-02 |
| **Rigor profile** | Light |
| **ADO process** | Basic (DEC-1) |

## 1. Assessment

1. **State and artifacts:** Scenario A. The only source is SRC-1, the initial message: "I want a small web app to keep track of my plants and remind me when to water them." There are no documents.
2. **Reusable information and decisions:** the purpose, and two headline capabilities, tracking plants and reminders [Fact · SRC-1].
3. **Missing or ambiguous:**
   - Who the users are (Blocking for the sharing scope). Asked and answered.
   - How reminders reach the user (Blocking for reminders). Asked and answered (DEC-2).
   - Exclusions (Material). Asked and answered.
   - Hosting (Material). Asked and answered (CON-1).
4. **Contradictions, risks, blockers:** none. How reminder emails are sent is still open, and is handed downstream as AQ-1.
5. **ADO process:** Basic (DEC-1).
6. **Route:** Stage 0 → 1 → 2 → 3, because only an idea existed. Light profile: one person, three capabilities, no regulated data.

G0: Pass, decided by the user on 2026-11-02.

## 2. Brief

**Summary:** A small web app that keeps a household's house plants in one place and emails a daily reminder of the plants that need watering. It starts for one person, and later the whole household can share it. Plant identification, a shop and a native mobile app are out of scope.

| ID | Objective | Success criterion |
|---|---|---|
| OBJ-1 | Never miss a watering | No plant goes past its watering date unnoticed [Decision · DEC-3] |
| OBJ-2 | Keep plant-care notes in one place | All plants and their locations are in the app [Decision · DEC-3] |

- **Primary users:** the user first, household members later [Fact · SRC-1 answers].
- **Out of scope:** identifying plants from photos; a plant shop; a native mobile app; sharing plants outside the household [Decision · DEC-3].
- **Constraints:** free-tier hosting only (CON-1).

## 3. Scope and needs

| ID | Capability | Priority | Milestone |
|---|---|---|---|
| CAP-1 | Plant catalogue | Must | MS-1 |
| CAP-2 | Watering schedule and reminders | Must | MS-1 |
| CAP-3 | Household sharing | Should | MS-2 |

| ID | Need (FR) | Capability | Priority |
|---|---|---|---|
| FR-1 | Users can add a plant with a name, a location and an optional photo | CAP-1 | Must |
| FR-2 | Users can edit and remove their plants | CAP-1 | Must |
| FR-3 | Users can browse their plants by location | CAP-1 | Must |
| FR-4 | Users can set a watering interval for each plant | CAP-2 | Must |
| FR-5 | Users can mark a plant as watered | CAP-2 | Must |
| FR-6 | Users receive a daily email listing the plants due for watering | CAP-2 | Must |
| FR-7 | Users can invite household members | CAP-3 | Should |
| FR-8 | Household members share one plant list and watering status | CAP-3 | Should |

**Non-functional requirements**

| ID | Statement | Applies to | D11 pattern | Priority | Target |
|---|---|---|---|---|---|
| NFR-1 | The app is usable in a phone browser | Global | Constraint | Must | Core screens usable at 360 px width |

**Constraints**

| ID | Statement | Source |
|---|---|---|
| CON-1 | Hosting must fit a free tier | SRC-1 answers |

## 4. Milestones

| ID | Name | Outcome | Scope |
|---|---|---|---|
| MS-1 | Personal use | I use it daily for my own plants | CAP-1, CAP-2 |
| MS-2 | Shared household | My household shares one list | CAP-3 |

## 5. Decisions, assumptions and questions

| ID | Entry | Kind | Affects | Status |
|---|---|---|---|---|
| DEC-1 | ADO process: Basic | Decision | All | Active |
| DEC-2 | Reminders are sent by email | Decision | CAP-2 | Active |
| DEC-3 | Brief approved: objectives, users and exclusions as written above | Decision | All | Active |
| ASM-1 | One reminder email per day is enough | Assumption | FR-6 | Open |
| AQ-1 | How are reminder emails sent (service, scheduling)? | Architectural question | CAP-2 | Handed off |

## Changelog

| Version | Date | Type | Summary | Ref |
|---|---|---|---|---|
| v1 | 2026-11-02 | New decision | First plan, after the G0 answers | DEC-1, DEC-2, DEC-3 |
| v2 | 2026-11-02 | Clarification | Breakdown approved at G3 | — |
