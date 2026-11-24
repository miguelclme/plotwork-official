---
name: push
description: Creates the Epics and Features of an approved plotwork work breakdown (docs/planning/work-breakdown.yaml, a full plan or a prototype) as work items in an Azure DevOps project, through a connected Azure DevOps MCP server. It checks the project, the process and the breakdown, shows a preview, and writes nothing until the user confirms; then it creates the items, links them, writes the new ADO IDs into the YAML and verifies the result. Use it when someone wants to push, export, upload, sync or create their approved plotwork breakdown in Azure DevOps, or runs /plotwork:push. Do not use it to plan or change a breakdown (use plan, prototype or update), or to create user stories, PBIs, requirements, issues or tasks.
argument-hint: --project "<ADO project>" [--file <path>] [--area "<area path>"[=<Epics>]]... [--mcp <server>] [--help]
---

# Push a work breakdown to Azure DevOps

Arguments: **$ARGUMENTS**

This is the only plotwork skill that calls Azure DevOps. **Nothing is written to ADO, or to the YAML, before the user says a plain yes to the preview.** It creates only Epics and Features; the team writes the delivery-level items later.

The shared files are in the plugin's `shared/` folder: `${CLAUDE_PLUGIN_ROOT}/shared/`, which is `../../shared/` from this skill's folder. Call it `<shared>`.

## Arguments

Read the arguments first, before looking for any Azure DevOps tool:

1. **`--help` or `-h`:** print the usage below as it is, and stop. Call no tool, read and write nothing, and don't ask for a project, even when other flags are given too.
2. **An unknown flag:** anything other than `--project`, `--file`, `--area`, `--mcp` and `--help` (or `-h`), for example `--org`. Say which flag is unknown, and print the usage.
3. **`--project "<name>"`: required.** The Azure DevOps project to create the items in. If it is missing, ask for it. Never pick a project yourself, never take one from an earlier run, a file or memory, and never let a tool's project prompt choose it.
4. **`--file <path>`:** optional. The default is `docs/planning/work-breakdown.yaml`.
5. **`--area "<area path>"[=<Epics>]`:** optional, once per area. Check it against the YAML, as *Area paths* says. Read the YAML for this; if it can't be read, say so.
6. **`--mcp <server>`:** optional. The Azure DevOps MCP server to use, by its name as `claude mcp list` shows it (such as `azure-devops`). Needed only when more than one Azure DevOps server is connected (see *Finding the Azure DevOps tools*). An `--mcp` with no name, or given more than once, is a problem. Whether the server exists is checked later, when looking for the tools.

If 2 to 6 find any problem, report every one together, and stop. No Azure DevOps tool is called, and nothing is written.

The usage:

```text
/plotwork:push --project "<ADO project>" [--file <path>] [--area "<area path>"[=<Epics>]]... [--mcp <server>] [--help]

  --project  required. The Azure DevOps project to create the items in.
  --file     the breakdown to push. Default: docs/planning/work-breakdown.yaml
  --area     the area path for a set of Epics. Each Epic's Features go with it.
             <Epics> are Epic numbers and ranges, such as 1-12,20 (3 is <KEY>-EP-003).
             Without <Epics>: every Epic not given another area.
             Repeat it for each area. Without --area: the project's root area.
  --mcp      the Azure DevOps MCP server to use, as `claude mcp list` names it.
             Needed only when more than one is connected.
  --help     show this and stop. -h does the same.

Nothing is written until you say yes to a preview. At the preview you can
also change areas instead, for example: 13-19 → Mobile
Every item the push creates is tagged plotwork-pushed.

Examples:
  /plotwork:push --project "Shop"
  /plotwork:push --project "Shop" --area Web
  /plotwork:push --project "Shop" --area Web=1-12,20 --area Mobile=13-19 --area Platform
  /plotwork:push --project "Home Lab" --mcp ado-personal
```

## Area paths

Every Epic goes to one area path, and **its Features always go with it**: a Feature never gets an area of its own. Without `--area`, every item goes to the project's root area (the project name), as before.

