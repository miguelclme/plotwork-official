# Project Plan — <Project name>

| | |
|---|---|
| **Project key** | <KEY> |
| **Version** | v1 |
| **Date** | <YYYY-MM-DD> |
| **Rigor profile** | Light |
| **ADO process** | <Basic · Agile · Scrum · CMMI> (DEC-1) · or "Pending — Stage 3 blocked" |

<!-- Light profile (§8.1, §12): one file holds the Assessment Record, Brief, Register, Roadmap and RAID Log.
     Same rules as the separate templates, with fewer optional sections. Label statements with the D4 labels.
     Checkpoints for Light: G0 and G3, with G1/G2 merged into G3. -->

## 1. Assessment *(required)*

1. **State and artifacts:** Scenario <A | B | C | D>. Sources: SRC-1 <…> (<status>).
2. **Reusable information and decisions:** <…>
3. **Missing or ambiguous:** <gap> (<Blocking · Material · Minor>) → <handling>
4. **Contradictions, risks, blockers:** <… or "None">
5. **ADO process:** <…> (DEC-1)
6. **Route:** Stage 0 → <…>, because <…>.

G0: <Pass · Pass with assumptions · Fail>, decided by you on <YYYY-MM-DD>.

## 2. Brief *(required)*

**Summary:** <One paragraph: what is built, for whom, why, and what is out.>

| ID | Objective | Success criterion |
|---|---|---|
| OBJ-1 | <…> | <…> |

- **Primary users:** <…>
- **Out of scope:** <… or "None yet">
- **Constraints:** <… or "None known"> (→ CON entries below)

## 3. Scope and needs *(required)*

<!-- Product-level needs only (D19). What, not how. Keep one ID per row, in the first column:
     the validation script reads IDs, priorities and statuses from these tables. -->

| ID | Capability | Priority | Milestone |
|---|---|---|---|
| CAP-1 | <…> | Must | MS-1 |

| ID | Need (FR) | Capability | Priority |
|---|---|---|---|
| FR-1 | <Users can …> | CAP-1 | Must |

**Non-functional requirements** *(conditional: they change scope)*

| ID | Statement | Applies to | D11 pattern | Priority | Target |
|---|---|---|---|---|---|
| NFR-1 | <…> | Global · CAP-n | Constraint · Capability · Verification | Must | <…> |

**Constraints and business rules** *(conditional)*

| ID | Statement | Source |
|---|---|---|
| CON-1 | <…> | <…> |

## 4. Milestones *(optional: single release → one milestone, "Release 1")*

| ID | Name | Outcome | Scope |
|---|---|---|---|
| MS-1 | Release 1 | <what is true when it is reached> | CAP-1, … |

## 5. Decisions, assumptions and questions *(required)*

| ID | Entry | Kind | Affects | Status |
|---|---|---|---|---|
| DEC-1 | ADO process: <…> | Decision | All | Active |
| ASM-1 | <…> | Assumption | <IDs> | Open |
| Q-1 | <…> (Blocking · Material · Minor) | Open question | <IDs> | Open |
| AQ-1 | <…> | Architectural question (handed downstream) | <IDs> | Open |

## Changelog

| Version | Date | Type | Summary | Ref |
|---|---|---|---|---|
| v1 | <YYYY-MM-DD> | New decision | First plan | DEC-1 |
