# Step: validate, review and send for approval (G3)

<!-- Shared by the plan, prototype, from-app, from-app-update and update skills. Paths are relative to the plugin's shared/ folder
     (${CLAUDE_PLUGIN_ROOT}/shared/), written <shared> in the commands. The calling skill says what its
     reviewer call and its G3 message add. -->

1. **Validate and render the review view** (see *Scripts* below). Fix every FAIL you caused yourself, then re-run. FAILs that need the user's decision go into the G3 message.
2. **Get an independent review.** A second model, the plugin's `breakdown-reviewer` agent, judges the review checks R1–R14, so that the user is not the only check on your work. Follow *Independent review* in `references/validation-checklists.md`: call the reviewer, fix what it finds, re-validate, and run a second round when round 1 had FAILs.
3. **Send the G3 message**, then stop and wait:
   - the path to the review view;
   - the counts: ready, needs elaboration, blocked;
   - the *Independent review* section: the reviewer's verdict, what you fixed, the WARNs you kept and why;
   - what needs the user: FAILs, WARNs to acknowledge, open questions and the reviewer's ASKs (each with a proposed answer, one per numbered item), assumptions and proposed priorities. Each assumption (ASM) you list gets one plain sentence on what confirming it, or dropping it, changes. Every question you list has a proposed answer, including the ones that can wait for the team's refinement;
   - your proposed G3 result.
4. **On approval:**
   - set `status: approved` and bump `version` (the update skill has already bumped it, so it does not bump again);
   - add changelog entries;
   - re-render the review view;
   - tell the user that the YAML is ready for `/plotwork:push --project "<ADO project>"`, which creates the items in Azure DevOps.

## Scripts

Both scripts are in the plugin's `shared/scripts/` folder. They need Python 3 and nothing else; if PyYAML is installed, they use it. Run them from the user's project folder:

```bash
python "<shared>/scripts/validate_breakdown.py" docs/planning/work-breakdown.yaml --planning-dir docs/planning
python "<shared>/scripts/render_review.py" docs/planning/work-breakdown.yaml --planning-dir docs/planning
```

- **`validate_breakdown.py`** runs the mechanical checks M1–M17 and prints the report. It exits with code 1 when anything FAILs. Use `--max-features-per-milestone N` when the user gave a capacity. M17 runs only for a prototype (`kind: prototype`).
- **`render_review.py`** writes `work-breakdown.review.md` next to the YAML, with the validation report at the end. It stamps the view with the YAML's version and hash, so validation can tell when the view is stale.
- **YAML syntax:** without PyYAML, the scripts read the subset the template uses. That means block mappings and lists, `[a, b]` lists, quoted strings and `>` / `|` blocks. Keep to it: no anchors, and no plain values that run over several lines.
- **Fallback (Q2):** if Python is missing, or a script fails for a reason you cannot fix, run the same checks by hand from `references/validation-checklists.md`. Then write the view from `templates/work-breakdown.review.md`, using its "rendered manually" banner. Tell the user you did this.
