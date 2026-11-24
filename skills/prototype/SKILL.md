---
name: prototype
description: Plans a prototype of a software project as a small, reviewed Azure DevOps-ready breakdown of Epics and Features (one milestone), for the Basic, Agile, Scrum or CMMI process, following the Plotwork planning standard. It proposes the smallest set of capabilities that proves what the user wants proven, lists everything else for later, and writes one short prototype plan. Use it when someone wants a prototype, an MVP to try out, a proof of concept, a spike-sized first version or "just the first slice" of an idea or roadmap, or runs /plotwork:prototype. The result can be pushed with push, and grown into a full plan later with plan. Do not use it when a plotwork breakdown already exists (use update or plan), when the project is already under development, or to create work items in ADO (use push).
---

# Plan a prototype

Turn an idea, a roadmap or existing documents into a reviewed plan for a **prototype**: the smallest set of Epics and Features that proves what the user wants proven. Everything else goes on a *Later* list. The result is the same `work-breakdown.yaml` as a full plan, marked `kind: prototype`, so `/plotwork:push` can create it in Azure DevOps and `/plotwork:plan` can later grow it into a full plan.

This skill stands on its own. It does not call the `plan` skill and does not need it to have run.

**You write every file. The user answers questions and decides at two review points.** So:

- batch your questions;
- propose answers the user can accept with "ok";
- never hand the user a template to fill in.

The plan skill's scope rules apply here too: never call an Azure DevOps tool, not even to read; never write User Stories, PBIs, Requirements, Issues or Tasks (if the user asks for them, explain that the team writes them later, and offer the Epics and Features); a project already under development is out of scope; open "how" questions become AQ entries; custom ADO processes are out of scope.

## Files

The shared files are in the plugin's `shared/` folder: `${CLAUDE_PLUGIN_ROOT}/shared/`, which is `../../shared/` from this skill's folder. Call it `<shared>`. It holds `steps/`, `references/`, `templates/`, `scripts/` and `examples/`.

| What | Where |
|---|---|
| Templates and their conventions | `<shared>/templates/`. Read `<shared>/templates/README.md` once, before writing the first file. The prototype plan is `<shared>/templates/prototype-plan.md` |
| Output | `docs/planning/prototype-plan.md` and `docs/planning/work-breakdown.yaml` in the user's project (create the folder). If the working folder is clearly not the project, ask once where to save |
| The user's existing documents | Leave them where they are. Reference them by section; never rewrite them |

Remove the templates' `<!-- -->` guidance comments from the files you fill in.

## Before you start: what is already in `docs/planning/`

The direction is always prototype → plan, never plan → prototype.

- **Nothing:** plan the prototype, as below.
- **A `work-breakdown.yaml` without `kind: prototype`:** a full plan already exists, and it already covers more than a prototype would. To change it, use `/plotwork:update <changes-file>`. Say so, and stop.
- **A `work-breakdown.yaml` with `kind: prototype`:** a prototype already exists. To change it, use `/plotwork:update <changes-file>`; to grow it into a full plan, use `/plotwork:plan`. Say so, and stop.

## The flow

```text
Stage 0  Assess, and propose the prototype scope ──► G0  user reviews     [always; can be approved in advance]
         Write prototype-plan.md
Stage 3  Epics & Features, validated ──────────────► G3  user reviews     [always]
```

### Stage 0 — Assess and propose the scope (always)

Follow `<shared>/steps/assess.md`, with these parts of its own:

- **Questions:** as step 9 says, with no fixed number. Cover what the assessment leaves open of:
  - what the prototype must prove;
  - who will try it;
  - what is explicitly out;
  - any data or compliance limits.

  The ADO process is always asked, when the user has not named it, and never proposed.
- **Step 7: propose the prototype scope, in the same G0 message.** Propose the smallest set of Epics and Features that proves what the user wants proven, and list every capability you are leaving for later, one line each. The user accepts with "ok" or edits.
  - **The user's priorities win.** Everything the user marked Must goes in; never drop one. Mark your own suggestions "(proposed)".
  - **Size:** one milestone, `MS-1 Prototype`, and no fixed number of Epics or Features. Every Epic and Feature is needed to prove what the prototype must prove, or is one of the user's Musts; everything else goes on the *Later* list. A bigger product can need a bigger prototype.
  - **Rigor:** record `Light`, or `Rigorous` when the prototype handles personal, financial or health data or has compliance needs. Either way, the planning stays in the one prototype plan file; the data limits become NFR or CON entries.
- **Step 8:** the Assessment Record is section 1 of `prototype-plan.md`.

### Write `prototype-plan.md` (after G0)

Write it from `<shared>/templates/prototype-plan.md`, from the user's G0 answers. It holds:

- the assessment;
- what the prototype must prove, who tries it, and how you'll know it worked;
- the capabilities in the prototype, with their needs at product level (D19);
- **Later:** every deferred capability, one line each, with the status Deferred;
- decisions, assumptions and questions. The ADO process is always a DEC.

**Never fill a gap with an invented requirement.** A proposal the user has not confirmed stays a `[Recommendation]` or becomes an ASM. Ask a second round only for what still blocks.

### Stage 3 — Work breakdown (always; needs the process)

1. Follow `<shared>/steps/breakdown.md`, with these differences:
   - add `kind: prototype` to `work_breakdown`, right after `key`;
   - only the prototype's capabilities become items, and they are fully described (D8). The deferred ones stay on the *Later* list and never become items;
   - every item targets `MS-1`.
2. Follow `<shared>/steps/check.md`. The validator's M17 checks the prototype's shape: one milestone and the *Later* list. When you call the reviewer, say that the breakdown is a prototype: it then also checks that everything in it is needed to prove the point, and that every deferred capability is on the *Later* list.
3. **The G3 message** also lists the *Later* capabilities, so the user sees what was left out.
4. **On approval:** the YAML is ready for `/plotwork:push --project "<ADO project>"`. Say that `/plotwork:plan` can grow the prototype into a full plan later, keeping its IDs.

## Writing rules

Follow `<shared>/steps/writing-rules.md`.

## Reference map

| Read | When |
|---|---|
| `<shared>/steps/` | `assess.md` at Stage 0, `breakdown.md` and `check.md` at Stage 3, `writing-rules.md` throughout |
| `<shared>/templates/README.md` | Before writing the first file |
| `<shared>/references/processes.md` | Stage 0 (the process question) and Stage 3 (the selected process's section) |
| `<shared>/references/decomposition-patterns.md` | Stage 3 |
| `<shared>/references/validation-checklists.md` | At every gate |
| `<shared>/examples/tool-share/` | A finished prototype (Agile) |
| `<shared>/references/standard.md` | Only to settle a doubt about a rule |
