<p align="center">
  <img src="assets/banner.svg" alt="Plotwork" width="880">
</p>

<h1 align="center">Mark out the plot before you dig</h1>

<p align="center"><b>Plotwork turns an idea, a roadmap or an external app prototype into a reviewed Azure DevOps breakdown of Epics and Features, or a small prototype of it, and pushes it to Azure DevOps. Claude writes. You answer and approve.</b></p>

<p align="center">
  <img src="https://img.shields.io/badge/status-beta-C0392B" alt="status: beta">
  <img src="https://img.shields.io/badge/works%20with-Claude%20Code-D58000" alt="works with Claude Code">
  <img src="https://img.shields.io/badge/Azure%20DevOps-Basic%20%7C%20Agile%20%7C%20Scrum%20%7C%20CMMI-272E3E" alt="Azure DevOps: Basic, Agile, Scrum, CMMI">
  <a href="https://github.com/miguelclme/spadework-official"><img src="https://img.shields.io/badge/family-Spadework-D58000" alt="family: Spadework"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-D58000" alt="license: MIT"></a>
</p>

<table>
  <tr>
    <td align="center" width="25%"><h3>~97%</h3>score on quality checks with Plotwork, across 23 test cases</td>
    <td align="center" width="25%"><h3>45%</h3>for the same tasks, without Plotwork (Claude Code "Vanilla")</td>
    <td align="center" width="25%"><h3>Every Feature</h3>traced back to the part of your idea or roadmap it came from</td>
    <td align="center" width="25%"><h3>4 processes</h3>Basic, Agile, Scrum and CMMI. The breakdown takes the shape of yours</td>
  </tr>
</table>


## Why

A roadmap is not a backlog. Turning one into Epics and Features by hand, or with a single prompt, goes wrong in familiar ways: phases become Epics, acceptance criteria appear that nobody asked for, user stories creep into Features, and nothing links a Feature back to the need it serves.

Plotwork follows a written method, the [planning standard](shared/references/standard.md): every rule, and the reason behind it. You don't need to read it to use Plotwork. Every Epic and Feature traces back to your sources. Open points become questions for you, not guesses. And a second model checks the result before you see it.

## What you get

Here is the [book-club example](shared/examples/book-club). The input was a one-page roadmap with three phases; the team runs Scrum.

```text
Epic: Run a book club without spreadsheets               Must have
  Feature: Club setup & membership                       Release 1 · Must have
  Feature: Meetings                                      Release 1 · Must have · needs club setup first
  Feature: Choosing the next book                        Release 1 · Must have · needs club setup first
  Feature: Quality verification before public launch     Release 3 · Must have · after everything else
Epic: Member engagement                                  Should have
  Feature: Discussion threads per book                   Release 2 · Should have · needs choosing the next book first
  Feature: Reading progress                              Release 2 · Should have · needs choosing the next book first
```

The roadmap's phases became releases. The Epics group what the product does. Phase 2 also became an Epic only because it matches exactly one area of the product.

Each Feature comes with a card your team can work from:

> **Club setup & membership** · Release 1 · Must have · ready
>
> Organisers create a club and invite members, who join from an invite link.
>
> **Acceptance criteria**
> 1. An organiser can create a club with a name and a description.
> 2. An organiser can share an invite link for the club.
> 3. A person with the link can join the club as a member.
>
> **Out of scope:** finding public clubs, because the roadmap doesn't ask for it.
> **Comes from:** roadmap, Phase 1, "Create a club" and "Invite members by link".

Behind the cards sits a structured file, `work-breakdown.yaml`, plus a readable review page generated from it. Each item has a short ID (such as `BCH-FT-001`) that never changes, so you and the team can refer to it from the first draft onwards.

## Try it in a minute

**You need** Claude Code (the CLI, the desktop app or the IDE extension), and Python (tested with 3.14) for the checking scripts. They use only the standard library; without Python, Claude runs the same checks by hand and tells you so. To push, you also need Microsoft's local Azure DevOps MCP server and Node.js 20 or newer ([how to connect it](user-guide/setup.md#azure-devops)).

Add the marketplace and install the plugin:

```bash
claude plugin marketplace add miguelclme/plotwork-official
```

```bash
claude plugin install plotwork@plotwork
```

Inside a Claude Code session, the same commands are `/plugin marketplace add miguelclme/plotwork-official` and `/plugin install plotwork@plotwork`.

Start a new session, so the skills load, and look at a finished example. The demo writes nothing into your project:

```text
/plotwork:demo book-club
```

Then plan your own:

```text
/plotwork:plan I want to build a web app where neighbours lend each other tools.
```

When the breakdown is approved, create it in Azure DevOps:

```text
/plotwork:push --project "Tool Share"
```

