# Plotwork planning standard

> The method behind Plotwork. The plugin's skills, templates and scripts implement it.

| | |
|---|---|
| **Version** | **v1.1.** Every decision in §2 is settled |
| **Date** | 2026-11-16 |
| **Scope** | Stages 0–3. Built-in, unmodified Azure DevOps processes only: Basic, Agile, Scrum, CMMI. **The Stage 3 output stops at Epics and Features** (Basic: Epics), and **everything in scope is fully described** |

**Who this document is for.** You don't need it to use Plotwork; the [user guide](../../user-guide/README.md) covers that. This is the full method: every rule and the reason behind it. Read it when you want to know why Plotwork works the way it does, or before you change one of its rules. The skills read it only to settle a doubt about a rule. Throughout, "you" is the person whose project is being planned, and "Claude" is Claude running the plugin.

**How to use this document:**

1. **§2** lists every decision and its rule. It is the quick reference.
2. **§5–§9** define the method, stage by stage. **§10–§12** define its inputs, checks and scaling.
3. **§13** applies the method to four worked examples.
4. **§15** lists the limits the plugin always keeps, and **§16** says how to change the standard.

**Labels used in this document**

- **[Established]**: widely used industry practice, or a documented default of the built-in ADO process templates.
- **[Recommended]**: a choice made for this standard where common practice varies or says nothing.

Both labels only say where a rule comes from. A **[Recommended]** rule applies just like an **[Established]** one.

ADO statements describe the *unmodified built-in templates* only. Exact fields, rules and link types vary by ADO version and configuration. `/plotwork:push`, the creation workflow, must validate them through MCP. This document deliberately names no ADO field.

---

## Contents

