# Plotwork user guide

This guide is for anyone who uses Plotwork to plan a software project. You don't need to be a developer. It explains every command: what it does, when to use it, what Claude asks you, how to answer, and what you get at the end. Nothing is hidden: each page also says which helpers the command calls and what they do.

## What Plotwork does

You have an idea for an app, a roadmap, some planning documents, or a working prototype the client already liked. Your team needs a backlog in **Azure DevOps**, the tool where they track their work.

Plotwork turns what you have into that backlog. It writes two kinds of items:

- **Epics:** big areas of the product, such as "Run a book club without spreadsheets".
- **Features:** things a user can notice and use, such as "Choosing the next book". Each Feature belongs to one Epic.

Each Feature gets a card with a description, what is in and out, the checks that say it is done (the *acceptance criteria*) and where it came from. When you approve the plan, Plotwork creates the items in Azure DevOps for you.

Plotwork stops at Epics and Features. Your team writes the smaller items (user stories, tasks) under each Feature later, because those depend on technical choices they make.

## Who does the work

| Who | What they do |
|---|---|
| **You** | Bring your idea or documents, answer questions, and approve. Nothing is final until you say so |
| **Claude** | Reads everything, asks the questions, writes every file and fixes what is wrong |
| **The reviewer** | A second AI that checks Claude's plan before you see it, so you are not the only check |
| **The app reader** | A second AI that reads a working prototype's code and lists its screens (only for `/plotwork:from-app` and `/plotwork:from-app-update`) |
| **The screen builder** | A second AI that rebuilds a prototype's screens so they can go to Figma (only when you ask for Figma) |

[The helpers](the-helpers.md) explains each helper: what it may do, what it may never do, and which command calls it.

## The journey

```text
  Your idea, roadmap, documents or working prototype
          │
  Start a planning command
          │
          ├── Stop 1: Claude says what it understood and asks its questions. You answer.
          │
  Claude writes the plan. The reviewer checks it. Claude fixes what the reviewer found.
          │
          ├── Stop 2: Claude shows the finished plan. You approve it, or ask for changes.
          │
  /plotwork:push sends it to Azure DevOps
          │
          ├── Preview: Claude shows exactly what it will create. You say yes.
          │
  Epics and Features in Azure DevOps. Your team takes it from there.
```

The two stops are called **G0** and **G3** in Claude's messages. G0 is "the assessment" (stop 1). G3 is "the breakdown" (stop 2).

## Which command to use

You don't have to type the commands. You can say what you want in plain words, such as "plan this app idea for Azure DevOps" or "apply these meeting notes to the plan". Claude picks the right command. But it helps to know them.

| You have… | And you want… | Use | Page |
|---|---|---|---|
| Nothing yet, just curiosity | To see what Plotwork makes | `/plotwork:demo` | [Seeing an example](seeing-an-example.md) |
| An idea, a roadmap or documents | A plan for the whole project | `/plotwork:plan` | [Planning a project](planning-a-project.md) |
| An idea, a roadmap or documents | A plan for a small first version only | `/plotwork:prototype` | [Planning a prototype](planning-a-prototype.md) |
| A working app the client approved, built on another platform | A plan from what that app does | `/plotwork:from-app` | [Planning from an external prototype](planning-from-an-app-prototype.md) |
| A working app the client approved, built on another platform | The plan plus the app's screens in Figma too | `/plotwork:from-app … --figma` | [Screens in Figma](screens-in-figma.md) |
| A plan made with `plan` or `prototype` | To change it before it goes to Azure DevOps | `/plotwork:update` | [Changing a plan](changing-a-breakdown.md) |
| A plan made with `from-app` | To apply client notes or a newer version of the app | `/plotwork:from-app-update` | [Updating a plan made from an app](updating-an-app-plan.md) |
| A small first version that proved its point | To grow it into a full plan | `/plotwork:plan` | [Planning a prototype](planning-a-prototype.md#growing-it-into-a-full-plan) |
| An approved plan | The items in Azure DevOps | `/plotwork:push` | [Sending the plan to Azure DevOps](pushing-to-azure-devops.md) |

Every command that changes something always shows you what it will do first, and waits for your answer.

## The pages

| Page | Read it when |
|---|---|
| [Getting ready](getting-ready.md) | Before your first plan |
| [Setup](setup.md) | Someone has to install Plotwork, Python, or the Azure DevOps or Figma connection. It is the one technical page: send it to your IT team |
| [The helpers](the-helpers.md) | You want to know who checks and reads what |
| [Seeing an example](seeing-an-example.md) | You want to see a finished result first |
| [Planning a project](planning-a-project.md) | You use `/plotwork:plan`. It also explains the two stops, which every planning command uses |
| [Planning a prototype](planning-a-prototype.md) | You use `/plotwork:prototype`, or want to grow a small first version into a full plan |
| [Planning from an external prototype](planning-from-an-app-prototype.md) | You use `/plotwork:from-app` |
| [Screens in Figma](screens-in-figma.md) | You want the prototype's screens in Figma |
| [Changing a plan](changing-a-breakdown.md) | You use `/plotwork:update` |
| [Updating a plan made from an app](updating-an-app-plan.md) | You use `/plotwork:from-app-update` |
| [Sending the plan to Azure DevOps](pushing-to-azure-devops.md) | You use `/plotwork:push` |
| [Your files](your-files.md) | The plan is ready and you have to review it |
| [Troubleshooting and FAQ](troubleshooting-and-faq.md) | Something didn't go as you expected, or you want to spend less |

## The words you need

| Word | Means |
|---|---|
| **Epic** | A big area of the product. It groups Features |
| **Feature** | Something a user can notice and use. It is the main unit of the plan |
| **Breakdown** | The full list of Epics and Features. Claude calls the whole result "the breakdown" |
| **Process** | How your Azure DevOps project is set up: **Basic**, **Agile**, **Scrum** or **CMMI**. Each one names its items a little differently. You always choose it; Claude never guesses. In Basic there are only Epics, no Features |
| **Milestone** | A release or a checkpoint, such as "Release 1". Each Feature belongs to one. Written `MS-1`, `MS-2` and so on |
| **Priority** | **Must**, **Should**, **Could** or **Won't**. Claude uses yours. If you gave none, it suggests some and marks them "(proposed)" |
| **ready** / **needs-elaboration** / **blocked** | How complete an item is. *Ready* means the team can start on it. *Needs elaboration* means a question is still open. *Blocked* means something outside the item stops it |
| **Project size** | **Light**, **Standard** or **Rigorous**. A bigger or riskier project gets more planning files |
| **External prototype** | A working app your team built with the client on another platform. Not the same as a Plotwork *prototype*, which is a plan for a small first version |
| **Delivery-level items** | User stories, PBIs, Requirements, Issues and tasks. Your team writes them later. Plotwork never does |
| **(proposed)** | Claude suggested this because your documents didn't say. You confirm it at stop 2 |

When you want the reason behind a rule, the [planning standard](../shared/references/standard.md) holds every rule and why it exists. You don't need it to use Plotwork.
