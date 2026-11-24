# Decomposition patterns — Plotwork planning standard

<!-- Reference for Claude, for Stage 3. Condensed from §9.1–§9.7 of the standard.
     Read it together with the selected process's section in processes.md. -->

## 1. Principles

1. **Stop at the portfolio levels** (D17): Epic → Feature, or just Epics in Basic. Everything below them is created downstream.
2. **Slice by value, not by technical layer.** A Feature is a capability that someone notices working, never "Backend" or "Database".
3. **One level of abstraction per item.** A Feature is a *part* of its Epic's outcome, not a *step* in building it.
4. **Say what "done" means.** An Epic has an outcome. A Feature (in Basic, an Epic) has acceptance criteria at capability level.
5. **Pass the hand-off test.** A `ready` Feature lets a Tech Lead create delivery items from it and the IDs it references alone, without going back to product questions.
6. **Reference, don't duplicate.** Cite NFRs and sources by ID.
7. **Describe everything in scope fully** (D8), whatever milestone it targets. Missing information becomes a Q, never an invention.
8. **Name outcomes, not activities** ("Recipe collection", not "Build the recipe module").

## 2. Procedure

1. Start from the capability map (CAP) and the objectives (OBJ).
2. **Form Epics:** large bodies of work, each with a clear outcome. In Basic, one Epic is one capability.
3. **Form Features** (Agile, Scrum, CMMI): releasable slices of capability within each Epic, each finishing within one milestone.
4. **Describe each item fully:** description, scope in/out, acceptance criteria, constraints, priority, milestone, rank, traces.
5. **Apply the NFR patterns** (§5 below).
6. **Link** each item: `parent`, `depends_on`, `traces_to`, `constraints`.
7. **Validate**, render the review view, and present it at G3.

## 3. Feature quality criteria

| Criterion | The Feature … |
|---|---|
| Valuable | delivers something a user or stakeholder notices when it ships |
| Bounded | states what is in scope and what is out |
| Verifiable | has acceptance criteria that can be checked at capability level |
| Milestone-sized | can be released within one milestone |
| Explicit about dependencies | lists its prerequisites, with no cycles |
| Design-free | contains no implementation choice, unless a CON imposes it |

**Granularity.** A good Feature usually turns into roughly **3–10 delivery items** downstream.

- If you can imagine it as only one item, it is too small. "Add a recipe", for example, belongs inside "Recipe collection".
- If you expect more than about 15 items, it is too big.

**Acceptance criteria level:**

| Write this (capability level) | Not this (delivery level, written downstream) |
|---|---|
| "A user can add, edit and delete a recipe with a title, ingredients and ordered steps." | "Saving a recipe without a title shows a validation message." |
| "A user can find every saved recipe that contains a given ingredient." | "Search results are sorted by most recently cooked." |

## 4. Placing each kind of work

| Kind of work | Pattern |
|---|---|
| **User-facing capability** | Epics and Features by capability. Acceptance criteria describe the observable capability |
| **Foundational work** (a deployable skeleton, sign-in for a single-user app) | Normally part of the first Feature's scope, noted in its description, with the item created downstream. Make it its own enabler Feature only when the work is substantial and several Features share it |
| **Infrastructure / DevOps** | An enabler Feature only when the work is real and sizeable. A "Platform & operations" Epic only when it holds several such Features |
| **Security** | Security NFRs are constraints. Security *capabilities* (sign-in, roles, audit trail) are ordinary Features. Add a verification Feature for a substantial review or penetration test |
| **Compliance** | Constraints (CON, BR) are referenced. The capabilities they require (consent capture, data export or erasure) become Features. Evidence needs become a verification Feature |
| **Reliability / observability** | Targets are constraints, often global. Backups and monitoring become enabler Features when they are substantial |
| **Performance, accessibility, usability** | A constraint, often global. Add a verification Feature when measuring it needs dedicated work |
| **Exploration under high uncertainty** | Record an AQ for downstream. Make it an enabler Feature with a learning outcome only when the exploration is substantial |

