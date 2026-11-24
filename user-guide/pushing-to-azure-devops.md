# Sending the plan to Azure DevOps: `/plotwork:push`

Back to the [user guide](README.md).

`/plotwork:push` creates the Epics and Features of your **approved** plan as items in an Azure DevOps project, and links them together. It is the only Plotwork command that talks to Azure DevOps.

**Nothing is written to Azure DevOps, or to your files, until you answer a plain `yes` to the preview.**

**Use it** when the plan is approved (a full plan or a small first version).

**Don't use it** to plan or change a plan, or to create user stories or tasks.

**Helpers it calls:** none. Claude does everything itself.

## Before you start

1. **Someone must connect Azure DevOps to Claude Code** once. The steps are in the [setup page](setup.md#azure-devops). If your company has more than one Azure DevOps organization, you may have one connection for each.
2. **Check the project in Azure DevOps.** It must exist (you need its exact name), use the same process as your plan, and let you create items. If you use *areas* (see below), they must already exist. Plotwork never creates areas.
3. **Have an approved plan,** with its automatic checks passed.

## The command

```text
/plotwork:push --project "<your Azure DevOps project>"
```

| Option | Needed | What it does |
|---|---|---|
| `--project "<name>"` | **Yes** | The Azure DevOps project. Put the name in quotes when it has spaces. Claude never picks a project for you: without this option, it asks |
| `--file <path>` | No | The plan to send. You almost never need it: Plotwork uses the one in `docs/planning` |
| `--area "<area>"=<Epics>` | No | Which area a set of Epics goes to. Repeat it for each area. See below |
| `--mcp <name>` | Only with more than one Azure DevOps connection | Which connection to use |
| `--help` | No | Shows the options and stops. Nothing else happens |

Examples:

```text
/plotwork:push --project "Book Club"
/plotwork:push --project "Shop" --area Web=1-12,20 --area Mobile=13-19 --area Platform
/plotwork:push --project "Home Lab" --mcp ado-personal
```

Any other option stops the push. Every problem with what you typed is reported together, before Azure DevOps is contacted.

**More than one Azure DevOps connection?** If you don't say which one with `--mcp`, the push stops before contacting Azure DevOps. It lists the connections, and gives you the command to copy for each one. It never picks one for you.

## Areas

An **area** groups items in Azure DevOps, usually by product part or by team (`Shop\Web`, `Shop\Mobile`). You give areas to **Epics**. **A Feature always goes in its Epic's area.**

| You write | Means |
|---|---|
| (no `--area`) | Every item goes to the project's main area |
| `--area Web` | Every Epic goes to `<project>\Web` |
| `--area Web=1-12,20` | Epics 1 to 12, and 20, go to `<project>\Web` |
| `--area Web=1-12,20 --area Mobile=13-19 --area Platform` | 1–12 and 20 to Web, 13–19 to Mobile, every other Epic to Platform |

- **The numbers** are the number in the Epic's ID: in a plan with the key `BCH`, `3` means `BCH-EP-003`. The full ID works too. A range covers the Epics that exist in it. Gaps are normal, because removed IDs are never reused.
- **Only one `--area` may have no numbers.** It takes every Epic not given another area.
- **The name:** `/` becomes `\`, and the project name is added in front if it's missing (`Web` becomes `Shop\Web`).

The push stops, lists every problem and writes nothing if you give a Feature's ID ("Features go with their Epic: give the Epic's number"), a number that isn't an Epic, an Epic in two areas, two `--area` without numbers, an empty area, or an area that doesn't exist.

**Epics already in Azure DevOps keep their area there,** and their new Features follow them. The preview warns you when that differs from what you asked. Nothing is ever moved.

## What happens

1. **Checks.** The project exists. The plan is approved, passes the automatic checks, and its review page is up to date. The project uses the plan's process. Every area exists. If one check fails, Claude says what is wrong and which command fixes it, and stops.
2. **It skips what already exists.** Items that already have an Azure DevOps number are skipped (Claude checks they still exist). If an earlier push broke halfway, the items it created are found by their ID tag and **adopted**: their number goes into your plan and nothing is created twice.
3. **The preview.** Claude shows:
   - each area, with its Epics, how many Features go with them, and whose team backlog it is on (when it can tell);
   - every item: its ID, type, title, parent, area, tags and what will happen to it (create, skip or adopt);
   - the project, the connection used, how many items and links will be created, and which fields each item gets;
   - any warnings, for example Epics left in the main area, or an area that no team looks at.
4. **You answer:**

   | You answer | What happens |
   |---|---|
   | A plain `yes` | The push goes ahead |
   | A change of areas, such as `13-19 → Mobile` or `the rest → Platform` | Claude applies it, checks it, and shows the whole preview again, with what changed at the top |
   | "Yes, but move 4 to Web" | Counts as a change: you get a new preview first |
   | Anything else | The push stops. Nothing is written |

5. **It creates** the Epics, then the Features, in the planned order. Right after each item is created, its Azure DevOps number is written into your plan, so the plan always says what exists.
6. **It links** each Feature to its Epic, and each "depends on" between items.
7. **It reads everything back** in Azure DevOps to confirm it, rebuilds the review page with the Azure DevOps numbers, and adds a "Pushed to <project>" line to your plan's change history.
8. **It reports** what was created, adopted and skipped, the links, and the command that repeats your areas, ready to copy.

## What each item gets in Azure DevOps

| From your plan | In Azure DevOps |
|---|---|
| Title | **Title** |
| Description, scope, limits, open questions, notes for the team, outside dependencies, and screen links (from Figma) | **Description**, written in words for your team, without the plan's internal IDs |
| Acceptance criteria | **Acceptance Criteria** (or a section of the description when your project's items have no such field) |
| Priority: Must, Should, Could, Won't | **Priority** 1 to 4 |
| User-facing Feature, or technical/checking Feature | **Value Area**: Business or Architectural (not in Basic) |
| Release and order | **Backlog order**, so your backlog shows the planned order |
| The item's ID, its release, its readiness when not ready, `prototype` for a small first version, and always `plotwork-pushed` | **Tags.** Search for `plotwork-pushed` to find every item Plotwork created |
| The Epic's area | **Area**, for the Epic and its Features |

The iteration (sprint) stays at the project's default. Only fields your project has are used. Anything else goes into the description, except the priority, which goes into the tags.

## If something goes wrong

**Run the same command again.** Items that were created are skipped or adopted. Nothing is created twice.

The push never deletes an item, never changes an item that already existed (it only adds missing links), and never creates anything other than Epics and Features.

## After the push

- **Change the Epics and Features in Azure DevOps from now on.** `/plotwork:update` refuses a plan that was sent.
- **A small first version can still grow** into a full plan with [`/plotwork:plan`](planning-a-prototype.md#growing-it-into-a-full-plan). The next push creates only the new items.
- **Your team writes** the user stories or tasks under each Feature. [Spadework](https://github.com/miguelclme/spadework-official), Plotwork's brother plugin, can pick them up from there.