0. [Version history](#0-version-history)
1. [Executive summary](#1-executive-summary)
2. [Decisions](#2-decisions)
3. [Problem analysis and challenged assumptions](#3-problem-analysis-and-challenged-assumptions)
4. [Core model and boundaries](#4-core-model-and-boundaries)
5. [End-to-end methodology](#5-end-to-end-methodology)
6. [Stage 0: Intake standard](#6-stage-0--intake-standard)
7. [Stage 1: Clarification standard](#7-stage-1--clarification-standard)
8. [Stage 2: Planning artifact standard](#8-stage-2--planning-artifact-standard)
9. [Stage 3: Process-aware decomposition standard](#9-stage-3--process-aware-decomposition-standard)
10. [Context schema](#10-context-schema)
11. [Validation framework](#11-validation-framework)
12. [Adaptive rules](#12-adaptive-rules)
13. [Worked examples](#13-worked-examples)
14. [Failure modes and trade-offs](#14-failure-modes-and-trade-offs)
15. [Plugin boundaries](#15-plugin-boundaries)
16. [Changing the standard](#16-changing-the-standard)

---

## 0. Version history

| Version | Date | Changes |
|---|---|---|
| **v1.0** | 2026-11-09 | First version |
| **v1.1** | 2026-11-16 | New decision D20: a working app prototype is a source, not the product. Adds scenario D (§5.2, §6.1), §6.9, and a plugin boundary for Figma (§15) |

---

## 1. Executive summary

The core idea: **plan once in tool-independent terms, then represent that plan in the hierarchy of the ADO process you selected.**

- **Two layers** (D1)
  - The **planning layer** holds objectives, scope, product-level needs, milestones, decisions and risks. It is identical whichever process you choose.
  - The **representation layer** is the work breakdown, named and nested exactly as the selected process defines it.
- **Portfolio levels only** (D17). Stage 3 produces Epics and Features (Basic: Epics, D18). Tech Leads and Developers create the delivery-level items (Issue, User Story, PBI, Requirement) and the Tasks downstream.
- **Everything in scope is fully described** (D8). Every Epic and Feature found in the idea or in the documents gets its full description, whichever milestone it targets. You or your team update it later through change handling.
- **Four stages, routed by Stage 0.** Stages 1 and 2 run only for the *areas* that need them. Existing approved material is referenced, never rewritten to fit a template.
- **Four gates (G0–G3)**, each a short checklist. A gate may pass *with documented assumptions*. It never passes with hidden gaps.
- **Process selection is an explicit input.** Without it, Stages 0–2 can finish but Stage 3 cannot start. Nothing defaults to CMMI, and the process is never inferred from wording.
- **Output** (D5, Q2). A canonical `work-breakdown.yaml`, plus a readable review view generated from it by a script. Claude writes the view only when the script cannot run. Draft IDs cannot be confused with ADO IDs.
- **Rigor scales** through three profiles (Light, Standard, Rigorous), which can be raised for a single risky area.

> **Guiding rule:** Assess first; reuse what exists; standardize the process; adapt the hierarchy; defer Tasks; stop before ADO integration. Delivery-level items are deferred along with the Tasks (D17).

---

## 2. Decisions

### 2.1 Decision register

These are the design choices the rest of the standard follows. The plugin's files cite them by ID (for example D17), so an ID is never reused or renumbered. D16 is retired and Q3 was rejected; both stay listed so that their IDs stay taken.

| ID | Decision | Rule | Status |
|---|---|---|---|
| **D1** | Separate planning from representation | Two layers: a tool-independent planning layer, and a process-specific representation layer that holds the work breakdown only | In force |
| **D2** | No neutral intermediate hierarchy | The planning layer keeps a capability map plus product-level needs. Stage 3 decomposes directly into the selected process's types | In force |
| **D3** | Artifact set | Five logical artifacts plus the Work Breakdown, physically merged by rigor profile (Light: one `project-plan.md`) | In force |
| **D4** | Status labels | Fact / Decision / Assumption / Recommendation / Open Question | In force |
| **D5** | Output format | Canonical `work-breakdown.yaml` plus a generated `work-breakdown.review.md` that is never edited by hand | In force |
| **D6** | Draft IDs | `<KEY>-<TYPE>-<nnn>`, with type codes `EP` and `FT`. Never numeric-only, never renumbered, never reused. `ado_id: null` is reserved | In force |
| **D7** | Prioritization | priority (MoSCoW), `depends_on`, rank, milestone and risk, kept as separate attributes | In force |
| **D8** | Depth of description | **Everything in scope is fully described**, whichever milestone it targets. Missing information is asked for, or recorded as a Q; it is never invented. Later updates by you or your team follow change handling (§8.6). Details in §2.2 | In force |
| **D9** | Granularity in Basic | Basic Epics are sized like Features in the other processes, one capability each. Larger groupings use traceability and tags. No level is invented | In force |
| **D10** | No skipped levels | In Agile, Scrum and CMMI, every Feature has an Epic parent | In force |
| **D11** | Non-functional and cross-cutting needs | The Constraint, Capability and Verification patterns, applied at Feature level (§2.2) | In force |
| **D12** | No estimates at initialization | No ADO estimates. An optional `size_hint` (S/M/L/XL) is used only to decide Feature splits | In force |
| **D13** | Types left out of the breakdown | Delivery-level types (Basic Issue, User Story, PBI, Requirement), Task, Bug, Impediment, Agile Issue, CMMI Risk / Change Request / Review / Issue, and test types. RAID entries are never exported as work items | In force |
| **D14** | Rigor profiles | Light / Standard / Rigorous, which can be raised for a single area | In force |
| **D15** | Ownership by role | Product Owner, Developer/Architect, and Facilitator (Claude never approves). Tech Leads and Developers own the delivery-level items downstream | In force |
| **D16** | Phrasing of delivery items | Retired. There are no delivery items in the output (D17). Titles use outcome phrasing (§9.1) | Retired |
| **D17** | Depth of the Stage 3 output | Portfolio levels only. Agile, Scrum, CMMI: Epic → Feature. Basic: Epic. Delivery-level items and Tasks are created downstream by Tech Leads and Developers | In force |
| **D18** | Basic output | Epics only. Each Basic Epic carries the Feature-level content: description, scope in/out, acceptance criteria, constraints. Basic Issues are never used as stand-in Features | In force |
| **D19** | Depth of the Requirements & Scope Register | Kept in the planning layer, at product level: capability map, headline FRs per capability, NFRs, business rules, constraints. No technical requirements | In force |
| **D20** | A working app prototype as a source | The prototype's code is a source, not the product: read only, never run, never changed. Each screen is Working, Mocked or Placeholder, and only Working behaviour becomes a need without asking. The output names no technology (§6.9) | In force |
| **Q1** | Location of planning files | `docs/planning/` | In force |
| **Q2** | How the review view is rendered | Option C: a script renders it. Claude writes it only when the script cannot run, and marks it "rendered manually" (§2.2) | In force |
| **Q3** | Export RAID risks as CMMI Risk items | Not offered | Rejected |

### 2.2 Rules in detail

#### D8: everything in scope is fully described

**The rule.** Stage 3 fully describes everything in scope: everything in the new idea, and everything in the documents that already describe part of the idea or its implementation.

| Process | What "fully described" means |
|---|---|
| Agile, Scrum, CMMI | Every **Epic** has a title, outcome, scope boundary, priority and traces. Every **Feature** has a description, scope in/out, acceptance criteria, constraints, dependencies, priority, milestone, rank and traces |
| Basic | Every **Epic** carries the Feature-level content listed above (D18) |

- **It applies to every milestone.** Milestones still exist (Roadmap, §8.5), and they still drive `milestone`, `rank` and dependencies. They no longer decide how much detail an item gets.
- **Full description is not invention.** Only the planning layer and the sources are used. Where information is missing, Claude either asks in Stage 1 or 2, or marks the item `needs-elaboration` with a Q that says what is missing.
- **Later updates.** After G3 approval, you or your team update the breakdown when you learn something. Each update follows change handling (§8.6):
  - it is recorded as a new decision, a modification or a clarification;
  - only the affected items change;
  - IDs persist (D6);
  - the version is bumped, and validation (§11) runs again.
- **Consequence for Stages 1 and 2.** G2 now needs every in-scope capability to be *Decomposition-ready* (§8.7). Expect a few more questions about later phases up front.

**Why.** Every Feature can then be handed to a Tech Lead or Developer without going back to product questions (the hand-off test, §9.1), whichever milestone it targets. The alternative, a rolling wave that fully describes only the next milestone, was considered and not chosen. The cost accepted is in §14.2: Features for later milestones may need updating, and Stages 1 and 2 ask more questions up front.

#### D11: non-functional and cross-cutting needs

**The problem it solves.** Non-functional needs (security, performance, accessibility, reliability, compliance) usually apply to many Features at once. Two mistakes are common:

1. Copying the same NFR text into every Feature. The copies then drift apart.
2. Creating an "NFR Epic" that collects the statements but contains no actual work.

**The rule.** Classify each NFR with the three tests below. An NFR can match more than one pattern.

| Pattern | Test | What you create | Example |
|---|---|---|---|
| **Constraint** | It limits *how well*, or *under which conditions*, Features must work | **Nothing new.** Reference it by ID on the Features it affects (`constraints: [NFR-2]`), or once in `global_constraints` when it applies to every Feature | "Usable on a phone-sized screen" (global). "Personal data encrypted in transit and at rest" (on the Features that handle personal data) |
| **Capability** | Meeting it requires building something that would not otherwise exist | An **enabler Feature** (Basic: an enabler Epic) that traces to the NFR | "Data can be restored after loss" → the Feature "Backup and restore". "Every booking change is traceable" → the Feature "Audit trail" |
| **Verification** | Proving it takes dedicated effort beyond normal delivery work | A **verification Feature** when that effort is substantial. Otherwise, an acceptance criterion on the Feature concerned | "Handles 500 concurrent bookings" → the Feature "Load verification of the booking flow". "WCAG 2.1 AA" → an audit Feature before the public release |

For example, a security NFR is a Constraint on the Features that handle personal data. It may *also* need a Verification Feature, such as a security review before the beta.

**Where enabler and verification Features live.** Under the Epic they affect most. A "Platform & operations" Epic is acceptable only when it holds real Capability or Verification Features, never just a list of NFR statements.

**Why it matters.** The breakdown stops at Features (D17), so the Feature is where NFRs reach Tech Leads and Developers. A Feature's `constraints`, together with `global_constraints`, tell them which NFRs every delivery item they create beneath that Feature must respect.

**In the YAML:**

```yaml
global_constraints: [NFR-1]            # Constraint that applies to every Feature
items:
  - draft_id: CSP-FT-001
    type: Feature
    title: Find and book an appointment
    constraints: [NFR-3, NFR-4]        # Constraint pattern
  - draft_id: CSP-FT-007
    type: Feature
    title: Audit trail
    nature: enabler                    # Capability pattern
    traces_to: [NFR-6]
  - draft_id: CSP-FT-008
    type: Feature
    title: Security verification before beta
    nature: verification               # Verification pattern
    traces_to: [NFR-3, NFR-4, NFR-5, NFR-6]
```

**Validation.** Every Must NFR must be covered by at least one pattern, and the coverage table shows which one. NFR text copied into several Features produces a warning.

#### Q2: how the review view is rendered

**Context.** D5 makes `work-breakdown.yaml` the single source of truth. The review view, `work-breakdown.review.md`, is **generated** from it: the tree, the Feature cards, the coverage tables and the validation report. It is the readable version of the breakdown: what you review and approve at G3, and what you share with others. It is never edited by hand. Q2 decides *what generates it*. It is an implementation detail of the plugin and does not change the method.

| Option | How it works | Pros | Cons |
|---|---|---|---|
| **A. Script only** | A small script in the plugin (e.g. `render_review.py`) reads the YAML and writes the Markdown. Claude runs it after every change | The same input always gives the same output. Nothing is paraphrased or skipped. The version stamp is guaranteed to match. Fast and cheap | Needs Python (or similar) on the machine. One more file to maintain |
| **B. Claude writes it** | Claude reads the YAML and writes the Markdown each time | No dependencies. Can add explanatory prose | The output can vary between runs. Claude can summarise, reorder or miss items, which is exactly the drift D5 is meant to prevent. Costs more tokens on large breakdowns |
| **C. Script, with Claude as fallback** (chosen) | The script by default. Claude writes the view only when the script cannot run, and marks it "rendered manually" | The reliability of A with the resilience of B | Slightly longer skill instructions |

The same choice applies to the validation script (`validate_breakdown.py`), which runs the mechanical checks of §11. Neither script ever contacts ADO.

**Decision:** option C.

---

## 3. Problem analysis and challenged assumptions

The recurring failure is not a lack of planning. Each plan has a different shape, mixes roadmap phases with work items, and carries no explicit readiness or traceability. As a result, turning it into a backlog becomes a fresh, inconsistent design exercise every time.

| # | Common assumption | Challenge | Consequence for the standard |
|---|---|---|---|
| A1 | "The roadmap is the backlog in rough form." | Roadmap phases are time- or outcome-based checkpoints. Work items are units of work. Phases often bundle unrelated capabilities | Milestones stay in the Roadmap, and items reference them (§8.5) |
| A2 | "More documentation means more readiness." | Readiness means having no *blocking* gaps. Page count is irrelevant | Gates test for blocking gaps. A Light project can live in one file (D3, D14) |
| A3 | "Epic → Feature → Requirement is the standard hierarchy." | That hierarchy belongs to CMMI. Basic has two levels, and Agile and Scrum use User Story and PBI | The representation is chosen per process (D1, §9.2) |
| A4 | "A requirement is a work item." | A requirement is a *statement of need* in the planning layer. A work item is a *unit of planned delivery*. One item can satisfy several requirements, and the reverse also happens | The Register keeps product-level needs (D19), and Features trace to them (§9.7). Requirement-level work items are created downstream (D17) |
| A5 | "User Story, PBI, Issue and Requirement are synonyms." | They differ in perspective, formality and how they are used | This standard does not produce them (D17). The selected process is recorded, so the downstream workflow creates the right type (§9.2) |
| A6 | "Stages run once, in order." | Stage 3 regularly exposes gaps | Loop-backs cover only the affected area (§5.3) |
| A7 | "A document is correct because it exists." | Documents age, contradict each other, and mix wishes with decisions | Stage 0 classifies every statement (D4) and lists contradictions |
| A8 | "Initialization should go down to delivery items and Tasks." | Delivery items and Tasks are technical. They depend on design decisions that Tech Leads and Developers make later | Decomposition stops at Epics and Features (D17) |
| A9 | "The process choice is only naming." | It changes the number of levels (Basic) and which delivery-level type is created downstream | The process must be chosen before Stage 3 and is never inferred |
| A10 | "Cross-cutting concerns need their own Epic." | They usually *constrain* many items, and only some of them produce work | Handled through the NFR patterns (D11) |

The genuine design choices, where reasonable people disagree, are collected in §2. The rest of this document follows from them.

---

## 4. Core model and boundaries

### 4.1 Two layers

```text
PLANNING LAYER  (tool-independent: the same for every process)
  Sources (SRC) ──► Project Brief (OBJ) ──► Requirements & Scope Register (CAP, FR, NFR, BR, CON)
                          │                              │
                          └──────► Roadmap (MS) ◄────────┘
  Decision & RAID Log (DEC, ASM, RSK, DEP, Q, AQ) ── referenced by everything above

        │   + selected ADO process (explicit user input, never inferred)
        ▼

REPRESENTATION LAYER  (process-specific: Stage 3 only, portfolio levels, D17)
  Work Breakdown
    Basic : Epic
    Agile : Epic ──► Feature
    Scrum : Epic ──► Feature
    CMMI  : Epic ──► Feature
  every item carries: draft_id · parent · traces_to · milestone · depends_on · constraints · readiness

        │   hand-off: work-breakdown.yaml (reviewed and approved, not yet in ADO)
        ▼

OUT OF SCOPE (downstream)
  ADO work-item creation (/plotwork:push, through MCP)
  Delivery-level items, created by Tech Leads / Developers under each Feature (Basic: each Epic):
    Basic Issue · Agile User Story · Scrum Product Backlog Item · CMMI Requirement  ──►  Tasks
  Specification · architecture · development
```

### 4.2 Planning-layer identifiers

| Prefix | Meaning | Lives in |
|---|---|---|
| `SRC-n` | A source document or conversation, cited with a section (`SRC-2 §4.1`) | Assessment Record |
| `OBJ-n` | Objective or desired outcome | Project Brief |
| `CAP-n` | Capability: one scope area of the capability map | Requirements & Scope Register |
| `FR-n` / `NFR-n` | Functional / non-functional requirement | Register |
| `BR-n` | Business rule | Register |
| `CON-n` | Constraint: an imposed "how" (e.g. "must run on the existing host") | Register |
| `MS-n` | Milestone | Roadmap |
| `DEC-n` | Decision | Decision & RAID Log |
| `ASM-n` / `RSK-n` / `DEP-n` / `Q-n` | Assumption / risk / external dependency / open question | Decision & RAID Log |
| `AQ-n` | Architectural question, handed to downstream architecture work and not answered here | Decision & RAID Log |

Planning IDs are local to the project. Draft work-item IDs (D6) have a different shape (`KEY-TYPE-nnn`), so they cannot be mistaken for planning IDs or for ADO's numeric IDs.

### 4.3 Responsibility boundaries

| # | Responsibility | In this standard? | Interface |
|---|---|---|---|
| 1 | Project intake and planning | **In scope** (Stages 0–2) | Produces the planning layer |
| 2 | Process-aware work breakdown | **In scope** (Stage 3) | Ends with an approved `work-breakdown.yaml` |
| 3 | Creating work items in a project-management system | Out: `/plotwork:push` | Reads the YAML, validates the schema through MCP, records ADO IDs |
| 4 | Detailed specification, technical design and delivery-level items | Out: separate workflows (Tech Leads / Developers) | Picks up Features (Basic: Epics) marked `ready`, creates the process's delivery-level items beneath them (Issue / User Story / PBI / Requirement), then Tasks |
| 5 | Architectural decisions and documentation | Out: separate workflows | Receives the AQ list, and may feed decisions back as DEC entries |
| 6 | Development, testing and validation | Out: separate workflows | none |

### 4.4 Hand-off contract

Downstream workflows can rely on the following, and on nothing more:

- There is one `work-breakdown.yaml` per project, with `process` set to `Basic`, `Agile`, `Scrum` or `CMMI`, and `status: approved`.
- Every item is an Epic or a Feature (Basic: Epics only), with a valid parent, a title, a description and a readiness state. Features marked `ready` (Basic: Epics) have a scope boundary, acceptance criteria and their constraints.
- There are no delivery-level items and no Tasks (D17).
- Every reference resolves to a planning-layer ID that exists.
- No key in the YAML implies an ADO field name. Mapping keys to fields is the creation workflow's job.

---

## 5. End-to-end methodology

### 5.1 Stages at a glance

| | **Stage 0: Assessment & Intake** | **Stage 1: Clarification** | **Stage 2: Standardized Planning** | **Stage 3: Process-Aware Work Breakdown** |
|---|---|---|---|---|
| **Runs** | Always | Only when G1 is not yet met | Only for areas that do not meet G2 | Always. It is the target, and it needs a selected process |
| **Objective** | Find out what exists, how good it is, which route to take, and which process applies | Establish purpose, users, scope and success | Make the planning information *just* sufficient for a dependable breakdown | Produce a validated, process-specific portfolio backlog: Epics and Features (Basic: Epics) |
| **Inputs** | Your description, any documents, the process choice if known | Gaps from the assessment, your answers | Brief, sources, gaps from the assessment | A ready planning layer, the selected process, the rigor profile |
| **Activities** | Inventory sources, classify statements, rate maturity, find gaps and contradictions, propose route and rigor | Targeted rounds of questions, then a draft Brief | Fill the Register and capability map, the Roadmap if needed, and the RAID Log; resolve conflicts | Decompose, link, trace, prioritize, validate |
| **Output** | Assessment Record (concise) | Project Brief (new or completed) | Updated or completed planning artifacts | `work-breakdown.yaml` plus the review view |
| **Gate** | **G0**: you have reviewed the assessment | **G1**: clarity exit criterion (§7.3) | **G2**: ready for decomposition (§8.7) | **G3**: breakdown validated (§11) and approved by you |
| **Skipped when** | Never | Existing material already passes G1 | Existing material passes G2 for every in-scope area | Never |

### 5.2 Route matrix

| Entry scenario | Typical route | Notes |
|---|---|---|
| **A**: New idea | 0 → 1 → 2 (often Light) → 3 | Stage 2 is often a single combined file |
| **B**: Existing roadmap or plan | 0 → 3, or 0 → 2 (gap-fill only) → 3 | The roadmap is never regenerated to match a template. A *trace index* adds IDs instead (§6.5) |
| **C**: Partial decomposition in documents | 0 → 2 (gap-fill) → 3, continuing from the deepest *sound* level, up to Feature level | Sound Epics and Features are kept and relabelled with the process's type names. Unsound ones are reworked. Delivery-level items are referenced in `downstream_notes`, not recreated (D17) |
| **D**: Working app prototype | 0 → 2 (gap-fill) → 3 | The code is read, never run. Every screen gets a state, and what the code can't show is asked at G0 (§6.9) |
| Process not chosen yet | 0 → 1 / 2 as needed → **wait** | Planning finishes. Stage 3 waits for your explicit choice |
| ADO backlog already populated | **Stop** | Out of scope. Say so and do not proceed |

### 5.3 Transitions and loop-backs [Recommended]

- **Forward:** move on only when the gate passes, or passes *with documented assumptions*. Each such assumption has an ASM ID and appears in the review view.
- **Localized loop-back:** when Stage 3 hits a blocking gap, mark the affected Epic or Feature `blocked`, record a Q, and return to Stage 1 or 2 *for that area only*. The rest of the breakdown carries on.
- **Change after approval:** apply the change-handling rules (§8.6) and re-run Stage 3 only for the affected branches.
- **Process change:** re-run Stage 3 from the unchanged planning layer and produce a new breakdown version. The previous file is kept and marked `superseded`. Between Agile, Scrum and CMMI, the Epics and Features usually carry over unchanged with the same IDs. A change to or from Basic restructures the breakdown and gets new draft IDs.

### 5.4 Checkpoints

You review at up to four points, depending on the rigor profile:

1. After G0. Always.
2. After the Brief, if Stage 1 ran.
3. At G2. Standard and Rigorous only; in Light it is merged into G3.
4. At G3. Always.

Claude proposes *pass*, *pass with assumptions* or *fail*, with reasons. **Claude never marks a gate as passed on your behalf.**

---

## 6. Stage 0 — Intake standard

### 6.1 Identify the entry scenario

| Signal | Scenario |
|---|---|
| Only a description or a conversation, no documents | **A**: New idea |
| A roadmap, plan, specification or requirements document, with no work-item outline | **B**: Existing artifacts |
| Documents that contain Epics, Features, stories, issues or any list of prospective work items, under any name | **C**: Partial decomposition |
| The code of a working app prototype, built to agree the product with the client | **D**: App prototype (§6.9) |
| An ADO backlog that already holds work items for this project | **Out of scope**: stop and say so |
| A mix of the above | Treat it as the most advanced scenario present, and assess each artifact separately |

### 6.2 Artifact inventory

For each source, record:

- an ID (`SRC-n`);
- its title or file name;
- its date or version;
- its stated status (approved, draft or unknown);
- its coverage (which §6.3 dimensions it informs);
- trust notes (age, contradictions, author's certainty).

### 6.3 Maturity rubric

Rate each dimension **Absent / Partial / Sufficient / Decomposition-ready**. *Sufficient* means there is enough to plan. *Decomposition-ready* means there is enough to write items with acceptance criteria.

| Dimension | *Sufficient* when … | *Decomposition-ready* when … |
|---|---|---|
| Purpose & objectives | The problem and 1–5 objectives are stated | Objectives have success measures, even qualitative ones |
| Users & stakeholders | The primary user type is known | User goals are known for each capability |
| Scope | In-scope capabilities are listed and key exclusions stated | A capability map with boundaries exists, and the MVP is separated from later work |
| Functional needs | Headline needs exist for each capability | The needs of every in-scope capability are clear enough to define its Features and their acceptance criteria (D8, D19) |
| Non-functional needs | The relevant quality concerns are named | Those concerns have targets or acceptance measures |
| Constraints & dependencies | Known constraints are listed, or "none known" is stated explicitly | Their impact on scope is understood |
| Risks & assumptions | The major ones are listed | Each one has a mitigation or an owner role |
| Priorities & milestones | A rough order or an MVP is defined | Milestones are defined as outcomes, with priorities per capability |
| Existing decomposition *(C only)* | Items exist | Items sit at consistent levels, are not duplicated, and are traceable |

### 6.4 Statement classification and gap analysis

- Every extracted statement gets a status label (D4).
- A statement counts as a **Decision** only with evidence of approval: the document says it was decided, or you confirm it. Otherwise it is a **Fact**, meaning only that it is documented, or an **Assumption**.
- **Gap severity** [Recommended]:
  - **Blocking**: prevents an accurate breakdown of an in-scope area, e.g. an unknown primary user or contradictory scope. Either resolve it or mark the area `blocked`.
  - **Material**: lowers quality. Proceed with an explicit assumption (`ASM-n`).
  - **Minor**: record it as a `Q-n` and defer it.
- **Contradictions:** list both statements with their sources and propose a resolution, labelled as a Recommendation. Never pick one silently.

### 6.5 Reuse rules [Recommended]

1. **Reference, don't copy.** The original document remains the source of truth for its own content.
2. **Preserve useful structure.** Keep the source's headings, phases and numbering, and add IDs *alongside* them, not instead of them.
3. **Use a trace index when Stage 2 is skipped.** The Assessment Record carries a small table (`ID → source section → short label`) that gives the existing statements OBJ, CAP, FR or MS IDs without restating them. This keeps traceability without rewriting an approved roadmap.
4. **Fill only material gaps.** Additions go into the standard artifacts with the note "added in Stage 2".
5. **Map by abstraction, not by label** (scenario C). Something a document calls an "Epic" that is really a milestone becomes an MS. A "Feature" that is really a Task-sized step is folded into acceptance criteria or deferred.
6. **Keep delivery-level content for downstream** (scenario C, D17). Stories, PBIs, Issues or Requirements found in documents are not recreated. The Feature they belong to (Basic: the Epic) references them in `downstream_notes`, so Tech Leads and Developers can reuse them.

### 6.6 Process selection

Rules [Recommended]:

- **Ask explicitly:** "Which built-in Azure DevOps process will this project use: Basic, Agile, Scrum or CMMI?"
- **Never default** (in particular not to CMMI). **Never infer** the process from the words a document uses, such as "stories" or "requirements".
- If you are unsure, Claude shows the guide below and you choose. The choice is recorded as a `DEC-n`.
- **While the choice is pending,** Stages 0–2 proceed, and the assessment states: "Process: pending — Stage 3 blocked".
- **Custom, inherited or modified process** stated or detected: out of scope. Say so.

**Short guide for choosing** [Established for the hierarchies and types of the default templates; the "fits when" column is Recommended]:

| Process | Produced by this standard (D17) | Created downstream | Fits when | Character |
|---|---|---|---|---|
| **Basic** | Epic | Issue → Task | Solo or small projects where you want minimal ceremony | The simplest. An Issue is a general-purpose work item |
| **Agile** | Epic → Feature | User Story → Task | User-centred products delivered iteratively | Story-based, with separate Bug and Issue types for tracking |
| **Scrum** | Epic → Feature | Product Backlog Item → Task | Work in sprints against an ordered product backlog | A PBI is any valuable backlog entry. Has an Impediment type for blockers |
| **CMMI** | Epic → Feature | Requirement → Task | Formal traceability, change control or auditability matter | The most formal. Adds Risk, Issue, Change Request and Review types |

At the level this standard produces, Agile, Scrum and CMMI have the same structure. The choice still matters: it decides which delivery-level type Tech Leads and Developers create, and how formal that downstream work is.

### 6.7 Assessment output template

```markdown
## Assessment Record — <project> (v<n>, <date>)
1. Project state & artifacts: Scenario <A|B|C|D>. Sources: SRC-1 … (status, coverage)
2. Reusable information & approved decisions: <bullets with SRC refs; DEC-n>
3. Missing or ambiguous information: <gap list with severity>
4. Contradictions, risks, blockers: <list with sources>
5. ADO process: <Basic|Agile|Scrum|CMMI> (DEC-n)  |  Pending — Stage 3 blocked
6. Recommended route: Stage <…> because <…>; skip Stage <…> because <…>
   Rigor profile: <Light|Standard|Rigorous> because <…>
(Trace index — only when Stage 2 is skipped)
```

**Proportionality** [Recommended]: about ½ page for Light, about 1 page for Standard, and at most 2 pages for Rigorous. The assessment is a decision aid, not a report.

### 6.8 Gate G0

The assessment has been presented, and you have confirmed or corrected the scenario, route, rigor profile and process status. **No substantial rework or decomposition happens before G0.**

### 6.9 App prototypes as sources (D20) [Recommended]

Some teams don't write requirements first. They build a working prototype with the client, on another platform, and change it until the client is happy. This *external prototype* then *is* the agreed product, but only for what it really does. The `from-app` skill plans from its code, and `from-app-update` applies later changes, from a newer version of the code or from a document. Plans made this way are recognised by their App Inventory.

**The prototype is a source, not the product.**
- It is `SRC-1`. The documents found inside it (notes, plans, a roadmap) are sources of their own.
- It doesn't make the project "under development". The stop in §5.2 still applies when the product itself is being built, or its ADO backlog holds work items.
- Whether the team builds the product new, using the prototype as the reference, or continues from the prototype's code is asked at G0 and recorded as a DEC. Either answer goes on.

**Read, never run.** The code is read only. Nothing is installed, built or started, because that would run code nobody has reviewed. Nothing is written inside the prototype's folder, because it may sync back to the tool that built it.

**Every screen gets a state:**

| State | Means | Becomes |
|---|---|---|
| **Working** | It really saves, reads, checks or sends | Needs, labelled Fact. They become Approved when you confirm that this version is the one the client approved |
| **Mocked** | Demo data, or a simulated result | What it *shows* is a Fact. What it must really *do* is asked at G0 |
| **Placeholder** | It does nothing | Asked at G0: in scope, later or out |

*Why:* a prototype looks finished where it isn't. Turning a simulated email or a "coming soon" page into a need would be invented scope (§14.1), which the client never agreed to.

**What the code can't show is asked, not guessed:** non-functional needs, real integrations, data migration, releases and the process.

**Technology-neutral output.** The planning layer and the breakdown never name a language, framework, database or file of the prototype (D19, R7). How the prototype does something goes to `downstream_notes` or to an AQ. It becomes a CON only when you state the constraint.

**The App Inventory** (`app-inventory.md`) lists every screen, its state, the files that show it, and the planning entries it became. It is the trace from the prototype to the plan, and it defines no IDs.

**The design.** The breakdown can't carry a design, but it can point to one. With `--figma`, `from-app` rebuilds each screen from the code in a Figma design file you name, and links each Feature (Basic: each Epic) to its screens in its optional `design` key, as `<Screen> — <where> — <Figma frame link>`. An Epic in the other processes lists the union of its Features' screens. `push` puts the links in the Description. The rebuilt screens are close to the prototype but not captured from it, so the functional team checks them before they become the design reference.

---

## 7. Stage 1 — Clarification standard

### 7.1 Project Brief content

| Field | Class | Why, or the condition that makes it required |
|---|---|---|
| Problem statement / purpose | **Mandatory** | Everything traces back to it |
| Objectives & outcomes (`OBJ`, 1–5) | **Mandatory** | The basis for traceability and priority |
| Primary users | **Mandatory** | Without them, items cannot express value |
| In-scope capabilities (headline) | **Mandatory** | Seeds the capability map |
| Explicit exclusions | **Mandatory** | Prevents scope creep. "None yet" must be stated explicitly |
| Success criteria (qualitative is fine) | **Mandatory** | Defines when the outcomes have been met |
| Known constraints | **Mandatory** ("none known" is allowed) | Constraints change the decomposition |
| Other stakeholders | Conditional | When anyone other than you is affected by the product or decides about it |
| Non-functional expectations | Conditional | When quality attributes shape scope: personal data, availability, performance, offline use, accessibility |
| Compliance / regulatory | Conditional | When regulated data or a regulated domain is involved |
| External dependencies & integrations | Conditional | When other systems or services are involved |
| Milestones / deadlines | Conditional | When timing or staged releases matter |
| Technical preferences | Conditional | Only *fixed* choices that constrain scope (platform, hosting, budget). Recorded as CON entries, not as design |
| Vision beyond the first release | Optional | Useful context, but not decomposed early |
| Personas, market notes, monetization | Optional | Background only |

### 7.2 Questioning rules [Recommended]

- Ask in rounds with **no fixed number of questions**: every Blocking and Material gap, grouped by topic and ordered by blocking impact. A Minor gap becomes a Q entry and is not asked.
- Where it helps, offer options or a proposed default, labelled as a *Recommendation* for you to accept or change.
- **Never fill a gap with an invented requirement.** Anything you have not confirmed stays a Recommendation or an Assumption.
- Stop asking once the exit criterion is met. Remaining unknowns become Q or ASM entries.

### 7.3 Exit criterion G1

G1 is met when both of these hold:

- You can state in one short paragraph *what* is being built, *for whom*, *why*, and *what is out*, and you can list the headline capabilities.
- Every Mandatory field is either filled or explicitly marked "unknown — non-blocking".

---

## 8. Stage 2 — Planning artifact standard

### 8.1 Artifact set

| Artifact | Purpose | Information owner (role, D15) | Necessary when | May be omitted or merged when |
|---|---|---|---|---|
| **Assessment Record** | Snapshot of what existed, the gaps, the route, and the trace index | Facilitator drafts; Product Owner confirms | Always | Never omitted, but it is short |
| **Project Brief** | Why, for whom, what, and what not | Product Owner | Always. It may be a section of an existing document | Merged into `project-plan.md` in Light |
| **Requirements & Scope Register** | Capability map, FR, NFR, BR and CON entries with priorities, acceptance measures and sources | Product Owner owns FR, BR and priority; Developer owns NFR targets and CON | Always | Becomes a section of `project-plan.md` in Light |
| **Roadmap** | Milestones, their sequence, and target outcomes or dates | Product Owner | There are several releases, deadlines, or staged delivery | Single release with no timing: one milestone, "Release 1", recorded in the Register |
| **Decision & RAID Log** | DEC, ASM, RSK, DEP, Q and AQ entries, plus change history | Shared; the Facilitator maintains it | Always | Becomes a section of `project-plan.md` in Light |
| **Work Breakdown** (Stage 3) | Process-specific Epics and Features (Basic: Epics) | Facilitator drafts; Product Owner approves | Always: it is the target | Never omitted |

**Relationships:** the Brief's objectives drive the Register's capabilities and requirements. The Roadmap's milestones are scoped by capabilities and requirements. The RAID Log is referenced from everywhere. The Work Breakdown traces to all of them (§4.1, §9.7).

**Physical packaging by profile** [Recommended]:

| Profile | Files |
|---|---|
| Light | `project-plan.md` (Assessment, Brief, Register, RAID, optional roadmap section) + `work-breakdown.yaml` + `work-breakdown.review.md` |
| Standard | `assessment.md`, `brief.md`, `requirements.md`, `roadmap.md` (if needed), `decisions-raid.md`, plus the breakdown files |
| Rigorous | As Standard. The Register may be split by capability area |

If your existing roadmap already *is* the Roadmap, it is referenced, not recreated. Planning files live in `docs/planning/` inside the project repository (Q1).

### 8.2 Suggested sections

| Artifact | Required sections | Optional or conditional sections |
|---|---|---|
| Project Brief | Purpose; Objectives (OBJ); Primary users; Scope in (headline); Scope out; Success criteria; Constraints | Stakeholders; Vision; Context |
| Requirements & Scope Register | Capability map (CAP: name, purpose, OBJ trace, boundary); FR table; priorities | NFR table (when relevant); Business rules; Constraints; Glossary (when domain terms are ambiguous) |
| Roadmap | Milestones (ID, name, outcome or exit condition, included CAP/FR scope) | Target dates; phase narrative |
| Decision & RAID Log | Decisions (ID, statement, date, rationale, supersedes); Assumptions; Open questions | Risks (with mitigation); Dependencies; Architectural questions (question, why it matters, affected CAP or items, needed-by milestone) |
| Assessment Record | The 6 points of §6.7 | Trace index (required when Stage 2 is skipped) |

Example rows from the Register:

| ID | Statement (what, not how) | CAP | Kind / quality attribute | Priority | Acceptance measure | Source | Traces to | Status |
|---|---|---|---|---|---|---|---|---|
| FR-007 | Users can export their data as a file | CAP-3 | Functional | Should | The export contains all of the user's records | SRC-1 §2 | OBJ-2 | Approved |
| NFR-002 | Personal data is protected at rest and in transit | Cross-cutting | Security | Must | Confirmed by a review checklist | Brief | OBJ-1 | Proposed |

### 8.3 Validation and maintenance rules

| Artifact | Validation | Maintenance |
|---|---|---|
| Assessment Record | All 6 points present; every source has an SRC ID | A snapshot. A new version is written only when Stage 0 is re-entered after a major change |
| Project Brief | Meets G1 (§7.3) | Changed only through a DEC entry; keeps a changelog |
| Register | IDs unique; every entry traces to an OBJ (or CON/DEC) and a source; every entry has a status; no duplicates | Statuses are updated in place. IDs are never reused. Dropped entries stay, marked *Dropped* |
| Roadmap | Milestones are outcomes; each milestone lists its scope | Dates can change freely (logged). Scope changes go through a DEC |
| Decision & RAID Log | Every Q has a needed-by point; every RSK has a mitigation; every AQ lists what it affects | Entries are closed with a resolution, never deleted |
| Work Breakdown | §11 | Only affected branches are regenerated; the version is bumped; superseded files are kept |

### 8.4 Requirements and scope conventions

- **Depth (D19)** [Recommended]. The Register records *product-level* needs: what users and stakeholders need from each capability, enough to define Features and their acceptance criteria. Technical requirements, and requirement-level work items, are written downstream by Tech Leads and Developers.
- **What versus how** [Recommended]. Requirements describe needs and outcomes. An implementation choice appears only as a constraint (CON), when it is genuinely imposed, or as an architectural question (AQ), when it is still open. Example:
  - FR: "Users can sign in with an account they already have."
  - CON, if imposed: "Use the organization's existing identity provider."
  - AQ, if undecided: "Which identity provider?"
- **Quality attributes.** Classify NFRs with a standard taxonomy, such as the ISO/IEC 25010 categories (performance efficiency, reliability, security, usability, maintainability, compatibility, portability …) [Established]. Include only the categories that are relevant.
- **Priority.** Use MoSCoW (Must / Should / Could / Won't-this-time) per capability and per requirement [Established technique].
- **Status lifecycle.** Proposed → Approved → (Changed | Deferred | Dropped). Only *Approved* entries, or entries explicitly covered by an ASM, feed Stage 3 as `ready` input.
- **Duplicates.** Merge them into one ID. The other ID remains as an alias pointing to the survivor.
- **Conflicts.** Record a Q that cites both sources. Block only the affected items.
- **Traceability.** Every FR and NFR traces to at least one OBJ (or to a CON or DEC, for imposed needs) and to at least one source.
- **Change impact.** When an entry changes, list every item that traces to it. The trace links make this a lookup.

### 8.5 Roadmaps versus work items

| Concept | What it is | What it is not | How it relates to work items |
|---|---|---|---|
| **Milestone** (MS) | A checkpoint defined by an outcome and/or a date | Work, an Epic, or a container of items | Items reference it (`milestone: MS-n`) |
| **Phase** | A period of time that groups milestones | A hierarchy level | Kept as narrative in the Roadmap |
| **Epic** | A large body of work that delivers a capability or outcome | A time box | It can span milestones, and its items can target different milestones |

Rules [Recommended]:

1. **Never map a phase or milestone to an Epic automatically.**
2. **The test:** "Does it reach a completion state by doing work?" Then it is a work item. "Is it a point at which we check that something is true?" Then it is a milestone.
3. A phase that *coincides* with exactly one capability area may produce an Epic, but only with an explicit note that explains the coincidence (example in §13.2).
4. The milestone is assigned on Features (Basic: Epics) and summarised upwards to Epics. How it becomes an iteration, tag or field in ADO is decided by the creation workflow.

### 8.6 Change handling

Every change is logged with one of three types:

| Type | Meaning | How it is recorded |
|---|---|---|
| **New decision** | Something not decided before | A new `DEC-n` |
| **Modification** | Changes an earlier decision | `DEC-m` *supersedes* `DEC-n`. The old entry stays visible, marked superseded |
| **Clarification** | Wording only, no change of meaning | Edited in place with a short note |

Rules [Recommended]:

- **Later updates** (D8): once the breakdown is approved, you or your team update it as you learn. Each update is one of the three types above, and only the affected items change.
- Approved choices are kept unless a contradiction or a material risk justifies reviewing them.
- Impact is found through the trace links, and only the affected branches are re-decomposed.
- Artifacts carry a short changelog (version, date, summary).
- A local change never triggers full regeneration.

### 8.7 Readiness criteria: Gate G2

| # | Criterion | Required level |
|---|---|---|
| 1 | Objectives stated with success criteria | Sufficient |
| 2 | Scope in/out and capability map | Decomposition-ready for every in-scope capability (D8) |
| 3 | Prioritized product-level needs (FRs) for every in-scope capability, enough to define Features and their acceptance criteria (D8, D19) | Decomposition-ready |
| 4 | Relevant NFRs identified, with a target or acceptance measure wherever they constrain in-scope work | Sufficient |
| 5 | Constraints and external dependencies known, or "none known" stated | Sufficient |
| 6 | Milestones defined as outcomes (when a roadmap applies) | Sufficient |
| 7 | No unresolved *Blocking* gaps in in-scope areas | Mandatory |
| 8 | Non-blocking unknowns recorded as ASM, Q or AQ entries | Mandatory |
| 9 | ADO process selected | Mandatory to *start Stage 3*, but not for G2 itself |

Possible outcomes:

- **Ready.**
- **Ready with documented assumptions.**
- **Partially ready.** Ready areas are fully described. The other areas are marked `needs-elaboration` or `blocked`, with the Q that holds them.
- **Not ready.**

---

## 9. Stage 3 — Process-aware decomposition standard

### 9.1 Universal principles

These principles are the same for all four processes. Only the levels and names change.

1. **Standardize the method, not the hierarchy.** The levels and type names come from the process.
2. **Stop at the portfolio levels** (D17). Agile, Scrum and CMMI: Epic → Feature. Basic: Epic. Delivery-level items and Tasks are created downstream.
3. **Slice Features by value, not by technical layer.** A Feature is a capability that a user or stakeholder can see working, not "Backend" or "Database" [Established agile practice].
4. **One level of abstraction per item.** A Feature is a *part* of its Epic's outcome, not a *step* in building it.
5. **Each item states what "done" means.** An Epic has an outcome and, optionally, a success measure. A Feature (in Basic, an Epic) has acceptance criteria at capability level.
6. **The hand-off test.** A `ready` Feature can be refined into delivery items by a Tech Lead or Developer using only the Feature and the planning IDs it references, without going back to product questions.
7. **Reference, don't duplicate.** Cross-cutting needs are referenced by ID (D11).
8. **Everything in scope is fully described** (D8). Every Epic and Feature found in the idea or the documents gets its full description, whichever milestone it targets. You or your team update it later as needed (§8.6).
9. **Uncertainty is explicit.** Every item carries `readiness` and `confidence`. Nothing that is blocked or low-confidence is presented as ready.
10. **Outcome phrasing in every process.** Epic and Feature titles name an outcome or capability, never an activity ("Recipe collection", not "Build recipe module"). This replaces D16.

**Feature quality criteria** [Recommended]. At this level they take the place of INVEST, which applies to delivery items. A good Feature is:

| Criterion | Meaning |
|---|---|
| **Valuable** | A user or stakeholder notices when it is released |
| **Bounded** | What is in and what is out are stated |
| **Verifiable** | Its acceptance criteria can be checked at capability level |
| **Milestone-sized** | It can be released within one milestone |
| **Explicit about dependencies** | Its dependencies are listed, and there are no cycles |
| **Design-free** | It contains no implementation choices, unless a CON imposes them |

**Procedure** [Recommended]:

1. Start from the capability map (CAP) and the objectives.
2. Form **Epics**. In Basic, one Epic is roughly one capability (D9, D18).
3. In Agile, Scrum and CMMI, form **Features**: releasable slices of capability within each Epic.
4. Describe every item fully (D8), using only the planning layer and the sources. Where information is missing, ask, or mark the item `needs-elaboration` with a Q. Never invent.
5. Apply the NFR patterns (D11): constraints, enabler Features and verification Features.
6. **Link** each item: parent, `traces_to`, `milestone`, `depends_on` and `constraints`.
7. **Validate** (§11), then present the breakdown at G3.

### 9.2 Hierarchies and excluded types

[Established: default built-in templates. Verify the exact types through MCP before creating anything.]

| Process | Produced by this standard | Created downstream by Tech Leads / Developers | Also in the template, but excluded (D13) |
|---|---|---|---|
| **Basic** | Epic | Issue → Task | none |
| **Agile** | Epic → Feature | User Story → Task | Bug, Issue (a tracking type, *not* Basic's Issue), test types |
| **Scrum** | Epic → Feature | Product Backlog Item → Task | Bug, Impediment, test types |
| **CMMI** | Epic → Feature | Requirement → Task | Bug, Change Request, Issue, Review, Risk, test types |

Hard rules:

- Only the Epic and Feature types appear in the output, and only Epics in Basic.
- Basic has no Feature level, and Basic Issues are never used as stand-in Features (D18).
- No delivery-level items (Issue, User Story, PBI, Requirement) and no Tasks (D17).
- Every Feature has an Epic parent (D10).
- RAID entries never become work items (D13, Q3).

**Note:** in the default templates, Epic and Feature serve the same purpose in Agile, Scrum and CMMI, so the output structure is the same for those three. The selected process is still recorded in the `process` key, for two reasons:

- It tells the downstream workflow which delivery-level type to create under each Feature.
- It changes the structure when the process is Basic.

The exact fields of Epic and Feature may differ by process. They are validated through MCP later.

### 9.3 Work-item type definitions

The rows are numbered by these eight attributes:

1. Purpose, scope and level of abstraction.
2. Required (R) and optional (O) information.
3. Allowed parents and children.
4. When to split or combine.
5. Completion criteria.
6. Dependencies and priority.
7. Traceability.
8. Quality checks, and when to elaborate further.

The size thresholds ("~8–10") are adjustable heuristics [Recommended], not rules.

#### Epic (all four processes)

| # | Agile / Scrum / CMMI | Basic (D9, D18) |
|---|---|---|
| 1 | A large body of work that delivers a business outcome or major capability. It spans several Features and possibly several milestones | A capability-sized body of work. It is the only level this standard produces in Basic, so it also carries the Feature-level information |
| 2 | **R:** title, outcome, scope boundary, `traces_to` (OBJ, CAP), priority. **O:** success measure, milestone span, risks | **R:** title, outcome, description, scope in/out, acceptance criteria, constraints, `traces_to` (OBJ, CAP, FR), priority, milestone, rank. **O:** success measure, tags for larger groupings, `downstream_notes` |
| 3 | Parent: none (top level). Children: Features | Parent: none. Children: none in this standard; Issues are created downstream |
| 4 | **Split** when it serves unrelated outcomes or has more than ~8–10 Features. **Combine** single-Feature Epics only when they share one outcome | **Split** when it covers two unrelated capabilities, spans milestones, or needs more than ~8 acceptance criteria. **Combine** when two Epics are halves of one capability |
| 5 | The outcome is achieved, and every child Feature is done or descoped | Its acceptance criteria are met. This is checked downstream as its Issues are delivered |
| 6 | Priority comes from the OBJ and CAP. Dependencies are recorded on its Features wherever possible | Priority, rank within the milestone, `depends_on` |
| 7 | Traces to at least one OBJ, to a CAP, and to sources | Traces to at least one OBJ, one CAP, its FR/NFR IDs, and sources |
| 8 | Clear outcome, and not a phase or milestone | It meets the Feature quality criteria (§9.1) |

#### Feature (Agile, Scrum, CMMI)

| # | Definition |
|---|---|
| 1 | A coherent capability that delivers value on its own, can be released, and completes within one milestone. **It is the unit handed off to Tech Leads and Developers for refinement** |
| 2 | **R:** title, description, scope in/out, acceptance criteria, constraints (NFR IDs), parent Epic, `traces_to` (CAP, FR), priority, milestone, rank. **O:** risks, `size_hint`, `open_questions`, `downstream_notes` |
| 3 | Parent: an Epic. Children: none in this standard. User Stories, PBIs or Requirements are created beneath it downstream |
| 4 | **Split** when it spans milestones, serves two distinct user goals, needs more than ~8 acceptance criteria, or has a `size_hint` of XL. **Combine** when it is really a single delivery item, or when two Features cannot be released separately |
| 5 | Its acceptance criteria are met and its constraints satisfied. Downstream, its delivery items are done |
| 6 | Priority (MoSCoW) comes from its FRs. It may depend on other Features, including ones in other Epics. It has a rank within its milestone |
| 7 | Traces to a CAP, to FR/NFR IDs, and to sources |
| 8 | It meets the Feature quality criteria, and it is `ready` only when it passes the hand-off test |

**Granularity guide for Features** [Recommended heuristic]:

- A Feature usually turns into roughly **3–10 delivery-level items** downstream.
- If you can imagine it as only one item, it is too small. "Add a recipe", for example, belongs inside "Recipe collection".
- If you expect more than about 15 items, it is too big.

**Acceptance criteria at Feature level** describe observable capability, not user-interface or technical detail:

| Feature level (this standard) | Delivery level (downstream, not written here) |
|---|---|
| "A user can add, edit and delete a recipe with a title, ingredients and ordered steps." | "Saving a recipe without a title shows a validation message." |
| "A user can find every saved recipe that contains a given ingredient." | "Search results are sorted by most recently cooked." |

**What happens beneath a Feature downstream.** This is not produced here. It is shown so that the semantic differences stay visible:

| Process | Delivery-level type created downstream | Character |
|---|---|---|
| Basic | Issue, under each Epic | General-purpose: feature slices, enablers and defects alike |
| Agile | User Story | Value from the user's point of view. Enabler stories are labelled as enablers |
| Scrum | Product Backlog Item | Any valuable entry in an ordered backlog, with a Definition of Done |
| CMMI | Requirement | Formal, verifiable "shall" statements. The Feature's `traces_to` gives Tech Leads the FR and NFR IDs to derive them from |

### 9.4 Decomposition by type of work

| Type of work | Pattern [Recommended] | Example |
|---|---|---|
| **User-facing capability** | Epics and Features by capability. Acceptance criteria describe the observable capability | The Feature "Recipe collection" |
| **Enabling (foundational)** | Normally part of the first Feature's scope, noted in its description, with the item itself created downstream. A dedicated enabler Feature only when the work is substantial and shared by several Features | "Deployable multi-tenant environment" (§13.3) |
| **Infrastructure / DevOps** | An enabler Feature only when the work is real and sizeable. A "Platform & operations" Epic only when it holds several such Features. Small setup work is left to downstream | none |
| **Security** | Security NFRs follow the Constraint pattern. Security *capabilities* (sign-in, roles, audit trail) are ordinary Features. A verification Feature is added for substantial reviews or penetration tests | NFR-3 listed in `constraints` on every Feature that handles clinic data |
| **Compliance** | Constraints (CON, BR) are referenced. The capabilities they require, such as consent capture or data export and erasure, become Features. Evidence needs become a verification Feature | none |
| **Reliability / observability** | Targets are constraints, often global. Backups and monitoring become enabler Features when they are substantial | none |
| **Other cross-cutting NFRs** (performance, accessibility, usability) | A constraint, often global. A verification Feature when measuring it needs dedicated work | "Load verification of the booking flow" |

**Anti-patterns:**

- An "NFR Epic" with nothing but copied statements.
- NFR text copied into many Features, instead of a reference to its ID.
- Features defined by technical layer, such as "Backend" or "Database".
- Features that are really a single delivery item.
- Features that prescribe an implementation, such as "Set up Kubernetes". These become an AQ plus an outcome-phrased enabler Feature.

### 9.5 When to stop decomposing

Stop when **any** of these applies:

- The item is a Feature (in Basic, an Epic) and is fully described (D8). This standard has no level below it.
- Further detail would be delivery-level: individual user steps, UI details, data fields, technical requirements. That belongs downstream.
- Further detail would need design or architectural decisions. Record an AQ instead.
- Further detail would be speculative, with no FR or source behind it.

**Warning signs** [Recommended heuristics]:

- An Epic with only 1 Feature, or with more than about 10.
- A Feature with more than about 8 acceptance criteria.
- A Feature that spans two milestones.
- A Feature you can only imagine as a single delivery item.
- More Features targeted at one milestone than it can plausibly hold. If so, recheck the scope or the milestone.

### 9.6 Prioritization and dependencies

| Attribute | Meaning | Where it is used |
|---|---|---|
| `priority` | Business or product value: Must / Should / Could / Won't | Every item. The default is inherited from the FR or CAP |
| `depends_on` | A technical or logical prerequisite: another draft ID, or an external `DEP-n` | Features (Basic: Epics). Dependencies may cross Epics |
| `rank` | The intended delivery order within a milestone | Features (Basic: Epics) |
| `milestone` | The target `MS-n` | Features (Basic: Epics), summarised upwards to Epics |
| `risk` | Risk level and RSK references. High-risk Features may be ranked earlier so you learn early | Optional |

Rules:

- **Parent–child order never implies sequence.**
- Dependencies are directed and must contain no cycles.
- A dependency that crosses Epics is recorded on the dependent Feature.
- How dependencies become ADO links is decided by the creation workflow.

### 9.7 Traceability

The chain runs **Objectives / Sources → Planning information → Process-specific backlog items**:

```text
OBJ-2 ──► CAP-3 ──► FR-007 ──► RCP-FT-004  (Agile / Scrum / CMMI)   |   RCP-EP-004  (Basic)
SRC-1 §2 ─────────────┘          ▲
NFR-002 ─────────────────────────┘   (Constraint: listed in the Feature's constraints)
```

**Mechanism** [Recommended]: each item lists `traces_to` (planning IDs), `sources` (SRC references) and `constraints` (NFR IDs). From these, the review view generates a coverage table:

| Planning ID | Priority | Covered by | Status |
|---|---|---|---|
| FR-007 | Should | RCP-FT-004 | Covered |
| FR-009 | Must | none | **Gap** |
| NFR-002 | Must | Constraint on 4 Features; verified by RCP-FT-011 | Covered |

Draft IDs (D6) are provisional. ADO assigns the real work-item IDs at creation, and the creation workflow writes them into `ado_id`. Downstream workflows can continue the chain below each Feature in whatever way suits them.

### 9.8 Structured output format

The format uses neutral logical keys and assumes no ADO field names or custom fields.

```yaml
work_breakdown:
  project: Recipe Keeper            # hypothetical
  key: RCP
  process: CMMI                     # Basic | Agile | Scrum | CMMI (mandatory, explicit)
  version: 0.2
  status: in-review                 # draft | in-review | approved | superseded
  rigor: Light
  planning_sources: [docs/planning/project-plan.md@v3]
  global_constraints: [NFR-1]       # D11: applies to every Feature
  items:
    - draft_id: RCP-EP-001
      type: Epic
      title: Organised home cooking
      parent: null
      outcome: Recipes are kept in one place and the week's meals are planned quickly.
      scope:
        in: [CAP-1, CAP-2]
        out: [nutrition tracking, grocery delivery]
      priority: Must
      traces_to: [OBJ-1, OBJ-2]
      sources: ["SRC-1"]
      readiness: ready
      confidence: high
      ado_id: null
    - draft_id: RCP-FT-001
      type: Feature
      title: Recipe collection
      parent: RCP-EP-001
      description: Users keep their own recipes and find them again by ingredient.
      scope:
        in:
          - add, edit and delete recipes
          - search recipes by ingredient
        out:
          - importing recipes from websites
      acceptance_criteria:
        - A user can add, edit and delete a recipe with a title, ingredients and ordered steps.
        - A user can find every saved recipe that contains a given ingredient.
      constraints: []               # NFR-1 already applies globally
      nature: user-facing           # user-facing | enabler | verification
      priority: Must
      rank: 1
      milestone: MS-1
      depends_on: []
      traces_to: [CAP-1, FR-1, FR-2]
      sources: ["SRC-1"]
      size_hint: M                  # optional S|M|L|XL; not an ADO estimate
      readiness: ready              # ready | needs-elaboration | blocked
      confidence: high              # high | medium | low
      open_questions: []
      downstream_notes: []          # e.g. story-level items found in source documents (scenario C)
      tags: []
      ado_id: null
```

In Basic, the same Feature-level keys sit on the Epic, and there are no Feature items (D18).

**Key classes:**

- **Core content:** `type`, `title`, `description` / `outcome`, `scope`, `acceptance_criteria`, `parent`.
- **Planning metadata:** `priority`, `rank`, `milestone`, `depends_on`, `constraints`, `traces_to`, `sources`, `nature`, `size_hint`, `readiness`, `confidence`, `open_questions`, `downstream_notes`, `design` (optional: Figma links, only in a plan from an external prototype), `tags`. Each of these may later map to an ADO field, tag, link or iteration, or stay planning-only. The creation workflow decides after validating the schema.
- **Header:** `process`, `version`, `status`, `rigor`, `planning_sources`, `global_constraints`.
- **Reserved:** `ado_id`, written only by the creation workflow.

**Review view** (`work-breakdown.review.md`), generated from the YAML and stamped with its version:

1. Summary counts by type and readiness.
2. Hierarchy tree.
3. Feature cards (Basic: Epic cards).
4. Traceability coverage.
5. Constraint matrix: NFRs × Features.
6. Dependency list.
7. Open questions and assumptions.
8. Validation report (§11.5).

---

## 10. Context schema

The schema lists what the standard needs to know, and where each item can come from.

| Information | Class | Derivable from documents? | Must you confirm it? |
|---|---|---|---|
| Project name and short key (e.g. `RCP`) | Universal | Name: yes. Key: proposed by Claude | Yes, the key |
| Purpose / problem | Universal | Often | When it comes from an old or unapproved document |
| Objectives | Universal | Often | When inferred |
| Primary users | Universal | Often | When inferred |
| Scope in / out | Universal | Partly; exclusions are rarely written down | Yes, the exclusions |
| Existing artifacts and their status | Universal | Inventory: yes. Approval status: rarely | Yes, which ones are approved |
| Constraints | Universal ("none known" is allowed) | Partly | Yes |
| **ADO process** | Universal for Stage 3 | **Never** | **Always, explicitly** |
| Milestones and the scope each one targets | Universal when a roadmap applies | Often, from the roadmap | Yes |
| Rigor profile | Universal (Claude proposes it) | Derived from §12 | Yes, at G0 |
| Stakeholders other than you | Conditional: others are involved | Partly | Yes |
| NFR targets | Conditional: the product is sensitive to quality attributes | Partly | Yes |
| Compliance obligations | Conditional: regulated data or domain | Rarely | Yes |
| Integrations / external dependencies | Conditional: external systems are involved | Often | Yes |
| Deadlines / release dates | Conditional: the work is time-bound | Often | Yes |
| Fixed technical constraints | Conditional: platform, hosting or budget is imposed | Often | Yes |
| Iteration length and capacity | Conditional: used to sanity-check how many Features one milestone can hold | No | Yes |
| *Basic:* tags for groupings larger than an Epic | Process-specific | No | Optional |

At the portfolio level (D17), Agile, Scrum and CMMI need no process-specific input beyond the selection itself. Process-specific detail, such as story format or the Definition of Done, belongs to the downstream workflows.

**Derivation rules** [Recommended]:

- Anything derived is labelled either a *Fact* (with its source) or an *Assumption*.
- The ADO process is never derived.
- Approval is never assumed from a document's tone or apparent completeness.

---

## 11. Validation framework

### 11.1 Gate checklists

**G0: Assessment**

- [ ] Scenario identified (A, B, C or D), or out-of-scope stated
- [ ] Every source inventoried with an SRC ID
- [ ] Statements classified (D4), with approved decisions evidenced
- [ ] Gaps listed with their severity, and contradictions listed
- [ ] Process selected, or "pending — Stage 3 blocked" stated
- [ ] Route and rigor profile proposed, with reasons
- [ ] You have reviewed the assessment

**G1: Clarity.** See §7.3.

**G2: Readiness.** See §8.7.

**G3: Breakdown.**

- [ ] Every check in §11.3 and §11.4 passes: no *Fail* results, and every *Warn* acknowledged
- [ ] The readiness counts are shown
- [ ] Blocked and low-confidence items are listed separately
- [ ] You approve

### 11.2 Readiness rubric for an existing roadmap (scenario B)

| Check | Passes when | Fails when |
|---|---|---|
| Purpose & objectives | Stated explicitly, or clearly inferable and then confirmed by you | Only features are listed, with no "why" |
| Scope boundary | Exclusions or an MVP cut are stated | Everything is "phase 2+", with no cut |
| Capability coverage | Phases list capabilities | Phases are only dates or vague themes |
| Capability depth | The needs of every in-scope capability are clear enough to define its Features and their acceptance criteria (D8) | Only capability names, for any phase |
| NFR awareness | Relevant concerns are named | None are named, although the project handles sensitive data, needs uptime, and so on |
| Consistency | No contradictions | Statements conflict across sections |
| Milestone semantics | Phases are defined by outcomes | Phases are named like work, e.g. "Build backend", and need reinterpretation |
| Currency | Reflects current intent | Contradicted by later decisions |

The rubric gives one of three results:

- **Sufficient:** go directly to Stage 3.
- **Gap-fill:** list the gaps, and run Stage 2 only for them.
- **Rework:** list the areas to rework.

### 11.3 Universal quality checks (breakdown)

| Check | Rule | Severity if violated |
|---|---|---|
| Completeness | Every in-scope capability has its Features (Basic: its Epic), each fully described (D8). Every Must FR is covered by a Feature, and every Must NFR by a D11 pattern | Fail for Must; Warn for Should or Could |
| Clarity | Titles name an outcome or capability, and a description is present | Warn |
| Granularity | The heuristics of §9.3 and §9.5 are respected | Warn |
| Duplicates | No two Features share an outcome, and no NFR text is copied across Features | Fail for duplicate items; Warn for copied text |
| Contradictions | No item contradicts an approved DEC or requirement | Fail |
| Acceptance criteria | Present on every `ready` Feature (Basic: Epic), written at capability level. Every Epic has an outcome | Fail for `ready` items |
| Hand-off sufficiency | Every `ready` Feature (Basic: Epic) has scope in/out, constraints (or reliance on `global_constraints`) and no blocking Q | Fail |
| Delivery-level detail | No delivery-level items, Tasks, UI-level criteria or technical requirements appear in the output (D17) | Fail for items; Warn for detail |
| Traceability | No orphans: every item traces to at least one planning ID, and every reference resolves | Fail |
| Dependencies | IDs are valid, there are no cycles, and dependencies across Epics are recorded | Fail for cycles or invalid IDs |
| Realistic scope | The number of Features per milestone is plausible, and no Feature spans two milestones | Warn |
| Milestone semantics | No item is a milestone in disguise | Fail |
| Invented scope | No item traces *only* to Recommendations that you have not approved | Fail |

### 11.4 Process-conformance checks

| Check | Basic | Agile | Scrum | CMMI |
|---|---|---|---|---|
| Allowed types | Epic | Epic, Feature | Epic, Feature | Epic, Feature |
| Parent of a Feature | n/a (no Features) | Epic | Epic | Epic |
| Forbidden in the output | Feature, Issue, Task | User Story, Task, Bug, Issue | Product Backlog Item, Task, Bug, Impediment | Requirement, Task, Bug, Change Request, Issue, Review, Risk |
| Type codes in draft IDs | `EP` | `EP`, `FT` | `EP`, `FT` | `EP`, `FT` |
| Skipped levels (D10) | n/a | Not allowed | Not allowed | Not allowed |

Checks common to all four:

- The `process` key is present and matches the selected process.
- Draft IDs are unique and well-formed.
- `ado_id` is null.
- Item text never refers to a Feature or Epic by another process's delivery-level names, e.g. calling a Feature a "Requirement" or a "User Story".

### 11.5 Item states and the validation report

**Readiness:**

| State | Meaning |
|---|---|
| `ready` | Fully described (D8), meets the Feature quality criteria, passes the hand-off test (§9.1), and has no blocking Q |
| `needs-elaboration` | Correct as far as it goes, but some required information is missing because the sources and your answers do not cover it yet. A Q records what is missing, so you or your team can complete it |
| `blocked` | Depends on an unresolved Blocking question or decision, which is listed by its Q ID |

**Confidence:**

| Level | Meaning |
|---|---|
| `high` | Based on approved information |
| `medium` | Rests partly on documented assumptions |
| `low` | Rests mainly on assumptions. A low-confidence item **cannot** be `ready` |

**Rule:** blocked and low-confidence items are never counted as ready, and they are listed separately in the review view.

**Report format:**

```text
Validation — RCP work breakdown v0.2 (process: CMMI)
PASS  Process conformance (types, parents, IDs; no delivery-level items)
PASS  Traceability: 5/5 items trace; 4/4 Must FRs covered; NFR-1 global constraint
WARN  Granularity: RCP-EP-002 has a single Feature (combine or justify)
FAIL  Hand-off sufficiency: RCP-FT-002 is marked ready but has no scope boundary
Ready 3 · Needs elaboration 1 · Blocked 1 (Q-3)
```

A script, `validate_breakdown.py`, automates the mechanical checks: schema, IDs, types and parents, cycles, orphans and coverage (§15, Q2). When it cannot run, Claude runs them by hand. The judgement checks, such as clarity, value slicing, hand-off sufficiency and realism, stay with the review.

---

## 12. Adaptive rules

### 12.1 Scaling dimensions

| Dimension | Signals |
|---|---|
| **Complexity** | Number of capabilities, user types and integrations, distributed parts, multi-tenancy |
| **Uncertainty** | New domain, unclear users, unproven technology, many open questions |
| **Artifact maturity** | The entry scenario and the §6.3 rubric scores |
| **Risk / regulation** | Personal, financial or health data, availability needs, compliance obligations |

### 12.2 Rigor profiles

| Aspect | **Light** | **Standard** | **Rigorous** |
|---|---|---|---|
| Typical project | Personal tool, up to ~5 capabilities, one release | Multi-release application with some integrations | Distributed or regulated system with many capabilities |
| Assessment | ½ page | 1 page | At most 2 pages |
| Artifacts | One `project-plan.md` | Separate files | Separate files; the Register is split by area |
| NFR depth | Only NFRs that change scope | The relevant categories, with acceptance measures | The full relevant taxonomy, with targets |
| Roadmap | Optional (a single milestone) | When there are several releases | Required |
| Depth (D8) | Everything in scope fully described | Everything in scope fully described | Everything in scope fully described. Where an open AQ or Q would make a Feature speculative, it is marked `needs-elaboration` instead |
| Checkpoints | G0 and G3 (G1/G2 merged in) | G0, G1 (when Stage 1 ran), G2, G3 | All gates, plus explicit sign-off on change impacts |
| Validation | Checklist | Checklist plus coverage table | Checklist, coverage table, and a dependency review |

**Selection rules** [Recommended]:

- The highest-scoring dimension sets the default profile.
- The profile can be **raised for one area**, e.g. a Light project with a Rigorous "payments" area.
- Choosing a profile *lower* than the risk/regulation dimension suggests requires an explicit DEC entry.

### 12.3 How uncertainty and existing artifacts change the depth

| Situation | Effect on the standard |
|---|---|
| High uncertainty | More questions in Stages 1 and 2, more `needs-elaboration` items where answers are not available yet, and more AQ entries handed downstream. An enabler Feature with a learning outcome only when the exploration is substantial |
| Mature artifacts (B or C) | Stages 1 and 2 shrink to gap-fill, the trace index replaces rewriting, and the assessment focuses on contradictions and currency |
| Partial decomposition (C) | Decomposition resumes at the deepest sound level, up to Feature level. Earlier levels are re-validated, not rebuilt. Delivery-level content goes into `downstream_notes` |
| Low risk and low complexity | Light profile, a single file, and checkpoints merged |

---

## 13. Worked examples

All four projects are **hypothetical**. They exist only to demonstrate the method. The examples are deliberately abbreviated, so "…" marks content left out. Stage 3 output is portfolio levels only (D17).

### 13.1 Example A: new small application, no plan (Basic)

**Input.** Your message: *"I want a small web app to keep track of my plants and remind me when to water them."*

**Stage 0: Assessment (Light)**

```markdown
## Assessment Record — Plant Care Reminder (v1)
1. State & artifacts: Scenario A. SRC-1 = initial message. No documents.
2. Reusable information: purpose; two headline capabilities (tracking, reminders). No decisions yet.
3. Missing: who the users are (Blocking for sharing scope); how reminders reach you (Blocking for
   the reminder capability); exclusions (Material); hosting constraints (Material).
4. Contradictions / risks: none. RSK-1: reminder delivery mechanism not chosen → AQ-1.
5. ADO process: pending → asked → Basic (DEC-1).
6. Route: 0 → 1 → 2 (Light, one docs/planning/project-plan.md) → 3. Rigor Light: one person,
   few capabilities, no regulated data.
```

**Stage 1: one round of questions**

1. Is it only for you, or for others in your household?
2. How should reminders reach you?
3. Must it work on a phone?
4. What is explicitly out? (e.g. identifying plants from photos)
5. Are there any deadline or hosting constraints?

Your answers produce the Brief:

- **Objectives:** OBJ-1 "Never miss a watering". OBJ-2 "Plant-care notes in one place".
- **Users:** you first; household members later.
- **Out of scope:** plant identification, a shop, a native mobile app.
- **Constraints and NFRs:** CON-1 free-tier hosting. NFR-1 usable in a phone browser.
- **Decisions:** reminders by email (DEC-2).

**Stage 2: Light, in `docs/planning/project-plan.md`**

| Capability | Product-level needs (D19) | Milestone |
|---|---|---|
| CAP-1 Plant catalogue | FR-1 add a plant (name, location, optional photo) · FR-2 edit/remove · FR-3 browse by location | MS-1 "I use it daily for my own plants" |
| CAP-2 Watering schedule & reminders | FR-4 watering interval per plant · FR-5 mark as watered · FR-6 daily email of plants due | MS-1 |
| CAP-3 Household sharing | FR-7 invite a member · FR-8 shared plant list | MS-2 "My household shares one list" |

- AQ-1 asks how emails are sent. It does not block the breakdown, because FR-6 is phrased as an outcome.
- ASM-1: one reminder email per day is enough.
- **G2 result:** ready with documented assumptions.

**Stage 3: Basic (Epics only, D18)**

```text
global_constraints: [NFR-1]  (usable in a phone browser)
PLT-EP-001 Plant catalogue                     Must   · MS-1 · rank 1 · ready
PLT-EP-002 Watering schedule and reminders     Must   · MS-1 · rank 2 · ready · depends_on PLT-EP-001
PLT-EP-003 Household sharing                   Should · MS-2 · rank 3 · ready · depends_on PLT-EP-001
```

```yaml
- draft_id: PLT-EP-002
  type: Epic
  title: Watering schedule and reminders
  parent: null
  outcome: The user never misses a watering.
  description: >
    Each plant has a watering interval. The user marks plants as watered
    and receives one daily email listing the plants that are due.
  scope:
    in:
      - watering interval per plant
      - marking a plant as watered
      - daily reminder email
    out:
      - push notifications (the native app is out of scope)
  acceptance_criteria:
    - Each plant can have its own watering interval.
    - Marking a plant as watered restarts its interval.
    - The user receives at most one email per day, listing every plant that is due or overdue.
  constraints: []                # NFR-1 applies globally
  priority: Must
  rank: 2
  milestone: MS-1
  depends_on: [PLT-EP-001]
  traces_to: [OBJ-1, CAP-2, FR-4, FR-5, FR-6]
  sources: ["SRC-1", "Brief"]
  readiness: ready
  confidence: medium             # rests on ASM-1 (once a day is enough)
  open_questions: []
  ado_id: null
```

**What this example shows:**

- In Basic, each Epic is one capability (D9) and carries the Feature-level content (D18).
- No Issues are created. You (or a collaborator) create them downstream, under each Epic.
- Foundational work (a deployable app and single-user sign-in) is noted in PLT-EP-001's description, not forced into an item of its own.
- The MS-2 Epic is fully described too, although it targets a later milestone (D8).
- The whole breakdown is 3 Epics.

### 13.2 Example B: existing Markdown roadmap, decomposed directly (Scrum)

**Input:** `roadmap.md` (SRC-1), which you confirm is approved. You selected Scrum at intake (DEC-1). The excerpt below is hypothetical:

```markdown
# Book Club Hub — Roadmap (approved)
Vision: make it easy for small book clubs to organise meetings and pick books.
Goals: 1) run a club without spreadsheets  2) more members join discussions  3) works well on phones
Users: organisers, members.   Out of scope: selling books, video calls.
Phase 1 — MVP "Run a club": create club; invite members by link; schedule meetings; propose and vote on next book
Phase 2 — Engagement: discussion threads per book (members post and reply; organiser can pin a post);
          reading progress (members mark chapters read; the club sees overall progress)
Phase 3 — Polish & performance: pages load in under 2 s on 4G; accessibility audit (WCAG 2.1 AA) before public launch
```

**Stage 0: assessment (excerpt)**

- Rubric:
  - Purpose: *Sufficient*.
  - Users: *Decomposition-ready*.
  - Scope: *Sufficient*, because exclusions are stated.
  - Capabilities of all three phases: *Decomposition-ready*.
  - NFRs: *Sufficient*.
- Gaps: Q-1 "How are tied votes resolved?" is Minor and affects one Feature.
- **Route:** 0 → 3. Stages 1 and 2 are skipped because the roadmap passes G1, and passes G2 for every in-scope capability, Phases 2 and 3 included. The rigor profile is Standard, because there are several releases.
- **Trace index:** the roadmap is referenced, not rewritten.

| ID | Source | Label |
|---|---|---|
| OBJ-1 … OBJ-3 | SRC-1 Goals 1–3 | Run a club without spreadsheets · More members join discussions · Works well on phones |
| CAP-1 … CAP-3 | SRC-1 Phase 1 | Club setup & membership · Meetings · Choosing the next book |
| FR-1 … FR-4 | SRC-1 Phase 1, items 1–4 | Create club · Invite by link · Schedule meetings · Propose & vote |
| CAP-4, FR-5, FR-6 | SRC-1 Phase 2 | Engagement: discussion threads, reading progress |
| NFR-1 · NFR-2 · NFR-3 | SRC-1 Goal 3 · Phase 3 · Phase 3 | Mobile browsers · WCAG 2.1 AA · Pages load in under 2 s on 4G |
| MS-1 · MS-2 · MS-3 | SRC-1 Phases 1–3 | A club completes its first meeting cycle · Members discuss books in the app · Quality bar verified |

**How the phases are treated** (§8.5):

| Roadmap phase | Becomes | Why |
|---|---|---|
| Phase 1 "Run a club" | **MS-1**. Its three capabilities become Features of BCH-EP-001 | A phase is a checkpoint. Its content is three capabilities |
| Phase 2 "Engagement" | **MS-2**. Its capability area *also* yields BCH-EP-002 | It coincides with exactly one capability area, so an Epic is allowed, with an explicit note (rule 3) |
| Phase 3 "Polish & performance" | **MS-3, not an Epic** | It names quality work, not a capability. NFR-1 to NFR-3 become global constraints *from the start* (D11). The audit and the speed check become one verification Feature, BCH-FT-006, targeted at MS-3 |

**Stage 3: Scrum (Epic → Feature)**

```text
global_constraints: [NFR-1 mobile browsers, NFR-2 WCAG 2.1 AA, NFR-3 pages load in under 2 s on 4G]
BCH-EP-001 Run a book club without spreadsheets                     (OBJ-1)
  BCH-FT-001 Club setup & membership                    MS-1 · rank 1 · ready
  BCH-FT-002 Meetings                                   MS-1 · rank 2 · ready · depends_on BCH-FT-001
  BCH-FT-003 Choosing the next book                     MS-1 · rank 3 · ready · confidence medium (Q-1)
  BCH-FT-006 Quality verification before public launch  MS-3 · verification (NFR-2, NFR-3) · ready
BCH-EP-002 Member engagement                                        (OBJ-2) · note: coincides with Phase 2
  BCH-FT-004 Discussion threads per book                MS-2 · rank 1 · ready · depends_on BCH-FT-001
  BCH-FT-005 Reading progress                           MS-2 · rank 2 · ready · depends_on BCH-FT-003
```

```yaml
- draft_id: BCH-FT-003
  type: Feature
  title: Choosing the next book
  parent: BCH-EP-001
  description: Members propose candidate books and vote; the organiser closes the vote.
  scope:
    in:
      - proposing candidate books
      - one vote per member per round
      - closing the vote and setting the next book
    out:
      - buying or linking to book shops (out of scope in SRC-1)
  acceptance_criteria:
    - Members can propose candidate books for the next meeting.
    - Each member can vote once per round, and the organiser can close the round.
    - Closing a round sets the winning book for the next meeting, applying the tie rule from Q-1.
  constraints: []                # NFR-1 to NFR-3 apply globally
  nature: user-facing
  priority: Must
  rank: 3
  milestone: MS-1
  depends_on: [BCH-FT-001]
  traces_to: [OBJ-1, CAP-3, FR-4]
  sources: ["SRC-1 Phase 1"]
  readiness: ready
  confidence: medium             # Q-1 is open but non-blocking
  open_questions: [Q-1]
  ado_id: null
```

**What this example shows:**

- Stages 1 and 2 are skipped, and the roadmap is kept intact behind a trace index.
- Phases become milestones. One phase legitimately coincides with an Epic, and that is noted.
- The quality phase becomes global constraints from day one, plus one verification Feature (D11).
- Every Feature is fully described, including those for MS-2 and MS-3 (D8).
- No PBIs are created. The Scrum team creates them downstream under each `ready` Feature.

### 13.3 Example C: complex project, partially decomposed, no ADO backlog (CMMI)

**Input.** Three documents:

- SRC-1 `vision.md`: approved.
- SRC-2 `epics-draft.md`: a draft that lists seven "Epics".
- SRC-3 `requirements-notes.md`: a draft with mixed needs, including 14 "The system shall …" statements.

The product is a multi-tenant appointment-scheduling platform for small clinics. You chose CMMI because you want formal traceability (DEC-1). The rigor profile is Rigorous, because of health-related personal data, multi-tenancy and payments.

**Stage 0: assessment of the existing decomposition**

| Item in the sources | Finding | Action |
|---|---|---|
| SRC-2 "Epic: Booking" | A sound capability. Of its three listed Features, one is Task-sized ("Create booking DB tables") | **Keep** → CSP-EP-001, with its two sound Features. The Task-sized one is referenced in `downstream_notes` for the Tech Lead |
| SRC-2 "Epic: Staff calendar" | Sound | **Keep** → CSP-EP-002 |
| SRC-2 "Epic: Notifications" | A capability, but reminder items also appear under Booking | **Keep** → CSP-EP-003. Move the reminder items here and merge the duplicates |
| SRC-2 "Epic: Payments" | Depends on two undecided points: are deposits in the MVP, and which provider? | **Keep as `blocked`** → CSP-EP-004 (Q-4). Not decomposed |
| SRC-2 "Epic: Beta launch" | A milestone, not work | **Reclassify** → MS-2 "Beta with three pilot clinics" |
| SRC-2 "Epic: Security" | A mix of NFR text and real capabilities | **Split** using D11. NFR-3 … NFR-6 become constraints. "Staff roles and permissions" becomes a Feature in EP-002. "Audit trail" (Capability) and "Security verification" (Verification) become Features in EP-005 |
| SRC-2 "Epic: Set up Kubernetes cluster" | A Task-level implementation choice that prescribes architecture | **Not an Epic.** Record AQ-2 (runtime and hosting), and replace it with the outcome-phrased enabler Feature "Deployable multi-tenant environment" |
| SRC-3, 14 "shall" statements | Requirement-level content, which is downstream work (D17) | **Not recreated as CMMI Requirements.** Product-level needs are extracted into the Register (D19). The original statements are referenced in each relevant Feature's `downstream_notes`, so the Tech Lead can reuse them |
| "Patients must log in securely" (three times: under Booking, Notifications and Security) | Duplicate | **Merge** → FR-12 (patient sign-in) + NFR-4 (authentication strength). Referenced, not copied |

**Other findings:**

- **Contradiction.** SRC-3 states "99.5 % availability", while SRC-1 says "always on". Recorded as Q-2, with ASM-2 (use 99.5 % until resolved). Neither statement was picked silently.
- **Architectural question.** AQ-1: which tenant isolation model? It does not block the breakdown, because NFR-3 ("each clinic's data is isolated") holds whatever model is chosen.
- **Open product question.** Q-5: may patients cancel bookings online, and until when? None of the sources says. It was asked in Stage 2 and is still unanswered at G3.
- **Route:** 0 → 2 → 3. Stage 2 is gap-fill only: Register IDs and deduplication, RAID entries, and the Roadmap (MS-1 internal alpha, MS-2 beta, MS-3 general availability). Stage 3 **resumes at Feature level** for the sound Epics.

**Stage 3: CMMI (Epic → Feature)**

```text
global_constraints: [NFR-1 availability 99.5 % (ASM-2), NFR-2 personal-data protection]
CSP-EP-001 Patient self-booking                                     (OBJ-1)
  CSP-FT-001 Find and book an appointment          MS-1 · ready · constraints NFR-3, NFR-4
  CSP-FT-002 Manage my bookings                    MS-2 · needs-elaboration (Q-5: online cancellation rules)
CSP-EP-002 Staff calendar                                           (OBJ-1)
  CSP-FT-003 Staff roles and permissions           MS-1 · ready · constraints NFR-5 · from the former "Security" Epic
  CSP-FT-004 Staff availability and schedules      MS-1 · ready
CSP-EP-003 Notifications                                            (OBJ-2)
  CSP-FT-005 Appointment reminders                 MS-1 · ready
CSP-EP-004 Deposits and payments                                    blocked (Q-4)
CSP-EP-005 Platform operations                                      (OBJ-3) · justified: holds real enabler work
  CSP-FT-006 Deployable multi-tenant environment   MS-1 · enabler · ready · constraints NFR-3
  CSP-FT-007 Audit trail                           MS-2 · enabler (Capability, NFR-6) · ready
  CSP-FT-008 Security verification before beta     MS-2 · verification (NFR-3 … NFR-6) · ready

Validation: Ready 11 · Needs elaboration 1 (CSP-FT-002, Q-5) · Blocked 1 (CSP-EP-004, Q-4)
```

```yaml
- draft_id: CSP-FT-006
  type: Feature
  title: Deployable multi-tenant environment
  parent: CSP-EP-005
  description: The platform runs as one deployment that serves many clinics, each isolated from the others.
  scope:
    in:
      - provisioning a new clinic without code changes
      - isolation of each clinic's data
    out:
      - the choice of runtime and hosting (AQ-2, architecture workflow)
  acceptance_criteria:
    - A new clinic can be provisioned without changing code.
    - No clinic can see or change another clinic's data.
  constraints: [NFR-3]
  nature: enabler
  priority: Must
  rank: 1
  milestone: MS-1
  depends_on: []
  traces_to: [OBJ-3, NFR-3]
  sources: ["SRC-2 Epic 7", "SRC-3 §4"]
  readiness: ready
  confidence: medium             # isolation model open (AQ-1); the criteria hold either way
  open_questions: [AQ-1, AQ-2]   # handed to the architecture workflow, not blocking
  downstream_notes:
    - "SRC-2 Epic 7 proposed Kubernetes. Recorded as AQ-2, not as a decision."
    - "SRC-3 §4, statements S-07 to S-09, describe tenant provisioning in 'shall' form."
  ado_id: null
```

**What this example shows:**

- Sound work is kept, and decomposition resumes at the deepest sound level.
- A milestone posing as an Epic is reclassified.
- The mixed "Security" Epic is split with all three NFR patterns.
- An item that prescribed the implementation becomes an AQ plus an outcome-phrased enabler Feature.
- Requirement-level statements are **not recreated**. They are passed downstream through `downstream_notes`.
- Duplicates are merged, and the contradiction is surfaced rather than resolved silently.
- The blocked Epic stays visible but is not presented as ready.
- Every Feature is fully described (D8). CSP-FT-002 is `needs-elaboration` only because a product question is still open (Q-5), not because of its milestone.

### 13.4 Side by side: one project under Basic, Agile, Scrum and CMMI

**Shared planning layer.** This part is identical in all four representations:

```text
OBJ-1 Keep all personal recipes in one place        OBJ-2 Plan the week's meals faster
CAP-1 Recipe collection : FR-1 add a recipe (title, ingredients, steps) · FR-2 search recipes by ingredient
CAP-2 Meal planning     : FR-3 plan a week of meals from saved recipes · FR-4 shopping list from a week plan
NFR-1 Usable on a phone-sized screen (global constraint)
MS-1 "Recipes in use" (CAP-1) · MS-2 "Weekly planning" (CAP-2)
```

**Basic: Epics only (D18)**

```text
RCP-EP-001 Recipe collection         MS-1 · fully described: scope, acceptance criteria, constraints
RCP-EP-002 Meal planning             MS-2 · fully described: scope, acceptance criteria, constraints
```

**Agile, Scrum and CMMI: Epic → Feature (identical at this level)**

```text
RCP-EP-001 Organised home cooking
  RCP-FT-001 Recipe collection       MS-1 · fully described: scope, acceptance criteria, constraints
  RCP-FT-002 Meal planning           MS-2 · fully described: scope, acceptance criteria, constraints
```

**Why the process still matters: what is created downstream.** Shown for orientation only; this standard does not produce these items.

| Process | Created beneath | By Tech Leads / Developers | How FR-2 might look there |
|---|---|---|---|
| Basic | each Epic | Issues | "Search recipes by ingredient" |
| Agile | each Feature | User Stories | "As a home cook, I want to search recipes by ingredient, so that I can cook with what I have" |
| Scrum | each Feature | Product Backlog Items | "Search recipes by ingredient", ordered in the backlog and done against the Definition of Done |
| CMMI | each Feature | Requirements | "The system shall return every saved recipe that contains a given ingredient." |

**What differs, and what does not**

| Aspect | Basic | Agile | Scrum | CMMI |
|---|---|---|---|---|
| Levels produced | 1 (Epic) | 2 (Epic, Feature) | 2 | 2 |
| Items produced | 2 Epics | 1 Epic · 2 Features | 1 · 2 | 1 · 2 |
| Where scope and acceptance criteria live | Epics | Features | Features | Features |
| Delivery-level type created downstream | Issue | User Story | Product Backlog Item | Requirement |
| **Unchanged in all four** | OBJ-1/2, CAP-1/2, FR-1…4, NFR-1, MS-1/2 and every trace link | ← | ← | ← |

**Notes:**

- As a result of D17, the structure of the output differs only between Basic and the other three. The process choice mainly shapes the downstream work.
- A draft ID belongs to one breakdown. `RCP-EP-001` means "Recipe collection" in Basic but "Organised home cooking" in the others. Switching between Agile, Scrum and CMMI keeps the same items and IDs; switching to or from Basic produces a new breakdown version (§5.3).

---

## 14. Failure modes and trade-offs

### 14.1 Failure modes

| Failure mode | Symptom | Prevention built into the standard | Detection |
|---|---|---|---|
| **Overdocumentation** | Many files with little value for decisions; existing plans rewritten to fit templates | Rigor profiles, logical versus physical artifacts (D3), reuse by reference, the trace index, "fill only material gaps" | Route review at G0; page budget per profile |
| **False completeness** | Everything marked ready; assumptions hidden | Status labels (D4), readiness and confidence states, blocked items listed separately | §11.3: a `ready` item needs criteria and no blocking Q; low confidence can never be `ready` |
| **Misclassified milestones** | Epics such as "Beta launch" or "Phase 2" | The milestone-versus-work test (§8.5) | Milestone-semantics check (Fail) |
| **Oversized items** | Epics with 20 Features; Features that span milestones | Split criteria (§9.3) | Granularity warnings |
| **Fragmented items** | Features that are really a single delivery item; splits by technical layer | The Feature granularity guide (§9.3) and value slicing | Single-child and granularity warnings |
| **Features too thin to hand off** | Tech Leads have to come back with product questions before they can create delivery items | The hand-off test (§9.1), and the full description of every Feature (D8) | Hand-off sufficiency check (Fail) |
| **Delivery-level detail creeping in** | User stories, "shall" statements, UI details or Tasks in the output | D17, stop rules (§9.5), Feature-level acceptance criteria (§9.3) | Delivery-level detail check; forbidden types (§11.4) |
| **Detail lost from source documents** | Story- or requirement-level content in existing documents is discarded | `downstream_notes` (§6.5 rule 6) | The G0 inventory shows where each such source item is referenced |
| **Duplicated cross-cutting requirements** | The same security text in 15 Features; a catch-all "Security Epic" | The NFR patterns and `global_constraints` (D11) | Copied-text check; coverage table and constraint matrix |
| **Process mismatch** | "Requirement" or "User Story" items in the output, Features in Basic, Basic Issues used as Features, a silent CMMI default | Explicit process selection (§6.6), D17, D18, the conformance rules (§9.2) | Process-conformance checks (Fail) |
| **Lack of traceability** | Nobody can tell why an item exists | `traces_to` and `sources` are mandatory | Orphan check |
| **Stale later-milestone Features** | Features for later milestones fall out of date as earlier milestones teach you things | Change handling (§8.6): you or your team update them, and only the affected items change | Validation (§11) runs again after each update |
| **Invented requirements** | Claude fills gaps with plausible features | The *Recommendation* label, plus your confirmation | "Invented scope" check (§11.3) |
| **YAML / review-view drift** | The YAML changes after the review view was generated, or someone edits the view by hand | The review view is generated only (D5, Q2) | The stamp shows a YAML that changed after the view was generated. A hand edit of the view is not detected: the next render replaces it |
| **Draft IDs mistaken for ADO IDs** | Draft IDs used as if they were real work-item IDs | Non-numeric, prefixed IDs (D6) and the `ado_id` key | ID format check |
| **Stale sources treated as truth** | An old roadmap overrides newer decisions | The currency check (§11.2) and statement classification | The contradictions list at G0 |

### 14.2 Trade-offs accepted

| Trade-off | Chosen | Cost accepted |
|---|---|---|
| Portfolio-only output versus full upper backlog | Portfolio only (D17) | Less upfront visibility of delivery scope. Agile, Scrum and CMMI outputs look the same at this level |
| Rigor versus speed | Profiles (D14) | Choosing a profile is a judgement call, confirmed at G0 |
| Neutral model versus direct decomposition | Direct (D2) | Switching to or from Basic requires a Stage 3 re-run |
| YAML plus Markdown versus Markdown only | YAML plus a generated view (D5) | Two files, and a render step (Q2) |
| Flat versus hierarchical IDs | Flat (D6) | An ID does not reveal its parent; the tree view does |
| Full description versus rolling wave | Everything in scope fully described (D8) | Features for later milestones may need updating. Stages 1 and 2 ask more questions up front |
| Strict levels versus flexibility | No skipped levels (D10) | Occasional single-Feature Epics |
| No estimates versus early sizing | `size_hint` only (D12) | No capacity forecast at initialization |
| Product-level Register versus none | Product level (D19) | A light Register still needs maintaining, but traceability survives |

---

## 15. Plugin boundaries

The Plotwork plugin implements this method as Claude Code skills. Whatever a skill does, these limits hold:

- Only `push` calls Azure DevOps. The other skills never call an ADO tool, not even to read.
- No skill creates delivery-level items (Issue, User Story, PBI, Requirement) or Tasks (D17), and RAID entries are never exported as work items (D13).
- No skill decides architecture. Open "how" questions become AQ entries.
- Claude never marks a gate as passed without you (§5.4).
- A project whose ADO backlog already holds work items is out of scope (§5.2).
- Only `from-app` and `from-app-update` call Figma, and only when you pass `--figma` and reply "yes figma". They add a new page to the one design file you named, through the one server confirmed as Figma's, and never create a file or change an existing page.

---

## 16. Changing the standard

A change to this standard follows its own change handling (§8.6):

1. **Record it.** A new rule is a new decision, with the next free ID. A change to a rule is a modification: the new decision supersedes the old one, which stays listed. A change of wording only is a clarification.
2. **Publish a new version,** and add a row to §0.
3. **Keep section numbers and IDs stable.** Never renumber a section and never reuse a decision ID. The plugin's files cite them (for example "§8.5" or "D17"), and so do the planning files Plotwork has already written for its users.
4. **Keep the plugin in step.** The plugin's runtime files restate these rules for Claude, so change them with the rule.

Creating the work items in Azure DevOps (`/plotwork:push`), and the delivery-level items and Tasks that Tech Leads and Developers create afterwards, are outside this standard (§4.3).
