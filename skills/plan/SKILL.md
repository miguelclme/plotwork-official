---
name: plan
description: Plans a software project into a reviewed, Azure DevOps-ready work breakdown of Epics and Features for the Basic, Agile, Scrum or CMMI process, following the Plotwork planning standard. Use it whenever someone wants to plan a new software project or app idea, structure or break down an existing roadmap or project plan, turn planning documents or a draft list of Epics or Features into a backlog, prepare work for Azure DevOps before any work items exist, or grow a plotwork prototype into a full plan, even if they never mention the standard. Also use it when someone asks to turn an idea or a roadmap into user stories, PBIs, requirements, issues or tasks for Azure DevOps. Those come later from the team, so this skill explains why and plans the Epics and Features instead. Do not use it when the project is already under development, when only a small prototype is wanted (use prototype), or when the task is to create or update work items in ADO (use push).
---

# Plan a software project

Turn an idea, a roadmap or partial planning documents into a reviewed plan and a work breakdown of **Epics and Features**. The result is ready for `/plotwork:push` to create in Azure DevOps.

**You write every file. The user answers questions and decides at two review points.** The point of the standard is to save the user time, so:

- batch your questions;
- propose answers the user can accept with "ok";
- never hand the user a template to fill in.

## Scope

**In scope:** assessing what exists, clarifying the idea, filling planning gaps, producing the Epic/Feature breakdown, validating it, and growing a prototype into a full plan.

**Out of scope.** Each of these belongs to a different workflow, so stop, or hand it on:

- **Azure DevOps itself.** Do not call any ADO tool, not even to read, and do not create work items. `/plotwork:push` does that from the approved YAML.
- **Delivery-level items and Tasks** (Issue, User Story, Product Backlog Item, Requirement). Tech Leads and Developers create them later, because they are technical (D17). If the user asks for them, explain this and offer the Epics and Features instead.
- **A project already under development** (something is built, or its ADO backlog has work items). It is out of scope for now: say so, and stop. A plotwork prototype is the one exception (see *Growing a prototype*).
- **Architecture.** Open "how" questions become AQ entries, handed downstream.
- **Custom, inherited or modified ADO processes.**

## Files

The shared files are in the plugin's `shared/` folder: `${CLAUDE_PLUGIN_ROOT}/shared/`, which is `../../shared/` from this skill's folder. Call it `<shared>`. It holds `steps/`, `references/`, `templates/`, `scripts/` and `examples/`.

| What | Where |
|---|---|
| Templates and their conventions | `<shared>/templates/`. Read `<shared>/templates/README.md` once, before writing the first file |
| Output | `docs/planning/` in the user's project (create it). If the working folder is clearly not the project, ask once where to save |
| The user's existing documents | Leave them where they are. Reference them by section; never rewrite them |

Remove the templates' `<!-- -->` guidance comments from the files you fill in.

## Before you start: what is already in `docs/planning/`

- **Nothing:** plan from scratch, as below.
- **A `work-breakdown.yaml` with `kind: prototype`:** grow it into a full plan. Follow *Growing a prototype* below.
- **A `work-breakdown.yaml` without `kind`:** a full plan already exists. To change it, use `/plotwork:update <changes-file>`. Say so, and stop.

## The flow

```text
Stage 0  Assess what exists ───────────────► G0  user reviews     [always; can be approved in advance]
Stage 1  Clarify the idea                                          [only if needed]
Stage 2  Fill planning gaps                                        [only if needed]
Stage 3  Epics & Features, validated ──────► G3  user reviews     [always]
```

Aim for two touchpoints with the user:

1. **G0:** one message with the assessment and every question you need answered.
2. **G3:** one message with the finished breakdown.

For the Light profile, G1 and G2 are folded into G3. For Standard and Rigorous, report G1 (when Stage 1 ran) and G2 together with the breakdown, unless one of them fails. In that case, stop and ask.

### Stage 0 — Assess (always)

Follow `<shared>/steps/assess.md`, with these parts of its own:

- **Step 7: choose the rigor profile and the route:**

  | Profile | Typical signals | Planning files |
  |---|---|---|
  | Light | Up to ~5 capabilities, one release, no sensitive data | `project-plan.md` |
  | Standard | Several releases or some integrations | `assessment.md`, `brief.md`, `requirements.md`, `decisions-raid.md`, plus `roadmap.md` when there are several releases |
  | Rigorous | Many capabilities, distributed or multi-tenant, or personal, financial or health data, or compliance needs | As Standard; the Register may be split by area |

  The highest-risk signal wins. A single area can be raised to a stricter profile.
