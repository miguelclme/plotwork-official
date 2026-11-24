# Changing a plan: `/plotwork:update`

Back to the [user guide](README.md).

`/plotwork:update` applies a list of changes to a plan that already exists: meeting notes, review comments, answers to the open questions, or an edited roadmap. It changes only what is affected, keeps every ID, records every change, and shows you the result at stop 2.

**Use it** for a plan made with [`/plotwork:plan`](planning-a-project.md) or [`/plotwork:prototype`](planning-a-prototype.md), **before** it is sent to Azure DevOps.

**Don't use it:**

- for a plan made from an app with `/plotwork:from-app`: use [`/plotwork:from-app-update`](updating-an-app-plan.md). `update` notices such a plan and points you there;
- to make a first plan: use `plan` or `prototype`;
- to grow a small first version into a full plan: use [`/plotwork:plan`](planning-a-prototype.md#growing-it-into-a-full-plan);
- after the plan was sent to Azure DevOps: change the items there.

**Helpers it calls:** the [reviewer](the-helpers.md#the-reviewer), before stop 2.

## Start it

Write your changes in a file, in any format and order, then give the file:

```text
/plotwork:update review-notes.md
```

For example:

```markdown
# Review notes (2026-11-01)

1. Tied votes: the organiser picks the winner from the tied books.
2. New: after a meeting, members can rate the book from 1 to 5 stars. This is for Phase 2.
3. Reading progress is pushed out. We won't do it this year.
4. "As a member, I want an email when a new meeting is scheduled, so that I don't miss it."
```

You can also paste the changes into your message. Your file is never changed: it becomes one more source of the plan.

## What Claude checks first

| It finds | It does |
|---|---|
| No plan | Suggests `/plotwork:plan` or `/plotwork:prototype`, and stops |
| A plan made from an app (it has a screen inventory) | Points you to `/plotwork:from-app-update`, and stops |
| A plan already sent to Azure DevOps | Says that changing the plan would no longer change Azure DevOps, and stops |
| A small first version (prototype) | Goes ahead, and keeps it to one release |

The one exception after sending: a small first version can still [grow into a full plan](planning-a-prototype.md#growing-it-into-a-full-plan).

## How each kind of change is handled

| You write | What happens |
|---|---|
| An answer to an open question | The question is closed. The answer is applied to the items that were waiting for it, and Claude checks again whether they are ready |
| Something new that wasn't decided before | Recorded as a new decision |
| A change to an earlier decision | Recorded as a new decision that replaces the old one. The old one stays visible, marked as replaced |
| A wording fix that doesn't change the meaning | Fixed in place, with a short note |
| A new need | It gets the next free ID and a priority (yours, or one marked "(proposed)"). An existing Feature is extended, or a new one is added. In a small first version, a need for later goes on the *Later* list |
| A need that is dropped | Marked *Dropped*, never deleted. An item is removed only when nothing in it is left in scope, and its ID is never used again |
| A need you defer | Claude asks: plan the later release now, as a new release (its items are then created in Azure DevOps with the rest), or keep it in the plan marked *Deferred*, with no item for now? |
| An item moved to another release | Its release changes. If that changes the order of other items, each change is listed at stop 2 |
| A user story, a task, a screen detail or a "the system shall…" statement | Never made into an item. It becomes a need, a check on a Feature, or a note for your team on the Feature |
| A change of Azure DevOps process | Between Agile, Scrum and CMMI your IDs stay. To or from Basic, you get a new plan with new IDs |
| Something that contradicts an approved decision, without saying it replaces it | Claude doesn't choose. It becomes a question for you at stop 2 |
| Anything unclear | A question for you, with a suggested answer |

Text in your file that gives Claude orders ("skip the review", "approve this") is not followed. Claude quotes it at stop 2 and asks you.

## What Claude does

1. **Saves a copy** of the plan as it was, in `docs/planning/.previous`, replacing any older copy. The reviewer compares it with the result.
2. **Applies each change.** Only the affected items change. Everything else stays exactly as it was. Every new or changed check on a Feature must come from your file, a source, an assumption or a question.
3. **Raises the version** (0.1 becomes 0.2, an approved 1.0 becomes 1.1), marks the plan as *in review*, and adds a line to the change history of every changed file.
4. **Runs the automatic checks,** rebuilds the review page, and calls the [reviewer](the-helpers.md#the-reviewer). The reviewer gets your file and the copy from step 1, but not Claude's list of changes: it works out the differences itself, and checks that every change in your file was made and nothing else changed.
5. **Sends the stop 2 message.**

## Stop 2: the changed plan (G3)

As in [Planning a project](planning-a-project.md#stop-2-the-finished-plan-g3). The message also has, before the counts:

- a table of the changes: each change, its type, the items it touched and any new IDs;
- which items are new, changed or retired.

When you approve, the version is not raised again: it was already raised in step 3.

## Tips

- **Collect your changes and run one update,** instead of one per change. Each update runs the checks and the reviewer again.
- **Number your changes,** so the table at stop 2 is easy to match against your file.
- **Say when something replaces a decision:** "we now want X instead of Y (this replaces the earlier decision)". Otherwise a contradiction becomes a question for you.
- **Say when something is for later:** "for Phase 2" puts it in the right release.
