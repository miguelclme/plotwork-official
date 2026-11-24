# Templates — Plotwork planning standard

These templates implement §6–§9 of the [standard](../references/standard.md).

**Claude fills them in, not you.** They are the fixed format Claude writes into, so every project gets the same files and sections. Claude saves the filled files in the project's `docs/planning/` folder (Q1).

## Who does what

| Step | Claude (Facilitator, D15) | You (Product Owner) |
|---|---|---|
| Stage 0 | Reads your idea or documents and writes the Assessment Record | Confirm the route, and choose the ADO process (G0) |
| Stages 1–2 | Asks short rounds of questions, then writes the Brief, Register, Roadmap and Decision & RAID Log from your answers | Answer the questions |
| Stage 3 | Writes `work-breakdown.yaml`, generates the review view, and runs validation | Read the review view, then approve or correct it (G3) |
| Later updates | Applies each change to the files, keeps the IDs, and re-validates | Say what changed, in plain words |

You never need to open a template. You can still edit a filled file by hand if you prefer. Claude then re-validates it and records the change.

## Which files Claude uses

| Rigor profile (§12) | Planning files | Work breakdown |
|---|---|---|
| **Light** | `project-plan.md` only | `work-breakdown.yaml`, plus the generated `work-breakdown.review.md` |
| **Standard** | `assessment.md`, `brief.md`, `requirements.md`, `decisions-raid.md`. Add `roadmap.md` when there are several releases, deadlines or staged delivery | Same |
| **Rigorous** | As Standard. `requirements.md` may be split by capability area (`requirements-<area>.md`) | Same |
| **Prototype** (`/plotwork:prototype`) | `prototype-plan.md` only | Same, with `kind: prototype` |
| **From an external prototype** (`/plotwork:from-app`, changed with `/plotwork:from-app-update`) | The chosen profile's files, plus `app-inventory.md` and `app-files.json` (the file fingerprints, written by a script; JSON, so the validation script never reads it) | Same |

Existing documents are referenced, never recreated (§6.5). If your roadmap already *is* the Roadmap, Claude skips `roadmap.md` and references the original from the Assessment Record's trace index.

## Files in this folder

| File | Artifact | Stage | Standard |
|---|---|---|---|
| `assessment.md` | Assessment Record | 0 | §6 |
| `brief.md` | Project Brief | 1 | §7 |
| `requirements.md` | Requirements & Scope Register | 2 | §8.2–§8.4 |
| `roadmap.md` | Roadmap | 2 | §8.5 |
| `decisions-raid.md` | Decision & RAID Log | 0–3 | §8.2, §8.6 |
| `project-plan.md` | All of the above in one file (Light) | 0–2 | §8.1 |
| `prototype-plan.md` | The prototype's plan in one file, with its *Later* list | 0–2 | §8.1 |
| `app-inventory.md` | App Inventory: the screens of an external prototype, what each really does, the planning entries it became, and its Figma frames. Defines no IDs. Its presence marks a plan made from an external prototype. Its *Figma* column records which version each frame was rebuilt from, and marks a frame that is out of date as stale; a header row points to `app-files.json` | 0 | §6.9, D20 |
| `work-breakdown.yaml` | Work Breakdown, the canonical Stage 3 output | 3 | §9.8 |
| `work-breakdown.schema.json` | JSON Schema for the Work Breakdown | 3 | §9.8, §11.4 |
| `work-breakdown.review.md` | Layout of the generated review view | 3 | §9.8, Q2 |

## Conventions

**Placeholders.** `<…>` marks what Claude replaces with project content. `<!-- … -->` comments are instructions for Claude, and Claude removes them from the filled files.

**Required and optional sections.** Every heading is marked *(required)*, *(conditional: when …)* or *(optional)*. Claude never deletes a required section. When there is nothing for it yet, Claude writes "None known" or "Unknown — non-blocking (Q-n)". Conditional and optional sections that don't apply are left out.

**Identifiers (§4.2).** Use plain numbers (`FR-1`, `FR-2`, …). Never reuse or renumber an ID. Dropped entries stay in place, marked *Dropped*. Define each ID once, as the first cell of a table row: the validation script reads planning IDs, priorities and statuses from those tables.

| Prefix | Meaning | Lives in |
|---|---|---|
| `SRC` | Source document or conversation | Assessment Record |
| `OBJ` | Objective | Project Brief |
| `CAP` | Capability | Register |
| `FR` / `NFR` | Functional / non-functional requirement (product level, D19) | Register |
| `BR` | Business rule | Register |
| `CON` | Constraint, an imposed "how" | Register |
| `MS` | Milestone | Roadmap (or the Brief, when there is no roadmap) |
| `DEC` / `ASM` / `RSK` / `DEP` / `Q` / `AQ` | Decision / assumption / risk / external dependency / open question / architectural question | Decision & RAID Log |

Draft work-item IDs follow D6: `<KEY>-EP-001` for Epics and `<KEY>-FT-001` for Features. They are never numeric-only, so they cannot be mistaken for ADO IDs.

**Status labels (D4).** In the Assessment Record and the Brief, end each material statement with one label:

| Label | Use when |
|---|---|
| `[Fact · SRC-n §x]` | A source actually says it, but it is not yet approved. For an external prototype, cite the file: `[Fact · SRC-1 <path>]`. Claude's summaries and inferences, and things nobody mentioned, are never Facts: use Recommendation, Assumption or Open |
| `[Decision · DEC-n]` | You approved it, and it is recorded in the Log |
| `[Assumption · ASM-n]` | It is accepted as true for now |
| `[Recommendation]` | Claude proposed it, and you have not accepted it yet |
| `[Open · Q-n]` | It is unanswered |

The Register uses a **Status** column for the lifecycle instead: Proposed → Approved → Changed, Deferred or Dropped (§8.4). Only Approved entries, or entries covered by an ASM, feed Stage 3.

**Sources.** Cite sections; don't copy their text: `SRC-2 §3.1`.

**Gates.** Claude proposes a gate result (*pass*, *pass with assumptions*, *fail*). Only you decide it. Each template has a small gate table for this.

**Changelog.** Every file ends with a changelog, and every change bumps the version. Each change has one of three types (§8.6):

- **New decision.**
- **Modification:** DEC-m supersedes DEC-n.
- **Clarification:** wording only.

## Related reference files

- [`../references/processes.md`](../references/processes.md): what each ADO process means here. It covers what Stage 3 produces, what is created downstream, and what must never appear in the output.
- [`../references/validation-checklists.md`](../references/validation-checklists.md): the checklists for gates G0–G3, the roadmap readiness rubric, the G3 mechanical and review checks, and the report format.
- [`../references/standard.md`](../references/standard.md): the full standard. The § numbers in these templates point to its sections.
