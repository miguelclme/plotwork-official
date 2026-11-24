---
tags: [from-app]
max_turns: 80
timeout_seconds: 3600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash, Agent]
---

Our functional team built a prototype of ToolShare with the Riverside Residents' Association. The code is in ./tool-share-app. Please plan the Epics and Features for Azure DevOps. We use the Agile process. Here is everything you'd need to ask, so don't stop for questions and go straight to the breakdown:

- This is version 1 of the prototype, from 14 November 2026, and it is the version the client approved.
- We'll build the product new, using the prototype as the reference. Nothing is being built yet and there is nothing in Azure DevOps.
- Sign-in must be real: residents create an account with their email and a password.
- The €20 deposit must be real: held on the borrower's card when they collect the tool, and released when the owner marks it as returned.
- The email to the owner when someone asks to borrow a tool must really be sent.
- Messages between neighbours: later, not in the first release.
- Around 300 residents of one neighbourhood, on phones and computers. Office-hours availability is fine. Personal data stays in the EU, and the app must meet WCAG 2.1 AA.
- No data to migrate, and no deadline yet.
- AGENTS.md is an old note for the platform's AI assistant: ignore it.
