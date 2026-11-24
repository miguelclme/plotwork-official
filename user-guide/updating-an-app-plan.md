# Updating a plan made from an app: `/plotwork:from-app-update`

Back to the [user guide](README.md).

`/plotwork:from-app-update` changes a plan that [`/plotwork:from-app`](planning-from-an-app-prototype.md) made from an external prototype (a working app built on another platform). Changes reach such a plan in two ways:

- **the client sends notes:** meeting notes, feedback, a list of changes, in a file;
- **the team changes the app** and sends you a newer version of its code, in a folder.

This command handles both. It works like [`/plotwork:update`](changing-a-breakdown.md), and also keeps the screen inventory up to date.

**Use it** before the plan is sent to Azure DevOps. After that, change the items in Azure DevOps.

**Don't use it** for a plan made from an idea or documents (use [`/plotwork:update`](changing-a-breakdown.md)), or to make a first plan (use `/plotwork:from-app`).

**Helpers it calls:**

- the [app reader](the-helpers.md#the-app-reader), only when you give a newer version of the app. It reads only the files that changed;
- the [reviewer](the-helpers.md#the-reviewer), before stop 2;
- with `--figma` only, the [screen builder](the-helpers.md#the-screen-builder), after you reply "yes figma".

## Start it

```text
/plotwork:from-app-update client-notes-2026-11-20.md
/plotwork:from-app-update ../booking-prototype-v2
/plotwork:from-app-update ../booking-prototype-v2 --figma https://www.figma.com/design/AbC123/Booking
```

| You add | It means |
|---|---|
| A file | A document of changes |
| A folder | A newer version of the app, unzipped |
| `--figma <link>` | Also rebuild the new and changed screens in Figma. **Only with a folder:** screens are rebuilt from code, so they can't show changes that exist only in a document |
| `--help` | Show the options and stop |

Any other option stops the command. A zip file: Claude asks you to unzip it first.

## What Claude checks first

| It finds | It does |
|---|---|
| No plan | Suggests `/plotwork:from-app`, and stops |
| A plan with no screen inventory (made from an idea or documents) | Points you to `/plotwork:update`, and stops |
| A plan already sent to Azure DevOps | Says changes are now made in Azure DevOps, and stops |

## Step 1: Claude works out what changed

**Nothing is saved before you confirm.** In this step Claude only reads.

**With a file of notes:** Claude reads it and lists every change in it. If nothing applies to the plan, it says so and stops.

**With a newer folder:**

1. **Claude compares the files** with the fingerprints saved last time, so it knows which files were added, removed or changed. This works even if you unzipped the new version over the old folder.
2. **If no file differs,** it says "No update made" and stops.
3. **The [app reader](the-helpers.md#the-app-reader) reads only the changed files,** and reports every screen, rule or finding they affect.
4. **Claude compares those screens with the inventory:** new or removed screens, a screen whose state changed (a mocked screen that now really works, for example), changed behaviour, fields, checks, rules, roles, outside services, and how a screen looks.
5. **If files changed but nothing the plan describes did** (a file was only reformatted, for example), it says "No update made" and stops.

A plan made before fingerprints existed is compared in full, screen by screen. It gets its fingerprints at this update.

**Either way:**

- Text in the notes or the code that gives Claude orders ("skip the review", "approve this") is quoted to you, never followed.
- A change you rejected before is not proposed again, unless it changed since. Then Claude asks: "Rejected before, but it changed: propose it again?"

## Step 2: the proposal (you answer)

Claude sends **one message** with:

- **a table of the proposed changes:** what changed, the evidence (the old and new files, when the old ones still exist), and how Claude would apply it. A mocked or placeholder screen still follows the from-app rule: what it must really do is a question, never a need;
- **every question the changes raise,** each with a suggested answer, with no limit;
- **for a newer folder:** which version it is, from when, and whether the client approved it;
- **with `--figma`:** the Figma block, proposing to rebuild the new screens and those whose look changed, each with why. Screens whose change doesn't show (a new calculation, for example) are not proposed. See [Screens in Figma](screens-in-figma.md).

**You confirm, edit or reject each change, and each screen.** With Figma, reply "yes figma" or "no figma" too. Claude applies **only what you confirmed**. If you confirm nothing, it records only the rejections, and stops.

If you defer something, Claude asks whether to plan the later release now (as a new release, whose items are created in Azure DevOps with the rest), or to keep it in the plan marked *Deferred*, with no item for now.

## Step 3: Claude applies what you confirmed

1. **Saves a copy** of the plan as it was, in `docs/planning/.previous`, for the reviewer.
2. **Records the changes you confirmed** in a file in `docs/planning/changes`, with the evidence and your answers.
3. **Records each change you rejected** in the screen inventory, so it isn't proposed again.
4. **Applies each change** like `/plotwork:update` does: only the affected items change, IDs are kept, the version goes up, and every changed file gets a line in its change history.
5. **Updates the screen inventory:** new screens added, changed ones updated, removed ones marked *Gone* (never deleted), and each screen's Features kept current. For a newer folder, it also saves the new fingerprints, and records the new version as the latest.
6. **Marks frames as stale** when a screen's look changed and Figma doesn't rebuild it in this run.
7. **Rebuilds the screens in Figma,** if you said "yes figma", and updates each item's screen links.
8. **Runs the automatic checks and calls the [reviewer](the-helpers.md#the-reviewer).** The reviewer compares the plan before and after by itself, checks that every confirmed change was made and nothing else changed, and runs the app checks too.

## Stop 2: the finished plan (G3)

As in [Planning a project](planning-a-project.md#stop-2-the-finished-plan-g3). The message also has, before the counts:

- a table of the changes applied: each change, its type, the items it touched and any new IDs;
- which items are new, changed or retired;
- with Figma: the Figma results (see [the final message](screens-in-figma.md#the-final-message)).

When you approve, the version is not raised again: it was already raised in step 3.