## 5. NFR patterns (D11)

Classify each NFR with the three tests below. An NFR can match more than one.

| Pattern | Test | What to create |
|---|---|---|
| **Constraint** | It limits *how well*, or *under which conditions*, Features must work | Nothing new. Put it in `global_constraints` when it applies to everything, otherwise in the `constraints` of the Features it affects |
| **Capability** | Meeting it means building something that would not otherwise exist | An enabler Feature (Basic: an enabler Epic) with `nature: enabler`, tracing to the NFR |
| **Verification** | Proving it takes dedicated effort beyond normal delivery work | A verification Feature with `nature: verification`, tracing to the NFR. If the effort is small, an acceptance criterion on the Feature concerned is enough |

Put enabler and verification Features under the Epic they affect most. Never create an Epic just to hold them. When a roadmap has a quality phase ("Polish & performance", "Launch readiness"), the phase becomes a milestone, and its verification Features sit under existing capability Epics with `milestone` set to it.

**Scope of a verification Feature.** Define it by reference, so that it stays right when Features are added: "every user-facing flow delivered by MS-n" for an NFR in `global_constraints`, or the Feature IDs whose `constraints` carry the NFR. Do not list flows by hand. Group the checks that share a milestone into one verification Feature. A single measurement is an acceptance criterion, not a Feature.

## 6. Anti-patterns

| Anti-pattern | Do this instead |
|---|---|
| An "NFR Epic" holding only copied statements | Constraints, plus real enabler or verification Features |
| The same NFR text in many Features | Reference the NFR ID |
| "Backend", "Database", "API" Features | Slice by capability |
| A Feature that is a single delivery item | Merge it into the capability it belongs to |
| "Set up Kubernetes" or any other prescribed solution | Record an AQ, plus an outcome-phrased enabler Feature ("Deployable multi-tenant environment") |
| A phase or milestone as an Epic ("Beta launch", "Phase 2") | A milestone in the Roadmap. Items reference it with `milestone` |
| One Epic per phase under outcome-style names: each Epic's Features all target that phase's milestone | Capability Epics whose Features may target several milestones. M16 warns about this shape |
| User stories or "shall" statements inside a Feature | Put them in `downstream_notes`, or leave them out |

## 7. When to stop

Stop when **any** of these applies:

- The item is a Feature (in Basic, an Epic) and is fully described. There is no lower level in this standard.
- More detail would be delivery-level: user steps, screens, fields, technical requirements.
- More detail would need a design or architecture decision. Record an AQ instead.
- More detail would be speculative, with no FR or source behind it.

**Warning signs:**

- an Epic with 1 Feature, or more than about 10;
- a Feature with more than about 8 acceptance criteria;
- a Feature that spans two milestones;
- more Features in one milestone than it can plausibly hold.

## 8. Priority, order and dependencies

| Key | Meaning |
|---|---|
| `priority` | Business value: Must, Should, Could or Won't. The default is inherited from the FR or CAP |
| `rank` | The intended delivery order within the milestone |
| `milestone` | The target `MS-n`. Epics summarise their Features' milestones |
| `depends_on` | Prerequisites: draft IDs, or an external `DEP-n`. They may cross Epics, and they must not form a cycle |
| `risk` | Optional. A high-risk Feature may be ranked earlier, so the team learns early |

Parent–child order never implies sequence. A dependency that crosses Epics is recorded on the dependent Feature.

## 9. Traceability

Each item lists:

- `traces_to`: the planning IDs it comes from (OBJ, CAP, FR, NFR, BR, CON, DEC);
- `sources`: SRC references with a section;
- `constraints`: the NFR IDs it must respect.

The review view uses these to build the coverage tables. A Must FR or NFR that nothing covers is a gap, and a gap fails validation.