**Reading `--area`:**
- `--area <path>=<Epics>` puts those Epics in `<path>`. `<Epics>` is what follows the last `=`: Epic numbers and ranges, separated by commas, such as `1-12,20`. A number is the number in the Epic's draft ID, without the zeros: with the key `BCH`, `3` is `BCH-EP-003` and `1000` is `BCH-EP-1000`. A full Epic ID (`BCH-EP-003`) is accepted too. A range covers the Epics that exist in it: draft IDs are never reused, so gaps are normal.
- `--area <path>` with no `=` puts every Epic not listed in another `--area` in `<path>`. Only one `--area` may have no Epics.
- Quotes may go around the path or around the whole value: `--area "Book Club\Web"=1-3` and `--area "Book Club\Web=1-3"` are the same.
- **The path:** `/` becomes `\`. A path that doesn't start with the project name (ignoring case) gets `<project>\` in front: `Web` becomes `Shop\Web`. The project name alone is the root area.
- Basic has only Epics. The rules are the same.

**Stop, list every problem found, and write nothing,** when:
- an ID is a Feature (`-FT-`). Say: "Features go with their Epic: give the Epic's number";
- a single number or ID is not an Epic in the YAML;
- an Epic is in more than one `--area`;
- more than one `--area` has no Epics;
- an `--area` has an empty path, or an `=` with no Epics after it.

**Epics already in ADO.** An Epic that already exists (it has an `ado_id`, or step 5 adopts it) keeps the area it has in ADO, and its new Features go there too, whatever `--area` says. Step 5 reads that area, and the preview warns when it differs from the one asked for. Never move it.

**At the preview,** the user can also change areas in the reply, with the same rules (step 6).

## Finding the Azure DevOps tools

Any Azure DevOps MCP server will do, whatever it is called. Never assume a server name. Look at the connected tools, load deferred ones if needed, and find one that does each of these operations:

| Operation | Tool names to look for (Microsoft's Azure DevOps MCP server, newer · older versions) |
|---|---|
| List projects | ends in `core_list_projects` |
| Read a work-item type and its fields | ends in `wit_work_item` (action `get_type`) · `wit_get_work_item_type` |
| Run a WIQL query | ends in `wit_query` (action `wiql`) · `wit_query_by_wiql`, `wit_get_query_results_by_id` |
| Read work items | ends in `wit_work_item` (actions `get`, `get_batch`) · `wit_get_work_item`, `wit_get_work_items_batch_by_ids` |
| Create a work item | ends in `wit_work_item_write` (action `create`) · `wit_create_work_item` |
| Link two work items | ends in `wit_work_item_link_write` (action `link`) · `wit_work_items_link` |
| List a project's teams (optional) | ends in `core_list_project_teams` |
| Read a team's area paths (optional) | ends in `work` (action `get_team_settings`) |

Other servers may name them differently: match on what the tool does, from its description and parameters. A tool's server is the `<server>` in its name, `mcp__<server>__<tool>`. An Azure DevOps server is one that has a tool to create work items.

**Which server:**
- **`--mcp` given:** use only that server's tools (the name matches ignoring case). If no connected Azure DevOps server has that name, say so, list the Azure DevOps servers found, and stop.
- **No `--mcp`, one Azure DevOps server:** use it.
- **No `--mcp`, more than one:** stop before calling any Azure DevOps tool. Do not ask which one, and do not pick one. List the servers found, and give one ready-to-copy command per server: the user's command with every other flag unchanged and `--mcp <server>` added, such as `/plotwork:push --project "Home Lab" --mcp ado-personal`. Say that nothing was written.
- **None:** say that an Azure DevOps MCP server is needed (for example Microsoft's, `@azure-devops/mcp`), and stop.

If the chosen server lacks one of the required operations, say which, and stop. Without the two optional tools, step 4 skips its team check.

Pass the project name explicitly in every call that takes one.

## Steps

1. **Check the project exists.** List the projects (filtered by the name) and find an exact match for `--project`. If there is none, show the closest names, and stop.
2. **Check the breakdown.** Read the YAML, then run, from the user's project folder:

   ```bash
   python "<shared>/scripts/validate_breakdown.py" <file> --planning-dir <the YAML's folder>
   ```

   Stop, and point to `/plotwork:plan`, `/plotwork:prototype` or `/plotwork:update`, when:
   - `status` is not `approved`;
   - the validator reports any FAIL;
   - M13 is not PASS (the review page is missing or out of date: re-render it with `render_review.py`, and get it approved).

   A WARN on M12 (some items have an ADO ID) is fine: an earlier push stopped halfway, or a prototype grew into a plan. Without Python, run the checks by hand from `<shared>/references/validation-checklists.md`, and say so.
3. **Check the process.** The project must use the YAML's `process`. Read these work-item types in the project:

   | YAML process | Must exist | Must not exist |
   |---|---|---|
   | Basic | Epic, Issue | Feature |
   | Agile | Epic, Feature, User Story | |
   | Scrum | Epic, Feature, Product Backlog Item | |
   | CMMI | Epic, Feature, Requirement | |

   If they don't match, say which process the project seems to use, and stop. Keep the field lists of Epic and Feature: steps 6 and 7 need them.
4. **Check the areas.** Skip this step when every Epic goes to the root area.
   - **Each area exists.** For each distinct area other than the root, run one WIQL query with `top: 1`, doubling any `'` in the names:

     ```sql
     SELECT [System.Id] FROM WorkItems
     WHERE [System.TeamProject] = '<project>' AND [System.AreaPath] UNDER '<area>'
     ```

     An error saying the area path does not exist (`TF51011`) means the area is missing. Any other error: say so, and stop.
   - **Which team's backlog** (a warning, never a stop). Items under an area that no team owns are on no team's backlog. List the project's teams. If there are 20 or fewer, read each team's settings and keep its `areaPaths` (`value`, `includeChildren`). An area belongs to a team when it is one of them, or is under one that includes children. With more than 20 teams, or without these tools, skip this, and say so in the preview.
   - If any area is missing, list each one, with the closest of the teams' area paths when there are any, and stop. Nothing is written.
