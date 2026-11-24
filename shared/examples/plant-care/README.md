# Example: plant-care

A hypothetical project, planned with the `plan` skill from a one-line idea.

| | |
|---|---|
| **Scenario** | A — only an idea, no documents |
| **ADO process** | Basic, so the breakdown has Epics only, each sized as a capability |
| **Rigor profile** | Light: one person, three capabilities, no regulated data, so everything is in one planning file |
| **State** | Approved at G3 (version 1.0) |

## What the user asked

> I want a small web app to keep track of my plants and remind me when to water them.

## How the skill handled it

1. **Stage 0 and G0.** Claude wrote the assessment, then stopped with one round of questions, each with a proposed answer:
   - which ADO process to use;
   - who the users are;
   - how reminders reach the user;
   - what is out of scope;
   - where it is hosted.

   The user answered: Basic; themselves first and the household later; a daily email; no plant identification, shop or native app; free-tier hosting.
2. **Stages 1 and 2.** These ran inside the same file, from those answers: a short brief, 8 needs (FRs), 1 NFR and 2 milestones.
3. **Stage 3 and G3.** Claude wrote 3 Epics, validated them, generated the review view and stopped for approval. The user approved.

## The result

| Epic | Milestone | Priority |
|---|---|---|
| PLT-EP-001 Plant catalogue | MS-1 | Must |
| PLT-EP-002 Watering schedule and reminders | MS-1 | Must |
| PLT-EP-003 Household sharing | MS-2 | Should |

## Files

| File | What it holds |
|---|---|
| `docs/planning/project-plan.md` | Assessment, brief, needs, NFRs, milestones, decisions and questions, all in one file (Light profile) |
| `docs/planning/work-breakdown.yaml` | The breakdown: the file `/plotwork:push` reads |
| `docs/planning/work-breakdown.review.md` | The generated review view, for people to read |

## What to notice

- **Basic has no Feature level.** Each Epic carries the Feature-level content: scope, acceptance criteria, milestone and rank.
- **A "how" question is not planned here.** "How are reminder emails sent?" is handed to the team as AQ-1.
- **Every acceptance criterion traces to a need** (FR-1 to FR-8) that the user's answers confirmed.
