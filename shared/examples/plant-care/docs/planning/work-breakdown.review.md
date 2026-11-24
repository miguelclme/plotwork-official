<!-- generated-from: work-breakdown.yaml version=1.0 sha256=ed756b6766b80ca8cab389e5e0d40e945a12e03e1b32dff50bc824f682afbb02 -->
# Plant Care Reminder — Work breakdown v1.0 (Basic)

> Generated from `work-breakdown.yaml` v1.0 on 2026-11-03 by `render_review.py`. **Do not edit**: change the YAML and regenerate.

## 1. Summary

| Epics | Features | Ready | Needs elaboration | Blocked | Low confidence |
|---|---|---|---|---|---|
| 3 | 0 | 3 | 0 | 0 | 0 |

- **Process:** Basic · **Status:** approved · **Rigor:** Light
- **Global constraints:** NFR-1
- **Open questions:** AQ-1

## 2. Hierarchy

```text
PLT-EP-001 Plant catalogue                                    MS-1 · rank 1 · Must · ready
PLT-EP-002 Watering schedule and reminders                    MS-1 · rank 2 · Must · ready · depends_on PLT-EP-001
PLT-EP-003 Household sharing                                  MS-2 · rank 1 · Should · ready · depends_on PLT-EP-001, PLT-EP-002
```

## 3. Epic cards

### PLT-EP-001 — Plant catalogue

| Milestone | Rank | Priority | Nature | Readiness | Confidence | Size |
|---|---|---|---|---|---|---|
| MS-1 | 1 | Must | user-facing | ready | high | — |

**Outcome:** The user has all their plants, and where they live, in one place.

Users add, edit, remove and browse their plants by location. Includes the foundation needed to use the app: a deployable web app with single-user sign-in.

- **In scope:** adding a plant with a name, a location and an optional photo; editing and removing plants; browsing plants by location; a deployable web app with single-user sign-in
- **Out of scope:** identifying plants from photos; a plant shop

**Acceptance criteria**

1. A user can add a plant with a name and a location, and optionally a photo.
2. A user can edit and remove their plants.
3. A user can see their plants grouped by location.
4. Only the signed-in user can see their plants.

- **Constraints:** none of its own · global: NFR-1
- **Depends on:** none
- **Traces to:** OBJ-2, CAP-1, FR-1, FR-2, FR-3 · **Sources:** SRC-1, project-plan.md §2
- **Open questions:** none · **Downstream notes:** none

### PLT-EP-002 — Watering schedule and reminders

| Milestone | Rank | Priority | Nature | Readiness | Confidence | Size |
|---|---|---|---|---|---|---|
| MS-1 | 2 | Must | user-facing | ready | medium | — |

**Outcome:** The user never misses a watering.

Each plant has a watering interval. The user marks plants as watered and receives one daily email listing the plants that are due.

- **In scope:** a watering interval per plant; marking a plant as watered; a daily reminder email
- **Out of scope:** push notifications (the native app is out of scope)

**Acceptance criteria**

1. Each plant can have its own watering interval.
2. Marking a plant as watered restarts its interval.
3. The user receives at most one email per day, listing every plant that is due or overdue.

- **Constraints:** none of its own · global: NFR-1
- **Depends on:** PLT-EP-001
- **Traces to:** OBJ-1, CAP-2, FR-4, FR-5, FR-6 · **Sources:** SRC-1, project-plan.md §3
- **Open questions:** AQ-1 · **Downstream notes:** none

### PLT-EP-003 — Household sharing

| Milestone | Rank | Priority | Nature | Readiness | Confidence | Size |
|---|---|---|---|---|---|---|
| MS-2 | 1 | Should | user-facing | ready | high | — |

**Outcome:** A household keeps one shared list of plants.

The user invites household members, who then see and update the same plants and watering status.

- **In scope:** inviting a household member; a shared plant list and watering status
- **Out of scope:** sharing plants with people outside the household

**Acceptance criteria**

1. A user can invite a household member.
2. Invited members see the same plants and watering status.
3. When any member marks a plant as watered, every member sees it.

- **Constraints:** none of its own · global: NFR-1
- **Depends on:** PLT-EP-001, PLT-EP-002
- **Traces to:** OBJ-1, CAP-3, FR-7, FR-8 · **Sources:** SRC-1, project-plan.md §3
- **Open questions:** none · **Downstream notes:** none

## 5. Traceability coverage

| Planning ID | Priority | Covered by | Status |
|---|---|---|---|
| CAP-1 | Must | PLT-EP-001 | Covered |
| CAP-2 | Must | PLT-EP-002 | Covered |
| CAP-3 | Should | PLT-EP-003 | Covered |
| FR-1 | Must | PLT-EP-001 | Covered |
| FR-2 | Must | PLT-EP-001 | Covered |
| FR-3 | Must | PLT-EP-001 | Covered |
| FR-4 | Must | PLT-EP-002 | Covered |
| FR-5 | Must | PLT-EP-002 | Covered |
| FR-6 | Must | PLT-EP-002 | Covered |
| FR-7 | Should | PLT-EP-003 | Covered |
| FR-8 | Should | PLT-EP-003 | Covered |

## 6. Constraints and NFR coverage (D11)

| NFR | Priority | Global | Constrains | Implemented or verified by |
|---|---|---|---|---|
| NFR-1 | Must | Yes | — | — |

## 7. Dependencies

| Item | Depends on | Crosses Epics? |
|---|---|---|
| PLT-EP-002 | PLT-EP-001 | Yes |
| PLT-EP-003 | PLT-EP-001 | Yes |
| PLT-EP-003 | PLT-EP-002 | Yes |

## 8. Open questions and assumptions

| ID | Question or assumption | Severity | Affects |
|---|---|---|---|
| AQ-1 | How are reminder emails sent (service, scheduling)? | — | PLT-EP-002 |
| ASM-1 | One reminder email per day is enough | Assumption | FR-6 |

## 9. Not ready

_Every item is ready._

## 10. Validation report

```text
Validation — PLT work breakdown v1.0 (process: Basic) · checks run by render_review.py
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
Ready 3 · Needs elaboration 0 · Blocked 0 · Low confidence 0
Mechanical result: FAIL 0 · WARN 0 · PASS 14 · SKIP 2. Review checks R1–R14 are done by the independent reviewer.
```