- **Step 8:** the Assessment Record is `assessment.md`, or section 1 of `project-plan.md` for Light.

### Stage 1 — Clarify (only when G1 is not met)

- `<shared>/templates/brief.md` marks each field mandatory, conditional or optional, and explains why.
- Usually the G0 questions are enough. Ask a second round only for what still blocks.
- **Never fill a gap with an invented requirement.** A proposal the user has not confirmed stays a `[Recommendation]` or becomes an ASM.
- **Exit:** G1 in `<shared>/references/validation-checklists.md`.

### Stage 2 — Fill planning gaps (only for areas that fail G2)

- **Register.** Write or complete it at *product level* only (D19): what users need from each capability. Technical requirements are for downstream.
- **Roadmap.** Write one only when there are several releases or deadlines. A milestone is a checkpoint, never an Epic.
- **RAID Log.** Record decisions, assumptions, questions and AQs. The ADO process is always a DEC.
- **Everything in scope must end up fully described** (D8). Ask about later phases now rather than leaving them thin.
- **Give each NFR its D11 pattern now:** Constraint, Capability or Verification.
- **Exit:** G2 in `<shared>/references/validation-checklists.md`.

### Stage 3 — Work breakdown (always; needs the process)

1. Follow `<shared>/steps/breakdown.md`.
2. Follow `<shared>/steps/check.md`: validate and render, get the independent review, send the G3 message, and act on approval.

## Growing a prototype

A prototype made by `/plotwork:prototype` is the starting point, never something to replace. The direction is always prototype → plan, never plan → prototype.

1. **Keep a copy.** Copy `docs/planning/` to `docs/planning/.prototype/`, replacing any older copy. It is the record of the prototype as it was.
2. **Stage 0.** Record `prototype-plan.md` and the prototype's `work-breakdown.yaml` as sources. Their decisions, assumptions and answers carry over: do not ask again what they already settle. The ADO process is already a DEC. The prototype's own work does not make the project "under development", and its items may already be in ADO; do not ask about it. Ask only about the deferred capabilities in the *Later* list, and about anything new the user brings.
3. **Stages 1–2.** Choose the rigor profile from the whole product, then move every entry of `prototype-plan.md` into that profile's planning files, **with its ID unchanged**. The *Later* capabilities become in scope: change their status from Deferred, add their needs, and give them milestones after `MS-1`. When nothing is left in `prototype-plan.md`, delete it, so that no ID is defined twice (M6).
4. **Stage 3.** Keep every prototype item, its draft ID and its `ado_id`. Extend items where needed, and add new ones with the next free draft IDs. Remove the `kind: prototype` line. Set `version` to the next major version (an approved 1.0 becomes 2.0), with `status: in-review`.
5. **Changelogs.** Record the growth as a new DEC ("prototype grown into a full plan") and add a changelog row to every file you changed.
6. **Check** with `<shared>/steps/check.md`. If the prototype was pushed, the validator gives a WARN on M12 (some items have an ADO ID, the new ones don't). That is expected: in the G3 message, say that `/plotwork:push` creates only the new items.

## Updating an existing breakdown

When the user brings changes to a breakdown that already exists, in a message or in a file, follow the plugin's `update` skill (`/plotwork:update <file>`, in `../update/SKILL.md`). In short:

1. Record each change as a new decision, a modification or a clarification (§8.6).
2. Change only the affected items, and keep their IDs.
3. Bump the version, re-validate and re-render.
4. Propose a G3 result for the new version.

## Writing rules

Follow `<shared>/steps/writing-rules.md`.

## Reference map

| Read | When |
|---|---|
| `<shared>/steps/` | `assess.md` at Stage 0, `breakdown.md` and `check.md` at Stage 3, `writing-rules.md` throughout |
| `<shared>/templates/README.md` | Before writing the first file |
| `<shared>/references/processes.md` | Stage 0 (the process question) and Stage 3 (the selected process's section) |
| `<shared>/references/decomposition-patterns.md` | Stage 3 |
| `<shared>/references/validation-checklists.md` | At every gate. Its *Independent review* section says how to call the reviewer agent before G3 |
| `<shared>/examples/` | To see finished results: `plant-care` (Basic, Light, new idea), `book-club` (Scrum, Standard, existing roadmap) and `tool-share` (Agile prototype). The `demo` skill presents them |
| `<shared>/references/standard.md` | Only to settle a doubt about a rule. It is the full approved standard, so it is long |
