# Screens in Figma: `--figma`

Back to the [user guide](README.md).

When you plan from an external prototype (a working app built on another platform), Plotwork can also rebuild the app's screens in **Figma**, the design tool. That way the design the client approved reaches the team that will build the product. Each Feature is then linked to its screens, and the links go into Azure DevOps with the plan.

This works with [`/plotwork:from-app`](planning-from-an-app-prototype.md) and [`/plotwork:from-app-update`](updating-an-app-plan.md), never with the other commands.

**Helpers it calls:** the [screen builder](the-helpers.md#the-screen-builder), once for every group of up to 20 screens, after you reply "yes figma".

## Before you start

- **Someone must connect Figma to Claude Code.** The steps are in the [setup page](setup.md).
- **Create a Figma design file you can edit, or pick one, and copy its link.** It must be a *design file*. Figma can't import screens into FigJam boards, Slides or Make files. Plotwork never creates a Figma file for you.

## The commands

```text
/plotwork:from-app ../booking-prototype --figma https://www.figma.com/design/AbC123/Booking
/plotwork:from-app-update ../booking-prototype-v2 --figma https://www.figma.com/design/AbC123/Booking
/plotwork:from-app ../booking-prototype --figma https://www.figma.com/design/AbC123/Booking --figma-only
/plotwork:from-app ../booking-prototype --figma https://www.figma.com/design/AbC123/Booking --figma-only --force
```

## What Plotwork promises

- **Nothing goes to Figma until you reply exactly "yes figma".** Any other reply, even "ok", means no.
- **It only writes to Figma.** It never reads your Figma file.
- **Each run creates a new page** in your file and never changes an older one. Older frames stay where they are. The links move to the new frames.
- **It keeps Figma calls to a minimum,** because Figma may limit how many calls an account can make. It tells you before it starts how many this run needs.
- **No passwords or secret keys go to Figma.** Real-looking names and emails in the demo data are replaced with placeholders.

## What happens, step by step

1. **Before anything is read,** Claude checks that a Figma connection is set up. If none is, it stops and says so. You can run again without `--figma`.
2. **At stop 1** (or with the proposed changes, for `from-app-update`), the message ends with a **Figma block**. It asks or tells you:
   - the first time only, which Figma connection to use (it is remembered for next time);
   - whether the app is for desktop, mobile or both. Desktop screens are 1440 pixels wide, mobile ones 390. "Both" makes two frames per screen;
   - how many screens it would rebuild, and which ones. Screens Claude already proposes to leave out of the plan are listed, each with why, so you can disagree;
   - **how many Figma calls the run makes:** one to create the page, then two for every 20 screens (10 if you chose both desktop and mobile). For example, 15 screens for desktop only take about 3 calls;
   - that each run creates a new page, and why;
   - a warning that this uses many more tokens (your Claude usage) than the plan alone, twice as much for both desktop and mobile, and that the screens' content, demo data included, goes to Figma.

   The message ends with this line: **Reply "yes figma"** to rebuild the screens, or **"no figma"** to skip. Even if you asked Claude to skip stop 1, it always stops here and waits.
3. **After the plan is written,** Claude makes sure the connection really is Figma's, by asking it which Figma account it belongs to. If that fails, nothing is sent, and the plan carries on without Figma.
4. **The [screen builder](the-helpers.md#the-screen-builder) rebuilds the screens** as simple web pages, from the code, in groups of up to 20. Screens that have no frame yet go first, then the changed ones, then the rest. That way, if Figma's limit stops the run early, what's left out matters least.
5. **Claude checks each group** before sending it, adds **a new page** to your file, named `Plotwork — <project key> screens — <date>`, and sends the groups one after the other. Each screen becomes a frame named after the screen.
6. **Each item is linked to its screens.** A Feature gets a list of its screens, each with a link to its frame (in Basic, the Epic gets it). An Epic lists all its Features' screens. When you push, these links go into the item's description in Azure DevOps, under *Design*.
7. **Claude cleans up.** The temporary files are kept in a `.plotwork` folder in your home folder while it works, and deleted at the end of every run, even when something fails.

## The final message

It gives the link to the new page, and lists:

- the screens that failed and why (they keep their earlier links, if they had any);
- the screens **not sent** because Figma's call limit was reached. Run `--figma-only` later to send only those;
- the items whose screen links changed;
- a reminder: "These screens are rebuilt from the code, not captured from the running prototype. The functional team should compare them with it before they become the design reference."

**Check the frames before the team uses them.** They are close to the app, but not pixel-perfect. Images the code doesn't contain, such as logos, appear as labelled boxes.

## Out-of-date frames

The screen inventory records which version of the app each frame was rebuilt from. When a screen changes in a newer version of the app and its frame isn't rebuilt in the same run, its frame is marked **stale** (out of date). A later `--figma-only` rebuilds it.

## Adding the screens later: `--figma-only`

Use it when you said "no figma", ran without `--figma`, a run failed or hit Figma's limit, or a screen changed after its frame was built.

```text
/plotwork:from-app ../booking-prototype --figma https://www.figma.com/design/AbC123/Booking --figma-only
```

- **It plans nothing new.** It reads the plan and the screen inventory.
- **By default it rebuilds only the screens that have no frame or a stale one,** new screens first. Screens the plan rules out are left out. If nothing is missing or stale, it says so and sends nothing.
- **To rebuild every screen anyway,** add `--force`.
- **Give it the latest version of the app.** Claude checks that every file the inventory lists is in the folder. If some are missing, it stops, lists them, and tells you it is either the wrong folder or a newer version (then use `/plotwork:from-app-update`).
- **It sends one message first,** with the screens and why each is included, then the Figma block. Nothing is sent before "yes figma".
- **No review runs,** because nothing in the plan changes except the links.

What happens to the links depends on whether the plan was already sent to Azure DevOps:

| The plan was… | Then |
|---|---|
| **Not sent yet** | The links go into the plan. Only the screen links change, and an automatic check confirms this before anything is saved. The version goes up by one small step |
| **Already sent** | The plan stays as it is. Claude lists each item with its screens' links, for the team to add in Azure DevOps by hand. Plotwork never writes to Azure DevOps outside `/plotwork:push` |
