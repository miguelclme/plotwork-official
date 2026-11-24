# Getting ready

Back to the [user guide](README.md).

This page says what you need before your first plan. The technical steps are in the [setup page](setup.md). If you are not technical, send that page to someone in your IT team: each step there takes a few minutes.

## What you need

| You need | For | Without it |
|---|---|---|
| **Claude Code** (the app, the terminal tool or the editor extension) | Everything | Plotwork can't run |
| **The Plotwork plugin** installed in Claude Code | Everything | The `/plotwork:` commands don't exist |
| **Python**, a free program | The automatic checks and the review page | Claude does the checks by hand. That is slower and less reliable, and you can't send the plan to Azure DevOps until the checks run automatically |
| **A connection to Azure DevOps** | Only to send the plan with `/plotwork:push` | Everything else works. Only the push stops |
| **A connection to Figma** and a Figma design file you can edit | Only to put an app's screens in Figma | Everything else works. Only the Figma part stops |

## Before each plan

1. **Make a folder for your project,** or use the one you already have. An empty folder is fine.
2. **Put your documents in it,** or know where they are. You can also just type your idea.
3. **Open Claude Code in that folder.** Plotwork saves everything in a `docs/planning` folder inside it. If you open Claude Code somewhere that clearly isn't a project (your home folder, for example), Claude asks where to save.
4. **After installing or updating Plotwork, start a new conversation** in Claude Code. The commands only appear in new conversations.

## Know these before you start

Claude asks fewer questions when you say these in your first message:

- **Your Azure DevOps process:** Basic, Agile, Scrum or CMMI. Not sure? Ask whoever runs your Azure DevOps project, or say you don't know and Claude shows a short guide to help you choose.
- **That the project is new:** nothing built yet, and nothing in Azure DevOps yet. Plotwork only plans new projects.
- **Which documents to use, and which ones are approved.**
- Who the users are, what is out of scope, any releases or deadlines, and any fixed limits (budget, platform, data rules).

## See an example first

Before your first real plan, look at a finished one: `/plotwork:demo book-club`. It takes a minute and writes nothing. See [Seeing an example](seeing-an-example.md).
