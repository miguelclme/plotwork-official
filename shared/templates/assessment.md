# Assessment Record — <Project name>

| | |
|---|---|
| **Project key** | <KEY> |
| **Version** | v1 |
| **Date** | <YYYY-MM-DD> |
| **Status** | Draft · Reviewed at G0 |

<!-- Stage 0 (§6). Keep it short: about ½ page for Light, 1 page for Standard, at most 2 pages for Rigorous.
     Present it for review before any rework or decomposition (G0). Label every statement (D4). -->

## 1. Project state and artifacts *(required)*

**Scenario:** <A — New idea | B — Existing artifacts | C — Partial decomposition | D — External prototype>

<!-- A project already under development is out of scope for now: stop and say so. If the user has not said
     whether the project is new, ask at G0 (or record it as an ASM when G0 is approved in advance). Never check ADO. -->

| ID | Source (title or file) | Date or version | Stated status | Covers (§6.3 dimensions) | Trust notes |
|---|---|---|---|---|---|
| SRC-1 | <e.g. initial conversation, roadmap.md> | <…> | Approved · Draft · Unknown | <…> | <age, contradictions, author's certainty> |

## 2. Reusable information and approved decisions *(required)*

- <statement> [Fact · SRC-1 §x]
- <statement> [Decision · DEC-1]

## 3. Missing or ambiguous information *(required)*

<!-- Severity (§6.4):
     Blocking = prevents an accurate breakdown of an in-scope area;
     Material = lowers quality, so proceed with an ASM;
     Minor    = record a Q and defer. -->

| Gap | Area (CAP or dimension) | Severity | Proposed handling |
|---|---|---|---|
| <what is missing> | <…> | Blocking · Material · Minor | Ask in Stage 1 or 2 · ASM-n · Q-n |

## 4. Contradictions, risks and blockers *(required)*

<!-- List both conflicting statements with their sources. Never pick one silently.
     Never define an ID here: Q-n and RSK-n are defined only in decisions-raid.md. Reference them in the last
     column. The first column is never an ID, because the validation script reads every table row whose first
     cell is an ID as that ID's definition. -->

| Conflict or risk | Sources | Proposed resolution | Logged as (defined in `decisions-raid.md`) |
|---|---|---|---|
| <…> | SRC-… | <…> [Recommendation] | Q-n · RSK-n |

## 5. ADO process *(required)*

<Basic | Agile | Scrum | CMMI> — DEC-<n>

<!-- Or write: "Pending — Stage 3 blocked". Never default to a process, and never infer it from wording (§6.6). -->

## 6. Recommended route *(required)*

- **Route:** Stage 0 → <…>, because <…>.
- **Skipped stages:** Stage <n>, because <…>.
- **Rigor profile:** <Light | Standard | Rigorous>, because <…> (§12).

## Maturity rubric *(optional for Light)*

| Dimension | Rating | Notes |
|---|---|---|
| Purpose & objectives | Absent · Partial · Sufficient · Decomposition-ready | |
| Users & stakeholders | | |
| Scope | | |
| Functional needs | | |
| Non-functional needs | | |
| Constraints & dependencies | | |
| Risks & assumptions | | |
| Priorities & milestones | | |
| Existing decomposition *(scenario C only)* | | |

## Existing decomposition review *(conditional: scenario C)*

<!-- Map by abstraction, not by label (§6.5).
     Delivery-level items found in documents (stories, PBIs, Issues, Requirements) are not recreated:
     reference them in the owning Feature's downstream_notes (D17). -->

| Item in source | Source | Finding | Action |
|---|---|---|---|
| <"Epic: …"> | SRC-n §x | Sound · Milestone in disguise · Task-sized · Duplicate · Prescribes implementation · Delivery-level | Keep → <KEY>-EP-nnn · Reclassify → MS-n · Split · Merge → … · AQ-n · downstream_notes |

## Trace index *(conditional: Stage 2 is skipped)*

<!-- Gives existing statements planning IDs without restating them (§6.5 rule 3). One ID per row.
     Give CAPs, FRs and NFRs a priority: the validation script uses it for coverage. Copy the source's priority
     when it states one. Otherwise propose one from the phases (first release Must, later ones Should) and mark it
     "(proposed)", for example "Must (proposed)"; the G3 message lists these for confirmation.
     When an entry is later deferred or dropped, add a Status column (Deferred, Dropped) instead of deleting the row:
     the validation script reads it and stops requiring coverage for that entry. -->

| ID | Source section | Short label | Priority |
|---|---|---|---|
| OBJ-1 | SRC-1 §<x> | <…> | — |
| FR-1 | SRC-1 §<x> | <…> | Must · Should · Could · Won't, plus "(proposed)" when the source states none |

## G0 review

| Gate | Proposed result | Your decision | Date |
|---|---|---|---|
| G0 | Pass · Pass with assumptions · Fail | <…> | <YYYY-MM-DD> |

## Changelog

| Version | Date | Type | Summary | Ref |
|---|---|---|---|---|
| v1 | <YYYY-MM-DD> | New decision | First assessment | — |
