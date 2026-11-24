# Example: book-club

A hypothetical project, planned with the `plan` skill from an approved roadmap.

| | |
|---|---|
| **Scenario** | B — an approved roadmap, broken down directly |
| **ADO process** | Scrum: Epics and Features |
| **Rigor profile** | Standard, because there are several releases |
| **State** | In review at G3 (version 0.1), waiting for the user's approval |

## What the user asked

> Here's our approved roadmap (docs/roadmap.md). We run Scrum. Go straight to the breakdown.

The roadmap has a vision, three goals, two user types, exclusions, and three phases.

## How the skill handled it

1. **Stage 0.** The roadmap passed the readiness rubric, so Claude referenced it through a trace index instead of rewriting it. Because the user asked to go straight through, G0 was recorded as "approved in advance". These were recorded instead of asked:
   - that the project is new, as ASM-1;
   - the voting rule the roadmap leaves open, as ASM-2;
   - the tie rule, as Q-1, which is not blocking.
2. **Stages 1 and 2** were skipped: the roadmap already covers them.
3. **Stage 3.** Claude wrote 2 Epics and 6 Features, validated them, generated the review view and stopped at G3. The G3 message lists the assumptions, the open question and the priorities it proposed.

## The result

| Epic | Feature | Milestone | Priority |
|---|---|---|---|
| BCH-EP-001 Run a book club without spreadsheets | BCH-FT-001 Club setup & membership | MS-1 | Must |
| | BCH-FT-002 Meetings | MS-1 | Must |
| | BCH-FT-003 Choosing the next book | MS-1 | Must |
| | BCH-FT-006 Quality verification before public launch | MS-3 | Must |
| BCH-EP-002 Member engagement | BCH-FT-004 Discussion threads per book | MS-2 | Should |
| | BCH-FT-005 Reading progress | MS-2 | Should |

## Files

| File | What it holds |
|---|---|
| `docs/roadmap.md` | The user's roadmap (the input; never edited) |
| `docs/planning/assessment.md` | The assessment and the trace index that gives the roadmap's statements planning IDs |
| `docs/planning/decisions-raid.md` | The process decision, assumptions and the open question |
| `docs/planning/work-breakdown.yaml` | The breakdown: the file `/plotwork:push` reads |
| `docs/planning/work-breakdown.review.md` | The generated review view, for people to read |

## What to notice

- **Phases stay milestones.** Phase 3 ("Polish & performance") did not become an Epic. Its accessibility and speed checks are a verification Feature under the first Epic, targeting MS-3.
- **Phase 2 is the one exception.** It coincides with exactly one capability area, so it became BCH-EP-002, and the assessment explains why.
- **NFRs are referenced, not copied.** WCAG 2.1 AA, page speed and mobile support are `global_constraints` (NFR-1 to NFR-3).
- **Nothing is invented silently.** The roadmap gives no priorities, so they are marked "(proposed)". A detail it leaves open, the voting rule, is an assumption the user confirms at G3.
