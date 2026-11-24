# Troubleshooting and FAQ

Back to the [user guide](README.md).

Some fixes below need a technical step. When they do, the [setup page](setup.md) has it: send it to someone in your IT team.

## Troubleshooting

### "Unknown command" when I type `/plotwork:...`

The conversation started before Plotwork was installed, or the plugin is turned off. **Start a new conversation** in Claude Code. If that doesn't help, ask your IT team to check the plugin is installed and turned on ([setup](setup.md)).

### Claude says Python isn't available, and did the checks by hand

Python is the free program that runs the automatic checks. Without it, the plan still works (the review page says "Rendered manually by Claude"), but the checks are slower and less reliable. **To send the plan to Azure DevOps you need Python.** Ask your IT team to install it, start a new conversation, then ask Claude to "validate and re-render the breakdown".

### Stop 2 still lists a FAIL

Claude fixes every FAIL it caused. One left at stop 2 needs your decision, and the message suggests an answer. The common ones:

| Code | Usual cause | What to do |
|---|---|---|
| M6 | An item refers to a need or question that isn't defined | Ask Claude to fix the reference, or to add the missing entry |
| M7 | A *Must* need has no item | Add a Feature for it, or mark the need *Deferred* or *Dropped* |
| M13 | The plan changed after the review page was built | Ask Claude to "validate and re-render the breakdown" |
| M17 | A small first version has more than one release, or no *Later* list | Keep everything in `MS-1`, or grow it with `/plotwork:plan` |

### `plan` or `prototype` stopped at once

They found a plan in `docs/planning`. Use `/plotwork:update` to change it, or `/plotwork:plan` to grow a small first version. To start over, move the `docs/planning` folder somewhere else first.

### `from-app` stopped at once

| It said | What to do |
|---|---|
| Unzip it first | Unzip the app's zip file into a folder of its own, and give that folder |
| A plan already exists | Use `/plotwork:from-app-update` for changes, or `--figma-only` for the screens |
| The plan came from an idea or documents | To plan from the app instead, run it in a folder with no plan, or move `docs/planning` aside first. To change the plan, use `/plotwork:update`. To grow a prototype plan, use `/plotwork:plan` |
| No Figma connection | Ask your IT team to connect Figma, or run again without `--figma` |
| Files are missing (with `--figma-only`) | You gave the wrong folder, or a newer version of the app. For a newer version, use `/plotwork:from-app-update` |

### Claude saved the files in the wrong place

Plotwork writes into `docs/planning` in the folder where Claude Code is open. Open Claude Code in your project's main folder.

### The push says…

| …this | Do this |
|---|---|
| No Azure DevOps connection | Ask your IT team to connect it ([setup](setup.md#azure-devops)), then start a new conversation |
| Azure DevOps refuses the sign-in | The access has expired or lacks a permission. Ask your IT team to renew it |
| More than one Azure DevOps connection | Run the push again with `--mcp <name>`. The message gives you the command for each connection |
| The project doesn't exist | Use the exact name, in quotes: `--project "Book Club"`. Claude shows the closest names |
| The process doesn't match | Send it to a project with the plan's process, or change the plan's process with `/plotwork:update` |
| An area doesn't exist | Ask your Azure DevOps admin to create it, or use an existing one |
| "Features go with their Epic" | You gave a Feature's ID in `--area`. Give its Epic's number instead |
| An item no longer exists | Someone deleted it in Azure DevOps. Decide with your team whether to recreate it. Never edit an Azure DevOps number in the plan by hand |
| It stopped halfway | Run the same command again. Nothing is created twice |

### `update` says the plan was already sent

Once any item is in Azure DevOps, change the items there. A small first version can still grow into a full plan with `/plotwork:plan`.

### Figma: some screens failed or were not sent

The final message lists them. Run `/plotwork:from-app <folder> --figma <link> --figma-only` later: it sends only the screens that are missing or out of date. See [Screens in Figma](screens-in-figma.md#adding-the-screens-later---figma-only).

## FAQ

**Can I get user stories?** Not from Plotwork. It stops at Epics and Features, because stories depend on technical choices your team makes later. User stories found in your documents are kept on their Feature, as notes for the team.

**Does Plotwork look at my Azure DevOps project while planning?** No. Only `/plotwork:push` contacts Azure DevOps.

**Which process should I choose?** The one your Azure DevOps project uses. Your Azure DevOps admin can tell you (it is in the project's settings, on the overview page). For a new project, say you're not sure, and Claude shows a short guide.

**Why does a Feature for release 3 have as much detail as one for release 1?** Because everything in scope is fully described, so the plan doesn't hide gaps in later releases.

**Why didn't my roadmap's phase become an Epic?** A phase is a point in time, so it becomes a release. Epics group what the product does.

**What does "(proposed)" mean?** Claude suggested it because your documents didn't say. It is listed at stop 2 for you to confirm.

**Can the reviewer change my files?** No. It can only read, and it backs every finding with evidence. Claude makes the fixes. See [The helpers](the-helpers.md).

**Does the app reader run the app?** No. It only reads the code. Nothing is installed or started.

**Can I use Plotwork for a project that has already started?** Not for now. The one exception is a small first version growing into a full plan.

## Spending less

Every Claude conversation uses *tokens*: the unit your Claude usage is counted in. To use fewer:

- **Use Medium effort** in Claude Code. In tests, Medium came close to High's quality with about 20% fewer tokens and 40% less time.
- **Give the key facts in your first message:** the process, that the project is new, the users, what is out, any fixed limits. Each one is a question Claude doesn't have to ask.
- **Answer everything in one message,** by number: `1 Scrum, 2 ok, 3 no shop`.
- **[Skip stop 1](planning-a-project.md#skipping-stop-1-go-straight-to-the-breakdown)** for an approved, complete roadmap.
- **Have Python installed.** The automatic checks take a second. By hand, they cost Claude many tokens.
- **Collect your changes** into one `/plotwork:update`, and your stop 2 corrections into one message.
- **Plan a small first version first** when you're not sure the idea works.
- **Point to files instead of pasting them,** give only the documents that matter, and say which ones are approved.
- **Start a new conversation for the push.** It only needs the approved plan, not the planning conversation.
- **Only use Figma when you need it.** Rebuilding screens uses many more tokens than the plan alone.
- **Turn Plotwork off in projects where you don't plan.** Its command descriptions use a few tokens in every conversation. Your IT team can do this ([setup](setup.md)).

Don't save on the stop 2 review or the reviewer. You are the final check, and a wrong assumption in the plan becomes a wrong Feature in your backlog.

## What Plotwork can't promise

- **It isn't perfect.** The [test results](../README.md#how-its-tested) show the steps work, not that every plan is right. You still review and approve every plan.
- **The reviewer can be strict.** It sometimes flags a check that adds a small detail to your source. Treat its findings as questions, not verdicts.
- **It only knows what you tell it.** It doesn't look in Azure DevOps while planning. Missing context becomes assumptions and questions.
- **Results vary between runs.** The same request can give slightly different Features or wording. The structure and the rules stay the same.

## Reporting a problem

[Open an issue](https://github.com/miguelclme/plotwork-official/issues) with the request you gave and what you expected.
