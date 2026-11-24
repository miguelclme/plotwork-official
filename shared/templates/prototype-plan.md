# Prototype Plan — <Project name>

| | |
|---|---|
| **Project key** | <KEY> |
| **Version** | v1 |
| **Date** | <YYYY-MM-DD> |
| **Kind** | Prototype (one milestone, MS-1) |
| **ADO process** | <Basic · Agile · Scrum · CMMI> (DEC-1) · or "Pending — Stage 3 blocked" |

<!-- Prototype (written by /plotwork:prototype): one short file holds the assessment, what the prototype
     must prove, its capabilities and needs, the Later list and the RAID entries. Same rules as project-plan.md:
     label statements with the D4 labels, and keep one ID per row, in the first column, because the validation
     script reads IDs, priorities and statuses from these tables. Checkpoints: G0 and G3.
     /plotwork:plan can later grow this file into a full plan, keeping every ID. -->

## 1. Assessment *(required)*

1. **State and artifacts:** Scenario <A | B | C>. Sources: SRC-1 <…> (<status>).
2. **Reusable information and decisions:** <…>
3. **Missing or ambiguous:** <gap> (<Blocking · Material · Minor>) → <handling>
4. **Contradictions, risks, blockers:** <… or "None">
5. **ADO process:** <…> (DEC-1)
6. **Route:** Stage 0 → 3, prototype. Rigor: <Light · Rigorous, because …>.

G0: <Pass · Pass with assumptions · Fail>, decided by you on <YYYY-MM-DD>.

## 2. What the prototype must prove *(required)*

**Summary:** <One paragraph: what the prototype is, who tries it, what it must prove, and what it leaves out.>

| ID | What it must prove | How you'll know it worked |
|---|---|---|
| OBJ-1 | <…> | <observable result, e.g. "5 neighbours lend a tool in the first two weeks"> |

- **Who tries it:** <…>
- **Out of the prototype:** <… or "Only what is on the Later list">
- **Data and compliance limits:** <… or "None known"> (→ NFR or CON entries below)

## 3. In the prototype *(required)*

<!-- Product-level needs only (D19). What, not how. Every capability here targets MS-1. -->

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

**Milestone**

| ID | Name | Outcome | Scope |
|---|---|---|---|
| MS-1 | Prototype | <what is true when the prototype has proved its point> | CAP-1, … |

## 4. Later *(required)*

<!-- Every capability the sources or the user mention that is not in the prototype, one line each, with the
     status Deferred. They never become items. /plotwork:plan brings them into scope when it grows the plan.
     When nothing is deferred, write "None: the prototype covers everything mentioned so far." -->

| ID | Capability | Why later | Source | Status |
|---|---|---|---|---|
| CAP-<n> | <…> | <not needed to prove OBJ-1> | <SRC-n §x> | Deferred |

## 5. Decisions, assumptions and questions *(required)*

| ID | Entry | Kind | Affects | Status |
|---|---|---|---|---|
| DEC-1 | ADO process: <…> | Decision | All | Active |
| DEC-2 | Prototype scope: the capabilities in section 3; the rest is Later | Decision | All | Active |
| ASM-1 | <…> | Assumption | <IDs> | Open |
| Q-1 | <…> (Blocking · Material · Minor) | Open question | <IDs> | Open |
| AQ-1 | <…> | Architectural question (handed downstream) | <IDs> | Open |

## Changelog

| Version | Date | Type | Summary | Ref |
|---|---|---|---|---|
| v1 | <YYYY-MM-DD> | New decision | First prototype plan | DEC-1, DEC-2 |
