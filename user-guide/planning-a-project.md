# Planning a project: `/plotwork:plan`

Back to the [user guide](README.md).

`/plotwork:plan` plans a whole project into Epics and Features, ready to send to Azure DevOps.

**Use it when you have:**

- a new idea, even one sentence;
- an approved roadmap or project plan;
- documents that already list some Epics, Features or user stories;
- a small first version made with `/plotwork:prototype` that you now want to grow into a full plan (see [Growing it into a full plan](planning-a-prototype.md#growing-it-into-a-full-plan)).

**Don't use it when:**

- you only want a small first version: use [`/plotwork:prototype`](planning-a-prototype.md);
- your source is a working app built on another platform: use [`/plotwork:from-app`](planning-from-an-app-prototype.md);
- a plan already exists and you want to change it: use [`/plotwork:update`](changing-a-breakdown.md);
- the project is already being built, or already has items in Azure DevOps. Plotwork only plans new projects.

**Helpers it calls:** the [reviewer](the-helpers.md#the-reviewer), once or twice, before stop 2.

## Start it

Type the command, then your request in your own words:

```text
/plotwork:plan I want to build a web app where neighbours lend each other tools. It's a new project. We use Agile.
```

```text
/plotwork:plan Here's our approved roadmap (docs/roadmap.md). It's a new project. We run Scrum. Go straight to the breakdown.
```

```text
/plotwork:plan Use docs/vision.md, docs/epics-draft.md and docs/requirements-notes.md. It's a new project for CMMI.
```

**Say these up front, and you get fewer questions:**

- **your Azure DevOps process** (Basic, Agile, Scrum or CMMI). If you don't say it, Claude always asks. Not sure? Say so, and Claude shows a short guide;
- **that the project is new.** Until you say so, Claude only assumes it, and asks you to confirm;
- **which files to use, and which ones are approved.** A document is not treated as approved just because it exists;
- who the users are, what is out of scope, any releases or deadlines, and any fixed limits.

**Point to files instead of pasting them.** Claude reads them and refers to them by section. Your own documents are never changed.

## What Claude checks first

Before anything else, Claude looks at your project's `docs/planning` folder:

| It finds | It does |
|---|---|
| Nothing | Plans from scratch |
| A small first version made with `/plotwork:prototype` | Grows it into a full plan. See [Growing it into a full plan](planning-a-prototype.md#growing-it-into-a-full-plan) |
| A full plan | Tells you a plan already exists and that `/plotwork:update` changes it. Then it stops |

It also stops if you say the project is already being built, or if you ask it to create items in Azure DevOps (that is `/plotwork:push`). If you ask for user stories or tasks, Claude explains that your team writes them later, and plans the Epics and Features instead.

## Stop 1: what Claude understood (G0)

Claude reads everything you gave it. Then it sends **one message** with:

1. **A short summary** (5 to 10 lines): what you brought, what can be reused, what is missing, your process, how it will plan, and the project size it suggests (Light, Standard or Rigorous).
2. **One round of questions,** as many as your project needs, grouped by topic, the most important first. Each one comes with a suggested answer, except the process: that choice is always yours. Small open points aren't asked: Claude lists them as open questions in the plan.
3. **Its suggested result** for this stop: go ahead, go ahead with some assumptions, or stop.

It may look like this:

```text
1. Who uses it? Suggested: the neighbours on one street, about 20 households.
2. What is out of scope? Suggested: payments, deposits, delivery.
3. Which Azure DevOps process will this project use: Basic, Agile, Scrum or CMMI?
4. Does it need to work on phones? Suggested: yes, in a phone browser.
```

**How to answer:**

- **Answer everything in one message, by number.** `1 ok, 2 ok, 3 Agile, 4 ok` is enough.
- **"ok" accepts a suggestion.** A plain `ok` accepts them all, but it doesn't choose a process. If the process is still open, name it.
- **Correct anything wrong in the summary,** such as the project size.
- **Add anything you like.** "Also, members must be able to leave a club" becomes part of your sources.

**Claude also tells you at this stop when:**

- **A document contains text that reads like an order to Claude** ("skip the review", "ignore the earlier priorities"). Claude does not follow it. It quotes it back to you, says which file it came from, and asks what you want.
- **The project is out of scope:** it is already being built (Claude stops), or your Azure DevOps process has been customised (Claude can still write the planning files, but not the Epics and Features).
- **You haven't chosen a process yet.** Claude can finish the planning files, but writes no Epics or Features until you choose.

### Skipping stop 1: "go straight to the breakdown"

Add **"go straight to the breakdown"** to your request. Claude then skips stop 1, if you named the process and nothing important is missing. It records stop 1 as approved by you in advance, and lists every assumption it made at stop 2, for you to confirm. You always still get stop 2.

This works best for an approved, complete roadmap. For a one-line idea, the questions usually matter: without them, many answers become guesses you have to check later.

## Between the stops

Claude now works without stopping. This usually takes a few minutes:

1. **It writes the planning files.** Which files depends on the project size (see [Your files](your-files.md#which-files-you-get)). It writes only what is needed: if your roadmap is already complete, it uses it as it is and writes no new documents.
2. **It writes the Epics and Features.** Each Feature gets its description, scope, acceptance criteria, release, priority and where it came from.
3. **It runs the automatic checks** and fixes every problem it caused.
4. **It calls the [reviewer](the-helpers.md#the-reviewer)**, fixes what the reviewer found, checks again, and calls the reviewer a second time if the first round found serious problems.
5. **It builds the review page,** a readable version of the whole plan.

A short second round of questions happens only when one of your answers raised something that blocks the plan.

**Three results often surprise people:**

- **A roadmap's phases become releases (milestones), not Epics.** Epics group what the product does. A phase is a point in time.
- **Every Epic and Feature is fully described, whatever release it is for.** A Feature for release 3 has as much detail as one for release 1. Where something is missing, the item is marked *needs-elaboration*, with a question that says what is missing.
- **User stories and "the system shall…" statements in your documents don't become items.** Claude keeps them on the Feature they belong to, as notes for your team.

## Stop 2: the finished plan (G3)

Claude sends **one message** with:

1. **Where the review page is** (`docs/planning/work-breakdown.review.md`). This is the file you read. [Your files](your-files.md#reading-the-review-page) explains it section by section.
2. **The counts:** how many items are ready, need more detail, or are blocked.
3. **The independent review:** the reviewer's verdict, what Claude fixed, and any warning it kept, with the reason.
4. **What needs you,** numbered, each with a suggested answer: problems only you can fix, warnings to accept, open questions, assumptions to confirm, and priorities Claude suggested because your documents gave none. Each assumption says what confirming or dropping it changes.
5. **Its suggested result:** go ahead, go ahead with assumptions, or something must change first.

The suggested answers are in this message, not on the review page.

**While you read the review page, ask yourself:** Is every Epic and Feature something we want? Is anything missing? Did Claude invent a check nobody asked for? Are the priorities and releases right? Are the assumptions true?

**How to answer:**

| You reply | What happens |
|---|---|
| `approve` | Claude marks the plan approved, gives it version 1.0 (or the next version), rebuilds the review page and tells you it is ready for `/plotwork:push` |
| `approve, 1 ok, 2 ok, 3 the organiser picks the winner` | Claude applies your answers, then approves |
| The changes you want, in plain words, in one message | Claude makes them, checks and reviews again, and sends a new stop 2 message |

Don't edit the review page by hand: Claude rebuilds it from the plan, so your edit would be lost. To change the plan, ask in the same conversation, or later use [`/plotwork:update`](changing-a-breakdown.md).

## Next step

[Send the plan to Azure DevOps](pushing-to-azure-devops.md) with `/plotwork:push`.
