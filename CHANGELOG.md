# Changelog

What changed in each Plotwork release. Versions follow [Semantic Versioning](https://semver.org).

## [0.1.0] - 2026-11-24

First public release, in beta.

### Added

- **`/plotwork:plan`** turns an idea, a roadmap or existing documents into a reviewed breakdown of Epics and Features, for the Basic, Agile, Scrum or CMMI process. Every Epic and Feature traces back to your sources.
- **Questions instead of guesses.** What your sources don't say becomes a question for you. Claude writes, and you answer and approve at each stop.
- **A second model reviews the breakdown** before you see it, and automatic checks run on it after every change.
- **A review page** is built from the plan file, `work-breakdown.yaml`, so you and your team read the Epics and Features as cards. Each item has a short ID that never changes.
- **`/plotwork:prototype`** plans only a small first version, with a list of what comes later. `/plotwork:plan` can grow it into a full plan.
- **`/plotwork:from-app`** plans from the code of an external prototype, a working app built on another platform. It reads the code without running it, and lists every screen and what it really does.
- **Screens in Figma.** With `--figma`, `/plotwork:from-app` rebuilds the screens in a Figma design file and links each Feature to its screens. `/plotwork:from-app-update` rebuilds only the new and changed ones.
- **`/plotwork:update`** and **`/plotwork:from-app-update`** apply changes to a plan: meeting notes, review comments, or a newer version of the external prototype. IDs are kept, and every change is logged.
- **`/plotwork:push`** creates the approved Epics and Features in Azure DevOps, after a preview you confirm. It writes the new work item IDs back into the plan.
- **`/plotwork:demo`** shows a finished example, so you can see the result before planning your own project. It writes nothing into your project.
