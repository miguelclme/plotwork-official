# Example: tool-share

A hypothetical project, planned as a prototype with the `prototype` skill from a one-line idea.

| | |
|---|---|
| **Scenario** | A — only an idea, no documents |
| **ADO process** | Agile: Epics and Features |
| **Kind** | Prototype: one milestone, `MS-1 Prototype`, and a *Later* list |
| **Rigor profile** | Light: one street, names and email addresses only |
| **State** | Approved at G3 (version 1.0), ready for `/plotwork:push` |

## What the user asked

> I want a web app where neighbours lend each other tools. Nothing is built yet. Before we plan the whole thing, I want a prototype to see if neighbours actually lend.

## How the skill handled it

1. **Stage 0 and G0.** Claude wrote the assessment and, in the same message, proposed the prototype's scope: membership, tool listings and borrowing in, and reviews, deposits and more neighbourhoods for later. It asked 4 questions, each with a proposed answer except the process:
   - which ADO process to use;
   - who will try it;
   - what the prototype must prove, and how you'll know it worked;
   - any data limits.

   The user answered: Agile; about 20 households on their street; at least 5 loans in the first 4 weeks; names and email addresses only. They accepted the proposed scope with "ok".
2. **The prototype plan.** Claude wrote `prototype-plan.md`: the assessment, what the prototype must prove, 3 capabilities with 7 needs, the *Later* list of 3 capabilities, and the decisions.
3. **Stage 3 and G3.** Claude wrote 1 Epic and 3 Features, all in `MS-1`, validated them (M17 checks the prototype's shape), had them reviewed, and stopped for approval. The user approved.

## The result

| Epic | Feature | Milestone | Priority |
|---|---|---|---|
| TSH-EP-001 Neighbours lend each other tools | TSH-FT-001 Street membership | MS-1 | Must |
| | TSH-FT-002 Tool listings | MS-1 | Must |
| | TSH-FT-003 Borrowing | MS-1 | Must |

**Later:** CAP-4 Reviews and trust, CAP-5 Deposits for valuable tools, CAP-6 More than one neighbourhood.

## Files

| File | What it holds |
|---|---|
| `docs/planning/prototype-plan.md` | Assessment, what the prototype must prove, needs, the *Later* list, decisions and questions, all in one file |
| `docs/planning/work-breakdown.yaml` | The breakdown, with `kind: prototype`: the file `/plotwork:push` reads |
| `docs/planning/work-breakdown.review.md` | The generated review view, with the Prototype banner and the *Later* list |

## What to notice

- **The smallest set that proves the point.** Every Feature is needed for a loan to happen; nothing else is in.
- **Deferred capabilities are listed, not lost.** They are on the *Later* list with the status Deferred, so they need no coverage now and never become items.
- **It can grow.** `/plotwork:plan` turns this into a full plan, keeping TSH-EP-001 to TSH-FT-003 and their ADO IDs, and bringing the *Later* capabilities into scope.
