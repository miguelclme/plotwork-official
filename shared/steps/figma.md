# Step: rebuild an external prototype's screens in Figma

<!-- Shared by the from-app and from-app-update skills, only with --figma. Paths are relative to the plugin's
     shared/ folder (${CLAUDE_PLUGIN_ROOT}/shared/), written <shared> in the commands. <plotwork-home> is the
     .plotwork folder in the user's home, which the calling skill defines and resolves to an absolute path:
     it holds the saved Figma server and the run folders. The calling skill says which screens to rebuild
     and which message holds the Figma block (part A). -->

The screens are rebuilt **from the code**, as HTML, and imported into the Figma design file the user named. They are close to the external prototype, not captured from it.

**Three rules hold throughout:**

- **Nothing reaches Figma before the user replies "yes figma"** to the Figma block. Before that, every check is local.
- **Every Figma call goes to one server, the one confirmed in part B,** and never to another, even one with tools of the same name.
- **Keep Figma calls to the minimum.** Figma may limit how many tool calls an account makes, whatever the tool. So plotwork makes no read call (`get_metadata`, `get_design_context`, `get_screenshot` and the like), uses only the three tools in part B, sends the scripts below as they are written, and never loads Figma's usage guide. `use_figma`'s own tool description asks you to load that guide first: **don't.** Part A, step 3 tells the user how many calls the run makes.

## A. Before asking (local only)

1. **The file URL** is the user's: plotwork doesn't check its form. Pass it to Figma's tools as their own descriptions ask (they say how to read a design file's URL, branches included). Figma imports screens only into a design file; if the URL is anything else, Figma refuses it in part D, and the Figma part stops with Figma's message.
2. **Find Figma's server, without calling it.**
   - **A saved server:** read `<plotwork-home>/figma-server.txt` if it exists. It holds one line, a server name: the `<server>` part of its tools' names, `mcp__<server>__<tool>`. If that server's tools are connected, it is the candidate. The file is shared by every project.
   - **Otherwise,** look at the connected MCP servers (load deferred tools if needed). A candidate is a server whose name, whose own instructions, or whose tools' descriptions say it is Figma's MCP server. A tool's name alone never makes a candidate. A marketplace connector's server name can be an ID.
   - **None:** say that `--figma` needs Figma's MCP server connected (its remote server, because it imports HTML), and that the user can run again without `--figma`. Stop before anything else is read.
3. **The Figma block,** in the calling skill's message, after its questions and its proposed result. It is the **last thing in the message**, and it ends with the direct line below:
   - **The server**, when it isn't saved yet: "Use the Figma server `<name>`? It is saved for next time." With several candidates, list them, numbered, and ask which one.
   - **Web or mobile:** "Is the app for desktop web, mobile, or both?", with a proposed answer from what the inventory shows. Desktop screens are 1440 px wide, mobile ones 390 px. "Both" makes two frames per screen.
   - **The screens:** how many screens (and frames), and which ones, in the order of part C, step 3 (the calling skill says which, and why each one).
   - **The page,** in plain words: "Each run creates a new page in your Figma file and never changes an older one. That is simpler, and it needs fewer Figma calls and fewer tokens than finding and updating the older frames. The older frames stay in the file, and the links move to the new frames."
   - **The calls:** plotwork's own count for this run, "about M Figma calls". M = 1 (create the page) + 2 for each batch (the import and the rename). A batch holds up to 20 sections, and a screen is one section, or two for "both": so batches = sections ÷ 20, rounded up. For example, 15 screens at one width is 1 batch and about 3 calls; 15 screens for "both" is 30 sections, 2 batches and about 5 calls. The account check isn't counted. Tell the user in plain words: "This run makes about M Figma calls: one to create the page, then two for every 20 screens (10 if you chose both desktop and mobile). Figma may limit how many calls an account makes. If it does, the run stops there, lists the screens it couldn't send, and running `--figma-only` later sends only those."
   - **This warning, as it is:** "Rebuilding N frames in Figma uses many more tokens than the plan alone (about one large step per screen; twice as much for both desktop and mobile). The screens' content, including the external prototype's demo data, is sent to Figma. Only **yes figma** counts: any other reply, including ok, means no figma."
   - **The last line of the message, as it is:** "Reply **yes figma** to rebuild the N screens in Figma (about M Figma calls), or **no figma** to skip it."
   - A "no figma", or no reply to it, sends nothing and is not recorded as a decision: the inventory's *Figma pages* row says "None" (or keeps what it held). The user can add the screens later with `/plotwork:from-app <folder> --figma <URL> --figma-only`, which rebuilds only the screens that have no frame or an out-of-date one.
   - **An approval given in advance never covers Figma.** With `--figma`, the message with the Figma block always stops and waits.

