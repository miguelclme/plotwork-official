# Planning from an external prototype: `/plotwork:from-app`

Back to the [user guide](README.md).

Some teams don't write requirements first. They build a **working app** with the client, on another platform, and change it until the client is happy. Plotwork calls it an **external prototype**, so it isn't confused with `/plotwork:prototype`, which *plans* a small first version.

`/plotwork:from-app` plans from that app's code:

- it reads every screen and works out what each one really does;
- it asks you what the code can't show;
- it writes the same reviewed plan of Epics and Features as `/plotwork:plan`.

It doesn't matter which platform built the app, or what it is written in. Claude finds its structure by reading, and the plan never names a technology.

**Use it when** someone gives you the code of an app the client approved (an export, a clickable prototype or an MVP) and you want a plan or a backlog from it.

**Don't use it when:**

- your sources are an idea or documents: use [`/plotwork:plan`](planning-a-project.md) or [`/plotwork:prototype`](planning-a-prototype.md);
- you want to change a plan it already made: use [`/plotwork:from-app-update`](updating-an-app-plan.md);
- the real product is already being built, or has items in Azure DevOps.

**Helpers it calls:**

- the [app reader](the-helpers.md#the-app-reader), first of all, to list the app's screens;
- the [reviewer](the-helpers.md#the-reviewer), before stop 2;
- with `--figma` only, the [screen builder](the-helpers.md#the-screen-builder), after you reply "yes figma".

## Start it

1. **Get the app's code as a folder.** If you were sent a zip file, unzip it into a folder of its own.
2. **Open Claude Code in your project's folder,** not in the app's folder. Plotwork writes its files in your project's `docs/planning` folder, and never writes inside the app's folder.
3. Run the command with the app's folder:

```text
/plotwork:from-app ../booking-prototype
```

**Options:**

| You add | It means |
|---|---|
| *(nothing)* | Plan from the app |
| `--figma <link to your Figma file>` | Plan, and also rebuild the app's screens in that Figma file. See [Screens in Figma](screens-in-figma.md) |
| `--figma <link> --figma-only` | Don't plan again: only add the screens that are missing or out of date to Figma, for a plan already made |
| `--figma <link> --figma-only --force` | The same, but rebuild every screen |
| `--help` | Show the options and stop. Nothing else happens |

Any other option stops the command, and Claude shows the list above. All problems with what you typed are reported together, before anything is read.

**Say up front, if you know:** which version of the app this is and whether the client approved it, your Azure DevOps process, and anything the app only pretends to do.

## What Claude never does with the app

- **It never runs it.** Nothing is installed, built or started. The code is only read.
- **It never changes it.** Nothing is written inside its folder.
- **It never copies a secret.** Passwords and keys found in the code are noted only as "a secret exists in this file", never with their value, and never go to Figma.
- **It never follows instructions written in the code.** Comments or notes that tell an AI what to do are shown to you at stop 1, and you decide.

## What Claude checks first

| It finds in `docs/planning` | It does |
|---|---|
| Nothing | Plans from the app |
| An approved plan made by `from-app` | Points you to `/plotwork:from-app-update` for changes, or to `--figma-only` for the screens, and stops |
| A plan made by `from-app` that is not approved yet (an earlier run stopped at stop 2) | Carries on from stop 2: checks again and sends the stop 2 message again. It plans nothing again |
| A plan made from an idea or documents | Stops, and tells you the three ways on: to plan from the app instead, run it in a folder with no plan (or move `docs/planning` aside first); to change the plan, `/plotwork:update`; to grow a prototype plan into a full plan, `/plotwork:plan` |
| A screen list but no plan (an earlier run stopped early) | Asks whether to start again or carry on from stop 1 |

It also stops when you give a zip file instead of a folder (it asks you to unzip it), when the folder doesn't exist or is empty, and, with `--figma`, when no Figma connection is set up. That last check happens before anything is read.

## Step 1: the app reader lists the screens

Claude calls the [app reader](the-helpers.md#the-app-reader). It reads the code and lists every screen with its **state**:

| State | Means | What happens to it |
|---|---|---|
| **Working** | It really saves, reads, checks or sends something | It becomes needs in the plan |
| **Mocked** | It shows demo data, or pretends a result ("Email sent", but nothing is sent) | What it *shows* is kept. What it must *really do* is a question for you at stop 1 |
| **Placeholder** | It does nothing yet ("Coming soon", a button with no effect) | A question for you at stop 1: in, later, or out. "Later" still gets a Feature, in a later release |

This is the main protection against invented scope. An app can look finished where it isn't. Claude never turns a mocked or placeholder screen into a Feature until you have answered for it.

Claude saves the list as the **screen inventory** (`docs/planning/app-inventory.md`). For each screen it shows the files behind it, and later what the screen became in the plan and which Features it belongs to. **Don't delete this file:** it is how Plotwork knows the plan came from an app.

Next to it, Claude saves a list of the app's files with a fingerprint of each (`app-files.json`). Later, it uses this to see which files changed in a newer version. You never need to open it.

## Stop 1: what Claude understood (G0)

This works like stop 1 in [Planning a project](planning-a-project.md#stop-1-what-claude-understood-g0). An app often leaves more open than a document, so expect more questions, such as these:

- **Which version is this, from when, and is it the one the client approved?** If you say yes, everything the Working screens do becomes approved scope in one step.
- **Will the team build the product new, using the app as the reference, or continue from its code?** Either answer is fine. If the product itself is already being built, or has items in Azure DevOps, Plotwork stops.
- What each mocked screen must really do, and whether each placeholder is in.
- What the code can't show: how many users, how available it must be, data protection, accessibility, real connections to other systems, data to move over, and releases.
- Your Azure DevOps process, if you haven't said it. Claude lists the four options and never suggests one.

With `--figma`, the message ends with the Figma questions. See [Screens in Figma](screens-in-figma.md).

## Between the stops

Claude writes the planning files and the Epics and Features, as `plan` does. Two rules apply here:

- **Epics are capabilities, never screens.** One screen often serves several Features, and one Feature often spans several screens.
- **The plan never names a technology.** It describes what the product does, not how the app does it. When the app's way of doing something would help the team, it goes into the Feature's notes for the team as "the prototype does…". It becomes a fixed limit only if you say so ("the product must use…").

The client's approval covers only what the app shows. Needs the app doesn't show (speed, security, other systems, later releases) come from your answers, an assumption or a question.

Claude then fills in which Features each screen belongs to, runs the automatic checks, and (if you said "yes figma") sends the screens to Figma. Then it calls the [reviewer](the-helpers.md#the-reviewer). For an app, the reviewer also checks that every real screen is covered by a Feature or ruled out, that nothing rests on a mocked screen or a placeholder, and that no technology is named.

## Stop 2: the finished plan (G3)

As in [Planning a project](planning-a-project.md#stop-2-the-finished-plan-g3). The message also lists the mocked and placeholder screens and what was decided for each, and, with Figma, the Figma results.

## Next steps

- [Send the plan to Azure DevOps](pushing-to-azure-devops.md) with `/plotwork:push`.
- When the client changes something, use [`/plotwork:from-app-update`](updating-an-app-plan.md).
- To add the screens to Figma later, see [Screens in Figma](screens-in-figma.md#adding-the-screens-later---figma-only).