5. **Skip what already exists.**
   - Items with an `ado_id` are skipped. Read them in ADO to confirm they still exist; if one doesn't, list it in the preview as a problem, and stop after the preview.
   - For each item without one, search the project for a work item of the same type whose tags contain its draft ID (`[System.Tags] CONTAINS '<draft_id>'`). An earlier run that broke halfway may have created it. If exactly one is found, it is adopted: its ID goes into the YAML in step 7, and nothing is created. If more than one is found, list them as a problem, and stop after the preview.
   - **Areas of what exists.** For each Epic that is skipped or adopted, read its `System.AreaPath`: its new Features go there. Note when it differs from the area asked for, and when one of its existing Features is in another area. Nothing is moved.
6. **Preview, then wait for a plain yes.** Show, in this order:
   - **Areas:** one row per area: its full path, its Epics (number and title), how many Features go with them, and the team whose backlog it is (when step 4 checked the teams). An Epic that already exists shows the area it has in ADO.
   - **Items:** one table of every item, in creation order: draft ID, type, title, parent, area, tags, and the action (create, skip with its ADO ID, or adopt with its ADO ID).
   - Under it: the project, the MCP server used, the process, how many items will be created, how many links, and the fields each item gets (see *What goes into each ADO field*).
   - **Warnings,** when there are any: Epics left in the root area while other areas were given; Epics already in ADO in another area than the one asked for; existing Features that are not in their Epic's area; areas that no team owns.
   - **The question:** yes, to create the items, or a change of areas (for example "13-19 → Mobile").

   Then, by the answer:
   - **A plain yes:** go to step 7.
   - **A change of areas**, such as "13-19 → Mobile", "4 to Web" or "the rest → Platform" ("the rest" is the area for the Epics not given another): apply it with the rules of *Area paths*, check any new area as in step 4, and show the whole preview again, with what changed since the last one at the top ("Epics 13-19: Shop\Web → Shop\Mobile"). Then wait again. If the change breaks a rule or names an area that doesn't exist, say what is wrong, show the last preview again unchanged, and wait.
   - **A yes together with a change** ("yes, but move 4 to Web") counts as a change, not a yes.
   - **Anything else:** stop.

   **Write nothing until there is a plain yes to the last preview shown.**
7. **Create the items,** Epics first, then Features, each group in backlog order. The area and the tags go into the create call (see *What goes into each ADO field*). Right after each item is created (or adopted), write its new ID into the YAML:

   ```bash
   python "<shared>/scripts/set_ado_ids.py" <file> <DRAFT-ID>=<ado id>
   ```

   The script changes only that item's `ado_id` line, so the YAML always says what exists. If a create fails, stop creating: go to step 9 with what exists, and report.
8. **Link them.**
   - Each Feature to its parent Epic (parent–child).
   - Each `depends_on` between two items: the item it depends on is the predecessor, the dependent item the successor. A `DEP-n` (an external dependency) gets no link: it is in the Description.
   - Skip a link that already exists.