To update the plugin: `claude plugin marketplace update plotwork`, then `claude plugin update plotwork`. To remove it: `claude plugin uninstall plotwork`. Your files in `docs/planning/` are never touched.

## Skills

| Skill | Use it to | Guide |
|---|---|---|
| `/plotwork:plan` | Plan a project from an idea, a roadmap or existing documents, or grow a prototype into a full plan | [Planning a project](user-guide/planning-a-project.md) |
| `/plotwork:prototype` | Plan only a small first version, with a list of what comes later | [Planning a prototype](user-guide/planning-a-prototype.md) |
| `/plotwork:from-app <folder>` | Plan from the code of an external prototype (a working app built with the client on another platform), and optionally rebuild its screens in Figma (`--figma`; `--figma-only` adds or refreshes only the missing or out-of-date ones later, `--force` rebuilds all) | [Planning from an external prototype](user-guide/planning-from-an-app-prototype.md) |
| `/plotwork:from-app-update <folder or file>` | Apply a newer version of the external prototype, or client notes, to a plan made with `from-app` | [Updating a plan made from an app](user-guide/updating-an-app-plan.md) |
| `/plotwork:update <changes-file>` | Apply changes to a breakdown made from an idea or documents, before it is pushed | [Changing a plan](user-guide/changing-a-breakdown.md) |
| `/plotwork:push --project "<name>"` | Create the approved Epics and Features in Azure DevOps, after a preview you confirm | [Sending the plan to Azure DevOps](user-guide/pushing-to-azure-devops.md) |
| `/plotwork:demo <example>` | See a finished example | [Seeing an example](user-guide/seeing-an-example.md) |

You don't have to type the commands: describe what you want, and Claude picks the right skill. Plotwork stops at Epics and Features; your team writes the user stories and tasks under them.

## Documentation

- [User guide](user-guide/README.md): how to use every command, in plain words, from the first request to the push.
- [Planning standard](shared/references/standard.md): the method's rules, and the reasons behind them.

## How it's tested

The cases in [`evals/`](evals) each hold a prompt, input files and the checks a good result must pass. Each case runs with Plotwork and again with the same Claude and no plugin, to show what the plugin adds. Claude Opus 5.5 did the work, and Claude Sonnet judged each check. The score is the share of checks passed.

| Test case | With Plotwork | Without |
|---|---|---|
| An approved roadmap planned into Scrum | 0.88 | 0.12 |
| A new idea with no process chosen | 1.00 | 0.14 |
| A request for user stories | 1.00 | 0.20 |
| A new idea planned as a prototype | 0.78 | 0.56 |
| A prototype asked for when a full plan exists | 1.00 | 0.00 |
| Six review notes applied to a breakdown | 0.93 | 0.50 |
| The demo lists its examples | 1.00 | 0.33 |
| The demo shows the book-club example | 1.00 | 0.20 |
| A push with no project named | 1.00 | 0.80 |
| A push with no Azure DevOps server connected | 1.00 | 0.80 |
| The push's `--help` | 1.00 | 0.57 |
| A push with `--area` on a Feature | 1.00 | 0.50 |
| A push with an option it doesn't take | 1.00 | 0.50 |
| An external prototype read, questions asked | 0.96 | 0.20 |
| An external prototype planned, answers given in advance | 0.96 | 0.56 |
| `--figma` with no Figma server connected | 1.00 | 0.71 |
| A plan made from an idea, sent to from-app | 1.00 | 0.50 |
| from-app with an option it doesn't take | 1.00 | 0.50 |
| from-app-update with `--figma` and a notes file | 1.00 | 0.43 |
| from-app-update's `--help` | 1.00 | 0.43 |
| A newer version of the external prototype | 0.84 | 0.53 |
| Client notes applied to a plan made from an app | 0.94 | 0.63 |
| from-app-update on a plan already pushed | 1.00 | 0.57 |
| **Mean** | **0.97** | **0.45** |

Read these numbers as evidence that the steps work, not as a guarantee. You still review and approve every breakdown.

## Plotwork and Spadework

Plotwork and [Spadework](https://github.com/miguelclme/spadework-official) belong to the same family. Plotwork marks out the plot: it plans the Epics and Features, and pushes them to Azure DevOps. Spadework does the digging: it triages the work items already in Azure DevOps, then builds, reviews and tests them.

## Reporting a bug or asking for an improvement

Plotwork's author maintains it and makes every change, so this repository takes no pull requests.

Found a wrong breakdown, a confusing question, a bug, or something that could work better? [Open an issue](https://github.com/miguelclme/plotwork-official/issues). Say what you asked Plotwork to do, what happened, and what you expected.

## License

MIT. See [LICENSE](LICENSE).
