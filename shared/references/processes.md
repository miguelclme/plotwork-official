# Process reference — Plotwork planning standard

<!-- Reference for Claude. Use §1 in Stage 0, when the process is chosen. Use the section for the selected process in
     Stage 3. Only the four built-in, unmodified Azure DevOps processes are supported. -->

This reference lists what each built-in ADO process means for this standard: what Stage 3 produces, what Tech Leads and Developers create later, and what must never appear in the output.

The work-item types listed are those of the **default built-in templates** [Established]. Exact types and fields can vary by ADO version and configuration. `/plotwork:push` validates them through MCP before it creates anything. Stage 3 never does.

## 1. Choosing the process (Stage 0)

- **Ask explicitly:** "Which built-in Azure DevOps process will this project use: Basic, Agile, Scrum or CMMI?"
- **Never default** to a process, in particular not to CMMI. This is the one G0 question with no proposed answer: do not propose or recommend a process, even as a suggestion the user can accept with "ok".
- **Never infer** the process from the words a document uses, such as "stories" or "requirements".
- **Record the answer** as a `DEC-n` in the Decision & RAID Log.
- **Custom, inherited or modified process:** it is out of scope. Say so. Stages 0–2 may continue, but Stage 3 does not start.
- **No answer yet:** Stages 0–2 continue, and the Assessment Record states "Process: pending — Stage 3 blocked".

When the user is unsure, show this guide:

| Process | Produced by this standard | Created downstream | Fits when | Character |
|---|---|---|---|---|
| **Basic** | Epic | Issue → Task | Solo or small projects with minimal ceremony | The simplest. An Issue is a general-purpose work item |
| **Agile** | Epic → Feature | User Story → Task | User-centred products delivered iteratively | Story-based, with separate Bug and Issue types for tracking |
| **Scrum** | Epic → Feature | Product Backlog Item → Task | Work in sprints against an ordered product backlog | A PBI is any valuable backlog entry. Has an Impediment type for blockers |
| **CMMI** | Epic → Feature | Requirement → Task | Formal traceability, change control or auditability matter | The most formal. Adds Risk, Issue, Change Request and Review types |

At the level this standard produces, Agile, Scrum and CMMI have the same structure. The choice still decides which delivery-level type Tech Leads and Developers create, and how formal that work is.

## 2. Rules shared by all four processes

- **Output stops at the portfolio levels** (D17). No delivery-level items and no Tasks.
- **Epic** = a large body of work with an outcome. **Feature** = a releasable capability within one milestone, and the unit handed off downstream (§9.3).
- **Titles** name an outcome or a capability, never an activity ("Recipe collection", not "Build recipe module").
- **Everything in scope is fully described** (D8). Missing information becomes a Q, and the item is `needs-elaboration`.
- **The `process` key** in `work-breakdown.yaml` is always set. It tells `/plotwork:push` which process the ADO project must use, and the team which delivery-level type to create.
- **Never in the output, in any process:** Task, Bug, test types, or RAID entries turned into work items (D13, Q3).

## 3. Basic

| | |
|---|---|
| **Produce** | Epics only (D18) |
| **Draft ID code** | `EP` |
| **Created downstream** | Issues under each Epic, then Tasks |
| **Never in the output** | Feature, Issue, Task |

- **Each Epic is one capability** (D9), about the size of a Feature in the other processes.
- **Each Epic carries the Feature-level keys:** description, scope in/out, acceptance criteria, constraints, nature, milestone, rank and `depends_on`. A `ready` Epic must pass the hand-off test (§9.1).
- **Split** an Epic when it covers two unrelated capabilities, spans two milestones, or needs more than about 8 acceptance criteria. **Combine** two Epics when they are halves of one capability.
- **Larger groupings** (an outcome spanning several capabilities) are expressed with `tags` and `traces_to` objectives. Never add a level.
- **Pitfalls:**
  - Using Issues as stand-in Features.
  - Outcome-sized Epics that are too broad for one milestone.

## 4. Agile

| | |
|---|---|
| **Produce** | Epic → Feature |
| **Draft ID codes** | `EP`, `FT` |
| **Created downstream** | User Stories under each Feature, then Tasks |
| **Never in the output** | User Story, Task, Bug, Issue (Agile's Issue is a tracking type, not Basic's Issue) |

- **Name the user in each Feature's description** ("for whom"). Downstream stories are written from the user's point of view.
- **Label enabler Features** `nature: enabler` rather than phrasing them as a user need.
- **Pitfall:** writing Features in story form ("As a … I want …"). Features stay capability titles; stories are written downstream.

## 5. Scrum

| | |
|---|---|
| **Produce** | Epic → Feature |
| **Draft ID codes** | `EP`, `FT` |
| **Created downstream** | Product Backlog Items under each Feature, then Tasks |
| **Never in the output** | Product Backlog Item, Task, Bug, Impediment |

- **`rank` matters most.** It is the starting point for the ordered product backlog.
- **The Definition of Done is a team artifact,** written downstream. Do not write it into Features. The Feature's `constraints` and `global_constraints` are the inputs to it.
- **Pitfall:** calling Features "PBIs", or using the word "Requirement" for them.

## 6. CMMI

| | |
|---|---|
| **Produce** | Epic → Feature |
| **Draft ID codes** | `EP`, `FT` |
| **Created downstream** | Requirements under each Feature, then Tasks |
| **Never in the output** | Requirement, Task, Bug, Change Request, Issue, Review, Risk |

- **Traceability carries the most weight.** Each Feature's `traces_to` lists every FR and NFR ID that Tech Leads will derive Requirements from.
- **"Shall" statements found in sources** are not recreated. They go into the owning Feature's `downstream_notes`, cited by source section.
- **RAID risks are never exported** as CMMI Risk items (Q3 rejected).
- **Pitfalls:**
  - Copying the FR register into Features one-to-one.
  - Creating Requirement items.
  - Writing Features as "The system shall …".

## 7. Conformance at a glance

These rules are enforced by `work-breakdown.schema.json` and by the checks in `validation-checklists.md`.

| Check | Basic | Agile | Scrum | CMMI |
|---|---|---|---|---|
| Allowed types | Epic | Epic, Feature | Epic, Feature | Epic, Feature |
| Parent of a Feature | n/a | Epic | Epic | Epic |
| Draft ID codes | `EP` | `EP`, `FT` | `EP`, `FT` | `EP`, `FT` |
| Delivery-level type, created downstream | Issue | User Story | Product Backlog Item | Requirement |
| Skipped levels (D10) | n/a | Not allowed | Not allowed | Not allowed |

## 8. Changing the process after a breakdown exists

| Change | What happens |
|---|---|
| Between Agile, Scrum and CMMI | Items and IDs carry over. Update `process`, bump the version, check that no text uses the old process's terms, then re-validate |
| To or from Basic | Re-run Stage 3 from the unchanged planning layer. Create a new breakdown version with new draft IDs, and mark the old file `superseded` |

Every process change is recorded as a decision (`DEC-m` supersedes `DEC-n`).