9. **Check in ADO.** Read every item back, with its relations, and confirm its type, title, tags, area path, parent and dependency links. Every item created in this run has the tag `plotwork-pushed`, and every Feature created in this run is in its Epic's area. Then:
   - re-render the review page, which now shows the ADO IDs:

     ```bash
     python "<shared>/scripts/render_review.py" <file> --planning-dir <the YAML's folder>
     ```
   - add a changelog row to the main planning file (`prototype-plan.md`, `project-plan.md` or `decisions-raid.md`): the current version, today's date, Clarification, "Pushed to <project>", and the range of ADO IDs. When any Epic is not in the root area, add the areas as finally confirmed, such as "areas: Shop\Web = 1-12, 20; Shop\Mobile = 13-19; Shop\Platform = the rest".
   - Do not change `version` or `status`.
10. **Report:** created, adopted and skipped, with their ADO IDs; the links made; the areas, and the command that repeats them, ready to copy, such as `/plotwork:push --project "Shop" --area Web=1-12,20 --area Mobile=13-19 --area Platform` (with `--file` when it isn't the default, and `--mcp` when one was given); any failure, and how to resume (run that command again: nothing is created twice, and new Features follow their Epic's area in ADO). Next step: the team writes the delivery-level items under each Feature (Basic: Epic).

## What goes into each ADO field

Read the type's fields (step 3) and use only fields that exist. When a field is missing, put the value in Description, or in the tags for priority.

| From the YAML | Into ADO |
|---|---|
| `title` | Title |
| `description` (Epic: `outcome` and `success_measure`), scope in and out, `constraints` and `global_constraints` (their statements, from the planning files), `open_questions` (their text), `downstream_notes`, and any `DEP-n` dependency (what it is) | Description, as sections with headings, in Markdown or HTML as the tool supports. See *Writing the Description* |
| `design` (screens, each as `<Screen> — <where> — <Figma link>`) | Description, as a *Design* section, one link per line |
| `acceptance_criteria` | Acceptance Criteria, when the work-item type has that field. Otherwise, an *Acceptance criteria* section in Description |
| `priority`: Must, Should, Could, Won't | Priority 1, 2, 3, 4 |
| `nature`: user-facing, or enabler and verification | Value Area: Business, or Architectural (Agile, Scrum and CMMI only) |
| `rank` | Backlog order (see below) |
| draft ID, `milestone`, `readiness` when not `ready`, `prototype` when `kind: prototype`, and always `plotwork-pushed` | Tags, for example `BCH-FT-003; MS-1; needs-elaboration; plotwork-pushed` |
| The Epic's area (see *Area paths*) | Area Path. A Feature gets its Epic's: the area from `--area`, or the one its Epic has in ADO when the Epic already exists |
| `parent`, `depends_on` | Parent links, predecessor and successor links |

Iteration stays at the project default. No iterations or areas are created.

**Writing the Description.** It is read by the team, with no access to the planning files. So (and the same for Acceptance Criteria):
- Write the content in words. Leave out the planning IDs (`OBJ-`, `CAP-`, `FR-`, `NFR-`, `CON-`, `DEC-`, `ASM-`, `Q-`, `AQ-`, `DEP-`, `SRC-`, `MS-`): give a constraint's statement, a question's text, a dependency's description, a capability's name. In scope text, drop references such as "(CAP-6, Later)", or write "(later)".
- Leave out `sources`, `traces_to`, `size_hint`, `confidence` and the draft ID. The draft ID and the milestone are in the tags.
- Leave out a section that would be empty.

**What `rank` is:** a field `plan` already writes. It gives the order to deliver Features (Basic: Epics) in, within a milestone (1 = first). The push uses it to put the ADO backlog in that order, so the team sees the planned sequence. Sort the items by milestone, then rank, and give them increasing values (1000, 2000, …) in the type's backlog-order field: Backlog Priority in Scrum, Stack Rank in the others. Epics in Agile, Scrum and CMMI are ordered by their earliest Feature.

## Never

- write to ADO before a plain yes to the last preview shown;
- create any type other than Epic and Feature, or create iterations, areas or queries;
- give a Feature an area other than its Epic's;
- delete a work item, or change the fields of one that already existed or that you adopted, its area included (adding a missing link from step 8 is fine);
- edit the YAML by hand to write an ADO ID: use `set_ado_ids.py`;
- choose the project, or choose the server when more than one Azure DevOps server is connected;
- call a tool from any server other than the one chosen.
