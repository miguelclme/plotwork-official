# Assessment Record — Book Club Hub

| | |
|---|---|
| **Project key** | BCH |
| **Version** | v1 |
| **Date** | 2026-11-02 |
| **Status** | Reviewed at G0 |

## 1. Project state and artifacts

**Scenario:** B — Existing artifacts

| ID | Source (title or file) | Date or version | Stated status | Covers (§6.3 dimensions) | Trust notes |
|---|---|---|---|---|---|
| SRC-1 | `docs/roadmap.md` | current | Approved | Purpose, users, scope, needs, NFRs, milestones | Approval confirmed by the user |

**New project:** the user did not say, and asked to go straight to the breakdown, so it is recorded as ASM-1 and listed in the G3 message for confirmation [Assumption · ASM-1].

## 2. Reusable information and approved decisions

- Vision, three goals and two user types [Decision · SRC-1, approved].
- Exclusions: selling books, video calls [Decision · SRC-1].
- Three phases, each with outcome-level content [Decision · SRC-1].
- ADO process: Scrum [Decision · DEC-1].

## 3. Missing or ambiguous information

| Gap | Area (CAP or dimension) | Severity | Proposed handling |
|---|---|---|---|
| How are tied votes resolved? | CAP-3 | Minor | Q-1, non-blocking |

## 4. Contradictions, risks and blockers

None found.

## 5. ADO process

Scrum — DEC-1

## 6. Recommended route

- **Route:** Stage 0 → 3, because the roadmap passes G1, and passes G2 for every in-scope capability, Phases 2 and 3 included.
- **Skipped stages:** Stages 1 and 2. The roadmap is referenced through the trace index below, not rewritten.
- **Rigor profile:** Standard, because there are several releases (§12).

## Maturity rubric

| Dimension | Rating | Notes |
|---|---|---|
| Purpose & objectives | Sufficient | Three goals |
| Users & stakeholders | Decomposition-ready | Organisers and members |
| Scope | Sufficient | Exclusions stated |
| Functional needs | Decomposition-ready | All phases list concrete needs |
| Non-functional needs | Sufficient | Mobile, page speed, WCAG 2.1 AA |
| Constraints & dependencies | Sufficient | None known |
| Risks & assumptions | Sufficient | None material |
| Priorities & milestones | Sufficient | Phases defined by outcomes |

## Trace index

| ID | Source section | Short label | Priority |
|---|---|---|---|
| OBJ-1 | SRC-1 Goals 1 | Run a club without spreadsheets | — |
| OBJ-2 | SRC-1 Goals 2 | More members join the discussions | — |
| OBJ-3 | SRC-1 Goals 3 | Works well on phones | — |
| CAP-1 | SRC-1 Phase 1 | Club setup & membership | Must (proposed) |
| CAP-2 | SRC-1 Phase 1 | Meetings | Must (proposed) |
| CAP-3 | SRC-1 Phase 1 | Choosing the next book | Must (proposed) |
| CAP-4 | SRC-1 Phase 2 | Member engagement | Should (proposed) |
| FR-1 | SRC-1 Phase 1, item 1 | Create a club | Must (proposed) |
| FR-2 | SRC-1 Phase 1, item 2 | Invite members by link | Must (proposed) |
| FR-3 | SRC-1 Phase 1, item 3 | Schedule meetings | Must (proposed) |
| FR-4 | SRC-1 Phase 1, item 4 | Propose and vote on the next book | Must (proposed) |
| FR-5 | SRC-1 Phase 2, item 1 | Discussion threads per book | Should (proposed) |
| FR-6 | SRC-1 Phase 2, item 2 | Reading progress | Should (proposed) |
| NFR-1 | SRC-1 Goals 3 | Works well in mobile browsers | Must (proposed) |
| NFR-2 | SRC-1 Phase 3, item 2 | WCAG 2.1 AA | Must (proposed) |
| NFR-3 | SRC-1 Phase 3, item 1 | Pages load in under 2 s on 4G | Should (proposed) |
| MS-1 | SRC-1 Phase 1 | A club completes its first meeting cycle | — |
| MS-2 | SRC-1 Phase 2 | Members discuss books in the app | — |
| MS-3 | SRC-1 Phase 3 | Quality bar verified before the public launch | — |

**Priorities.** The roadmap states none. They are proposed from the phases and goals: Phase 1 and the launch conditions (mobile, WCAG) Must, the rest Should. The G3 message lists them for confirmation [Recommendation].

**Phases.** Phase 1 and Phase 3 are milestones only. Phase 2 also coincides with exactly one capability area (CAP-4), so it yields the Epic BCH-EP-002, noted here as §8.5 rule 3 requires.

## G0 review

| Gate | Proposed result | Your decision | Date |
|---|---|---|---|
| G0 | Pass | Approved in advance by the user ("go straight to the breakdown") | 2026-11-02 |

## Changelog

| Version | Date | Type | Summary | Ref |
|---|---|---|---|---|
| v1 | 2026-11-02 | New decision | First assessment | DEC-1 |
