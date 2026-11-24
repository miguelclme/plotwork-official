# Seeing an example: `/plotwork:demo`

Back to the [user guide](README.md).

`/plotwork:demo` shows a finished example of what Plotwork makes, so you know what to expect before you plan your own project. The examples are made-up projects that come with Plotwork.

**It only reads.** It writes nothing into your project, calls no helper and never touches Azure DevOps.

## The examples

| Example | What it shows |
|---|---|
| `plant-care` | A one-line idea becomes 3 Epics after one round of questions. Process: Basic. Size: Light |
| `book-club` | An approved roadmap becomes 2 Epics and 6 Features, without rewriting the roadmap. Process: Scrum. Size: Standard |
| `tool-share` | An idea becomes a small first version: 1 Epic and 3 Features, with a *Later* list. Process: Agile |

## How to use it

To see the list:

```text
/plotwork:demo
```

To see one example:

```text
/plotwork:demo book-club
```

You can also ask in plain words: "show me an example of what Plotwork makes".

## What happens

1. **No example named, or a name that doesn't exist:** Claude shows the list above and the command to run. Then it stops.
2. **An example named:** Claude reads that example's files.
3. **It runs the automatic checks** on the example, to show you they pass. Without Python it says so and skips this.
4. **It shows you, in one message:**
   - the request: what the person asked, which process and which project size;
   - how Plotwork handled it: which steps ran, what it asked at stop 1, and where it waited;
   - the result: a table of the Epics and Features, with their releases and priorities;
   - the files, each with where to find it;
   - the result of the checks, in one line;
   - two to four things worth noticing;
   - how to try it with your own project.

## Getting a copy to look through

If you want to open the files yourself, ask: "copy the book-club example into my folder". This is the only time `demo` writes anything. Claude copies the example into a `plotwork-demo/book-club` folder in your current folder. If that folder already exists, Claude asks before replacing it.

## Next step

Plan your own project with [`/plotwork:plan`](planning-a-project.md), or a small first version with [`/plotwork:prototype`](planning-a-prototype.md).
