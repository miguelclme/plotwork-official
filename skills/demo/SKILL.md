---
name: demo
description: Shows a finished example of what the Plotwork plugin produces, so a user can see the result before planning a real project. Use it when someone asks for a demo, an example or sample output of the planning plugin, or asks what the plan skill creates, or runs /plotwork:demo with an example ID such as plant-care, book-club or tool-share. It only reads and presents the example; it never plans the user's own project.
argument-hint: <example_id>
---

# Show a planning example

Example to show: **$ARGUMENTS**. If that is empty, list the examples and ask which one to show.

The examples live in the plugin's `shared/` folder: `${CLAUDE_PLUGIN_ROOT}/shared/examples/`, which is `../../shared/examples/` from this skill's folder. Call that folder `<examples>`, and the `shared/` folder `<shared>`.

**This skill only reads.** Write nothing into the user's project unless the user asks for a copy (step 5). Never call an Azure DevOps tool.

## Steps

1. **Read `<examples>/README.md`.** It lists the example IDs.
   - **No argument, or an ID that is not listed:** reply with the list (ID, scenario, process, the one-line summary), plus the command to run, `/plotwork:demo <example_id>`. Then stop.
2. **Read the example.** Read `<examples>/<id>/README.md`, then the files it lists under `<examples>/<id>/docs/`. Take every fact you present from these files. Never invent a step or a result the files do not show.
3. **Validate it live.** Run the validator on the example's breakdown. It only reads:

   ```bash
   python "<shared>/scripts/validate_breakdown.py" "<examples>/<id>/docs/planning/work-breakdown.yaml" --planning-dir "<examples>/<id>/docs/planning"
   ```

   If Python is not available, say so and skip this step.
4. **Present the example** in one message of about 60 lines at most, in this order:
   1. **The request:** what the user asked, the scenario, the ADO process and the rigor profile.
   2. **How the skill handled it** (`plan`, or `prototype` for a prototype example): the stages it ran or skipped, what it asked at G0 (or why G0 was approved in advance), and where it stopped for the user.
   3. **The result:** a table of the Epics, and their Features unless the process is Basic, with ID, title, milestone and priority. Use `work-breakdown.yaml` as the source.
   4. **The files:** one line each, with its path, so the user can open it. Point to `work-breakdown.review.md` for the full detail.
   5. **Validation:** the result from step 3, in one line.
   6. **What to notice:** the 2–4 points from the example's README.
   7. **Try it for real:** run `/plotwork:plan` (or `/plotwork:prototype` for a small first version) with an idea or a roadmap in their own project. Changes later go through `/plotwork:update <file>`, and `/plotwork:push --project "<name>"` creates the approved items in Azure DevOps.
5. **On request only,** copy `<examples>/<id>/docs/` to `plotwork-demo/<id>/docs/` in the user's current folder, so they can browse or edit it. If that folder already exists, ask before overwriting. Then say where the copy is.