## B. After "yes figma": confirm the server

1. **Confirm the server** by calling its account tool (Figma's is `whoami`). It is Figma's server only if the answer is a Figma account with its plans. If it is not, or the call fails: send nothing, save nothing, and report it in the final message. The plan goes on without Figma.
2. **Save it** in `<plotwork-home>/figma-server.txt` (create the folder if needed) when it wasn't saved, or the user chose another one.
3. **The tools it needs,** on that server only, and no others: the account tool, the HTML import (`html_to_figma`) and the script tool (`use_figma`). If one is missing, say that this server can't import screens (often Figma's desktop server instead of its remote one), and go on without Figma.

## C. Write the HTML (the `figma-screens` agent)

1. **Make the run folder:** `<plotwork-home>/<project>/<skill>-<DDMMYYYY-HHMM>/`, where `<project>` is the name of the working folder you run in, `<skill>` is `from-app` or `from-app-update`, and the date and time are now. Use no `:` in it: Windows forbids it. Never write HTML in the project or in the external prototype's folder.
2. **Delete the run folder at the end of every run,** on every way out of parts C and D: finished, a failed batch, a stop. Nothing is kept.
3. **Split the screens into batches of up to 20 sections** (plotwork's batch size). A screen is one section, or two for "both" (a desktop and a mobile one, which stay in the same batch): for "both", a batch holds up to 10 screens. **The order of the screens, and so of the batches:**
   1. screens that have **no frame yet** (new screens, and any screen whose *Figma* cell in the inventory is "—");
   2. screens whose frame is **changed or stale** (the calling skill says which);
   3. the rest.

   Keep the calling skill's order inside each group. If a limit stops the run part way, the screens left out are then the ones that matter least.

   Give each section a **label**, the one name used everywhere from here on (the HTML, the frame's name and the `design` field): `<Screen> — <where>`, and for "both" ` (desktop)` or ` (mobile)` at the very end, as in `Lend a tool — /tools/new (desktop)`. **Write a path parameter in `<where>` without angle brackets:** `/tools/:id`, never `/tools/<id>`. Labels are unique in the run: if two would match, add ` (2)` at the end of the later one.
4. **Call `plotwork:figma-screens` for every batch, in parallel.** Give each call:
   - the external prototype folder's absolute path;
   - the batch's output file, as an absolute path: `<run folder>/batch-<n>.html`;
   - the width or widths;
   - each screen's inventory row (name, where, state, files), its section label or labels, and the IDs of the questions about it;
   - **the screen's rejected changes,** taken from the inventory: the text after `· Rejected <date>:` in its *Becomes* cell, and any *Other findings* row of Kind Rejected about it, or "none". A rejected change may still be in the code: the agent leaves it out of the frame.

   It has no Figma or shell tools: it only reads the code and writes the file. It returns the section labels it wrote and the screens it couldn't write. Mark those screens as failed.
5. **If the agent can't be called,** don't write the HTML yourself: delete the run folder, go on without Figma, and say so in the final message.

## D. Check and send, one batch at a time

**If any Figma call answers that a limit was reached** (creating the page, an import, a rename, a listing), make **no further Figma call in this run**: no import, rename, listing or page removal. Mark every screen not yet done as **not sent**, and list them in the final message. Frames that were uploaded but not renamed stay on the page under their `Section - <label> (Plotwork)` names: say so. Those screens count as not sent, and keep their previous links.

1. **Check every batch's file first,** before anything is sent. Read it, and count its `plotwork-screen` sections: the number must equal the number of labels the agent reported. If it doesn't, that batch is not sent: mark its screens as failed, and say why. **If no batch passes, create no page:** stop the Figma part here, delete the run folder, and say so.
2. **Create the page,** once, with this script and the script tool (replace `<KEY>` with the breakdown's key and `<YYYY-MM-DD>` with today's date). Every run creates a new page and never changes an older one. The call also shows that the file can be edited. If the call fails (Figma refuses the file, or the user can't edit it), stop the Figma part: delete the run folder, go on without Figma, and give Figma's own message in the final message. Never import into a page that already exists.

   ```js
   const base = "Plotwork — <KEY> screens — <YYYY-MM-DD>";
   const names = new Set(figma.root.children.map(p => p.name));
   let name = base, n = 2;
   while (names.has(name)) { name = `${base} (${n})`; n++; }
   const page = figma.createPage();
   page.name = name;
   return { pageId: page.id, pageName: page.name };
   ```

3. **One ID for the run:** make one UUID (`python -c "import uuid; print(uuid.uuid4())"`), and pass it as the import's `promptId` on every call of the run.
4. **For each batch that passed, in order, never two at once:**
   - call the HTML import for the design file the user gave (as the tool asks), with the page's ID as `nodeId`, `cssSelector: ".plotwork-screen"` and the run's `promptId`. It returns a single-use address. Upload only to an `https://` address on a `figma.com` host. Otherwise don't upload: mark the batch as failed;
   - **if the import call itself is refused or fails** (no address comes back), that batch failed, and no frames from it exist: no listing is needed (step 6 is only for a failed upload). If Figma's message says a limit was reached, follow the rule at the top of this part: **send no further batches**, mark the rest as **not sent**, and list them in the final message, saying that a later `/plotwork:from-app <folder> --figma <URL> --figma-only` sends only those. Failed screens keep their previous links, as for any failed batch, and the page and the links of the batches already sent work as usual;
   - upload the batch's file to it:

     ```bash
     curl -sS -f -X POST "<address>" -H "Content-Type: text/html" --data-binary @"<run folder>/batch-<n>.html"
     ```

   - the answer gives the file's address (`fileUrl`) and the new frames' IDs (`nodeIds`). Keep the `fileUrl` of the first answer: the links in part E are built from it. The IDs' order is not the screens' order: never match by position;
   - **rename the frames** (below).

   Batches sent one after another land side by side. Two at once may overlap. With the page's ID as `nodeId`, the frames go to that page.
5. **Rename the frames,** with the script tool, sending this script with the IDs of the batch's frames as strings. Imported frames are named `Section - <label> (Plotwork)`. The script gives each one its label, and returns the label with the ID, so you match each screen to its frame **by name**:

   ```js
   const ids = [/* the nodeIds from the upload's answer, as strings */];
   const out = [];
   for (const id of ids) {
     const node = await figma.getNodeByIdAsync(id);
     if (!node) { out.push({ id, error: "not found" }); continue; }
     const m = node.name.match(/^Section - (.*) \(Plotwork\)$/);
     const label = m ? m[1] : node.name;
     node.name = label;
     out.push({ id, name: label });
   }
   return out;
   ```

   A screen whose label comes back is done: its frame is that ID. A screen whose label doesn't come back failed.
6. **If an upload fails** (the import call gave an address, but the upload didn't finish), the address is single-use, and the frames may have arrived anyway. First list the page's frames with this script (if Figma says a limit was reached, don't: see the rule at the top of this part):

   ```js
   const page = await figma.getNodeByIdAsync("<pageId>");
   await page.loadAsync();
   return page.children.map(c => ({ id: c.id, name: c.name }));
   ```

   - **The listing fails:** mark the batch's screens as failed. **Never import that batch again**: its frames may be there already.
   - **The batch's frames are there** (named `Section - <label> (Plotwork)` or already `<label>`): treat them as sent, and rename them as in step 5. A label that is missing is a failed screen.
   - **None of them is there:** make a **new** import call, and upload once more. If that fails too, mark the batch's screens as failed and carry on.
7. **If every batch failed or was not sent,** remove the page you created, only if it is still empty (when a limit was reached, make no call: the page stays, and the final message says that it is empty):

   ```js
   const page = await figma.getNodeByIdAsync("<pageId>");
   if (!page) return "not found";
   await page.loadAsync();
   if (page.children.length === 0) { page.remove(); return "removed"; }
   return "kept";
   ```

   Say so in the final message.
8. **Delete the run folder.**

## E. Link the screens back

A screen **failed** if its batch failed, the agent couldn't write it, or its label didn't come back. A screen was **not sent** if a limit stopped the run before it was done (see the rule at the top of part D). Either keeps its previous links, in the inventory and in the `design` field, and its *Figma* cell as it was. Never blank them.

- **A frame's link:** the `fileUrl` kept in part D, without anything from its `?` on, plus `?node-id=<frame ID with ":" written as "-">`. **The page's link** is built the same way from the page's ID.
- **The inventory:**
  - fill the *Figma* column of each screen sent as `[frame](<link>) SRC-n`, with two links for "both" (`[desktop](<link>) [mobile](<link>) SRC-n`). `SRC-n` is the version of the external prototype the frames were rebuilt from: the one in the header's *External prototype* line now. The new cell replaces the old one, so a rebuilt screen is no longer stale;
  - a screen whose frame is out of date, and that this run doesn't rebuild, is marked `[frame](<link>) SRC-n · stale`, keeping its old `SRC-n` (the calling skill says when);
  - add the page to the *Figma pages* row at the top, only if at least one screen was linked to it: never record a page that part D, step 7 removed, or a page left empty after a limit (the final message says it is empty and can be deleted).
- **The breakdown,** when the calling skill says to. The `design` key holds the screens of an item as `"<label> — <Figma frame link>"`, one per frame, with the label exactly as in part C:
  - **a Feature** (Basic: an Epic) gets the screens whose *Features* cell names it, and only those. An inventory made before the *Features* column existed has none: add the column first, naming for each screen the Features whose own scope includes it (not every Feature that shares one of its needs), and use it.;
  - **an Epic** (Agile, Scrum, CMMI) gets the union of its Features' screens, in order, without duplicates.

  Run, for every item whose screens changed:

  ```bash
  python "<shared>/scripts/set_design_links.py" docs/planning/work-breakdown.yaml '<DRAFT-ID>=<label>|<link>' ...
  ```

  **Put each argument in single quotes, never double quotes.** Inside double quotes the shell changes text: `$toolId` in a screen's address becomes nothing, and `$(…)` or backticks in a screen's name would run a command. Inside single quotes the text stays exactly as written. A `'` inside the text would end the quoting, so write each one as `'\''` (close the quote, an escaped apostrophe, open the quote again): `'TSH-FT-001=Owner'\''s tools — /owner|https://…'`.

  To remove an item's `design` field (it has no screens left), give its ID with nothing after `=`: `'TSH-FT-003='`.

  Give **every** screen of each item named, not only the new ones: the new links for the screens just rebuilt, and the existing ones from the inventory for the rest. The script replaces that item's whole `design` list. It changes nothing else, checks this before writing, and writes nothing on exit 1.

  **On exit 1 (or 2):** the YAML stays as it is. Keep the links in the inventory, and list the items that failed in the final message.
- **The final message** gives the page's link, and lists:
  - the screens that failed and why. Those that were rebuilt before are still on the older page;
  - the screens **not sent**, when a limit stopped the run, and that a later `/plotwork:from-app <folder> --figma <URL> --figma-only` sends only those, and any screen with no frame or a stale one;
  - the items whose `design` field changed, and those the script could not change;
  - when the plan has needs that came only from documents (a file of changes, or documents found in the external prototype), not from the code: "Needs that came only from documents are not on the frames.";
  - this sentence: "These screens are rebuilt from the code, not captured from the running prototype. The functional team should compare them with it before they become the design reference."
