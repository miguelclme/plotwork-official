# Your files

Back to the [user guide](README.md).

Everything Plotwork writes goes into the `docs/planning` folder of your project. Your own documents stay where you put them, and are never changed.

## The one file you review

**At stop 2, you read `work-breakdown.review.md`, the review page,** together with Claude's stop 2 message. The page holds the whole plan in a readable form. The message holds the questions that need you, with suggested answers.

You don't have to open the other files. Open one when you want to check where something came from, or what was decided.

## Which files you get

At stop 1, Claude suggests a project size and tells you why. The size decides which planning files you get. A bigger or riskier project (many capabilities, or personal, financial or health data) gets more files.

| File | What it holds | When you get it |
|---|---|---|
| `work-breakdown.review.md` | **The review page.** The whole plan, readable | Always |
| `work-breakdown.yaml` | **The plan itself,** in a structured form that Plotwork reads. It holds the same content as the review page. This is what you approve and what the push sends | Always |
| `project-plan.md` | Everything in one file: what Claude found, the brief, the needs, the releases and the decisions | Light size |
| `prototype-plan.md` | The plan of a small first version, with the *Later* list | `/plotwork:prototype` |
| `assessment.md` | What Claude found at stop 1: your sources, what is missing, how it planned | Standard and Rigorous size |
| `brief.md` | What is built, for whom, why, and what is out | Standard and Rigorous size |
| `requirements.md` | Every need, with its priority. Look here if a Feature seems to miss something | Standard and Rigorous size |
| `roadmap.md` | The releases, when Claude had to write them | Standard and Rigorous size, with several releases |
| `decisions-raid.md` | Every decision, assumption, open question, risk and dependency | Standard and Rigorous size |
| `app-inventory.md` | **The screen inventory:** every screen of the app, what it does, what it became in the plan, and its Figma frames | `/plotwork:from-app` |
| `app-files.json` | A fingerprint of each file of the app, to spot changes later. You never need to open it | `/plotwork:from-app` |

Some folders may also appear:

| Folder | What it holds |
|---|---|
| `.previous` | A copy of the plan from before the last change, for the reviewer. You can delete it after you approve |
| `.prototype` | Your small first version as it was before it grew into a full plan. Keep it as a record |
| `changes` | The changes you confirmed with `/plotwork:from-app-update`, one file per update |

## Reading the review page

The page starts with the project name, the plan's version and its process. The line under it says the page was built automatically. If it says *"Rendered manually by Claude"*, the automatic tool wasn't available and Claude wrote it by hand.

Then come ten numbered sections. Basic has nine (no section 4). A small first version also has a *Later* section after the first.

| Section | What to look at |
|---|---|
| **1. Summary** | The counts, the status (*draft*, *in-review*, *approved*, or *superseded* when a newer version replaced it), the project size (shown as *Rigor*), and the limits that apply to everything |
| **2. Hierarchy** | The tree of Epics and Features, in delivery order. Each line shows the ID, title, priority and readiness. A Feature line adds its release, its place in that release, and what it depends on |
| **3. Feature cards** (Basic: Epic cards) | **The part your team works from.** One card per Feature: the description, what's in and out, the acceptance criteria, the limits, the dependencies, the screens (from Figma), and where it came from |
| **4. Epics** | One row per Epic: what it achieves, its scope, and its releases (not in Basic) |
| **5. Traceability coverage** | Every capability and need, with the items that cover it. A gap on a *Must* need is a problem |
| **6. Constraints and NFR coverage** | Every quality need (NFR: speed, security, accessibility…): whether it applies to everything, and which items handle it |
| **7. Dependencies** | Every "depends on", and whether it crosses Epics |
| **8. Open questions and assumptions** | Every open question and unconfirmed assumption an item relies on. The suggested answers are in the stop 2 message |
| **9. Not ready** | Every item that isn't ready, and the question that holds it |
| **10. Validation report** | The result of the automatic checks, one line per check |

**On a card:**

- **Priority** is Must, Should, Could or Won't.
- **Readiness:** *ready*, *needs-elaboration* (a question is open) or *blocked*.
- **Confidence:** how sure Claude is about the item, from what your sources said.
- **Nature:** *user-facing* (something users notice), *enabler* (something the product needs underneath, such as sign-in for everyone) or *verification* (a Feature that checks quality, such as an accessibility review).
- **Size** (S to XL) only helps decide whether to split a Feature. It is not an estimate, and it is not sent to Azure DevOps.

### The validation report

Each line shows a status, a check code and a short result.

| Status | Means |
|---|---|
| **PASS** | The check found nothing |
| **WARN** | Something to look at. It doesn't block. Claude either fixed it or says at stop 2 why it kept it |
| **FAIL** | Something is wrong. A plan with a FAIL can't be sent to Azure DevOps. Claude fixes every FAIL it caused. One still listed at stop 2 needs your decision |
| **SKIP** | The check didn't run, with the reason. The check called M13 always shows SKIP on the review page itself, because the page can't check itself while it is being written |

**The check codes** you may see:

| Code | Checks that… |
|---|---|
| M1 | The plan's file has the right shape |
| M2, M3 | Every ID is unique and starts with the project key |
| M4 | Every Feature belongs to an Epic that exists |
| M5 | Every "depends on" points to something that exists, with no loops |
| M6 | Every reference to a need, release or question points to something that exists |
| M7 | Every *Must* need is covered by an item |
| M8 | The same, for *Should* and *Could* needs (a warning only) |
| M9 | Open questions listed on items are still open |
| M10 | No Epic has only one Feature or too many, and no Feature has too many checks |
| M11 | No release holds more Features than the capacity you gave |
| M12 | Either no item or every item has an Azure DevOps number |
| M13 | The review page is up to date with the plan |
| M14 | Quality needs are not copied word for word into Features |
| M15 | No item calls itself a user story, PBI, Requirement or Issue |
| M16 | Epics are not just releases or phases in disguise |
| M17 | A small first version has one release and a *Later* list |

The reviewer's own checks are described in [The helpers](the-helpers.md#the-reviewer). Its verdict is in the stop 2 message.

## IDs and labels

- **Item IDs,** such as `BCH-EP-001` (an Epic) and `BCH-FT-003` (a Feature), never change, are never renumbered, and are never reused. `BCH` is the project key. Claude suggests one; if you want a specific key, say so in your first message. After the push, cards also show the Azure DevOps number (`ADO #1234`).
- **Planning IDs,** such as `FR-3` (a need), `NFR-2` (a quality need), `MS-1` (a release) or `Q-4` (a question), point to an entry in the planning files.
- **Labels,** such as `[Fact · SRC-1 §2]` or `[Assumption · ASM-1]`, say how sure a statement is, and where it came from. `SRC-1` is your first source, `§2` its section 2.
- **Every planning file ends with a change history,** so you can see what changed in each version.

## Editing files by hand

You can, but asking Claude is usually better, because Claude keeps the IDs, change history and checks consistent.

- **Never edit `work-breakdown.review.md`.** Claude rebuilds it from the plan, so your edit is lost. Until then, the checks report the page as out of date, which blocks the push.
- **After you edit any other file,** ask Claude to "validate and re-render the breakdown".
- **Never edit an Azure DevOps number** in the plan. Only the push writes them.
- **Keep IDs as they are.** Don't renumber them, and don't reuse a removed one.
