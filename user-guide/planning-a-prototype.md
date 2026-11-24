# Planning a prototype: `/plotwork:prototype`

Back to the [user guide](README.md).

`/plotwork:prototype` plans only a **small first version** of your project: the smallest set of Epics and Features that proves what you want to prove. Everything else goes on a *Later* list.

**Use it for** an MVP, a proof of concept, a pilot, or "just the first slice" of an idea or a roadmap.

**Don't use it when:**

- a plan already exists (change it with [`/plotwork:update`](changing-a-breakdown.md), or grow it with [`/plotwork:plan`](planning-a-project.md));
- the project is already being built;
- you want to plan from a working app built on another platform. That is [`/plotwork:from-app`](planning-from-an-app-prototype.md). (Plotwork calls that app an *external prototype*, so the two are not confused.)

**Helpers it calls:** the [reviewer](the-helpers.md#the-reviewer), before stop 2.

The result is a normal plan, marked as a prototype. You can send it to Azure DevOps, and later grow it into a full plan without losing anything.

## Start it

```text
/plotwork:prototype I want a web app where neighbours lend each other tools. Just a prototype, to see if they actually lend.
```

You can bring the same things as for `plan`: an idea, a roadmap or documents. **Say up front, if you know:**

- **what the prototype must prove,** and how you'll know it worked ("at least 5 loans in the first 4 weeks");
- who will try it;
- what must be in, and what can wait;
- any data or privacy limits;
- your Azure DevOps process.

## What Claude checks first

| It finds in `docs/planning` | It does |
|---|---|
| Nothing | Plans the prototype |
| A full plan | Tells you a full plan already covers more, points you to `/plotwork:update`, and stops |
| A prototype already | Points you to `/plotwork:update` to change it, or `/plotwork:plan` to grow it, and stops |

The direction is always small first version → full plan, never the other way round. If you have a full plan and want to build a slice first, keep the plan and choose what goes first in its releases, or in Azure DevOps.

## Stop 1: what Claude understood, and the proposed scope

This works like stop 1 in [Planning a project](planning-a-project.md#stop-1-what-claude-understood-g0), with three differences:

- **Questions only on what a prototype needs:** what it must prove, who will try it, what is out, any data limits, and the process. As many as that takes.
- **The proposed scope.** The message also lists the Epics and Features Claude proposes for the prototype, and every capability it leaves for later, one line each. Its own suggestions are marked "(proposed)".
- **Your musts win.** Everything you said must be in goes in. Claude never drops one.

To change the scope, just say so: "move reviews into the prototype", "booking can wait".

## Between the stops

1. Claude writes **one short planning file**, `prototype-plan.md`. It holds what Claude found, what the prototype must prove and for whom, the capabilities in it, the *Later* list, and the decisions.
2. It writes the Epics and Features, all for one release, called `MS-1 Prototype`. Capabilities on the *Later* list never become items.
3. It runs the automatic checks. They fail a prototype with more than one release, or without a *Later* list. They don't limit its size: the reviewer checks that everything in it is needed.
4. It calls the [reviewer](the-helpers.md#the-reviewer). For a prototype, the reviewer also checks that everything in it is needed to prove the point, and that everything left out is on the *Later* list.

## Stop 2: the finished plan

As in [Planning a project](planning-a-project.md#stop-2-the-finished-plan-g3). The message also shows the *Later* list, so you see what was left out. When you approve, Claude says it is ready for `/plotwork:push`, and that `/plotwork:plan` can grow it into a full plan later.

## What a prototype looks like

| | Basic | Agile, Scrum, CMMI |
|---|---|---|
| Size | No fixed number of Epics: only what it must prove, and your musts | No fixed number of Epics or Features: only what it must prove, and your musts |
| Releases | One: `MS-1 Prototype` | One: `MS-1 Prototype` |
| Planning files | Only `prototype-plan.md` | Only `prototype-plan.md` |

In Azure DevOps, every item of a prototype also gets the tag `prototype`. To see a finished one, run `/plotwork:demo tool-share`.

## Changing a prototype

Use [`/plotwork:update`](changing-a-breakdown.md), as for a full plan. It stays a prototype: one release, small. If a change needs more than that, Claude says so at stop 2 and suggests growing it.

## Growing it into a full plan

When the prototype has proved its point, run `/plotwork:plan` in the same project. This works even after the prototype was sent to Azure DevOps.

1. **A copy is kept** in `docs/planning/.prototype`, as a record of the prototype as it was.
2. **Nothing settled is asked again.** Decisions, assumptions, answers and the process carry over. Claude asks only about the *Later* capabilities and anything new you bring.
3. **The project size is chosen for the whole product.** Everything in `prototype-plan.md` moves into the full plan's files, with the same IDs, and `prototype-plan.md` is deleted. The *Later* capabilities come into scope, with releases after `MS-1`.
4. **Every prototype item stays,** with its ID and its Azure DevOps number. New items get the next free IDs. The version goes up to the next whole number (an approved 1.0 becomes 2.0).
5. **The growth is recorded** as a decision, then checked and reviewed as usual, up to stop 2.

If the prototype was already sent, the checks warn that some items are in Azure DevOps and the new ones aren't. That is expected: after you approve, the next push creates only the new items.
