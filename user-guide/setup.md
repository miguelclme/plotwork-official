# Setup

How to install everything Plotwork uses: the plugin, Python, and the Azure DevOps and Figma servers. It is the one technical page of the user guide. If you are not technical, send it to someone in your IT team: each step is written to be followed as it is.

Back to the [user guide](README.md).

## What is needed for what

| Piece | Needed for | Without it |
|---|---|---|
| Claude Code (CLI, desktop app or IDE extension) | Everything | Nothing runs |
| The Plotwork plugin | Everything | The `/plotwork:` commands don't exist |
| Python (tested with 3.14) | The checks, the review page, writing ADO IDs and Figma links, file fingerprints | Claude runs the checks by hand and writes the review page from its template, marked "rendered manually". The push needs Python |
| PyYAML (a Python package) | Nothing. Optional | The scripts use their own reader for the YAML the template uses |
| Node.js 20 or newer | Microsoft's local Azure DevOps MCP server | No push |
| An Azure DevOps MCP server | `/plotwork:push` only | The push says one is needed, and stops |
| Figma's remote MCP server | `--figma` only | `from-app` and `from-app-update` stop before reading anything, when `--figma` is given |

An **MCP server** (Model Context Protocol server) is a small program that gives Claude tools to talk to another system, such as Azure DevOps or Figma. Claude Code starts and manages it.

## Install the plugin

The repository is its own marketplace (a list of plugins Claude Code can install), named `plotwork`. So the install ID is `plotwork@plotwork`.

```bash
claude plugin marketplace add miguelclme/plotwork-official
```

```bash
claude plugin install plotwork@plotwork
```

Inside a Claude Code session, the same commands are `/plugin marketplace add miguelclme/plotwork-official` and `/plugin install plotwork@plotwork`.

**Start a new session** afterwards. Skills load when a session starts.

| To | Run |
|---|---|
| Update | `claude plugin marketplace update plotwork`, then `claude plugin update plotwork`, then start a new session |
| Check it is installed and on | `claude plugin list` |
| Turn it on | `claude plugin enable plotwork` |
| Turn it off (its skill descriptions cost tokens in every session) | `claude plugin disable plotwork` |
| Remove it | `claude plugin uninstall plotwork`. Users' files in `docs/planning/` are never touched |
| See its token cost | `claude plugin details plotwork` |

## Python

Install Python 3.14 from [python.org](https://www.python.org/downloads/) or your system's package manager. Make sure `python` (or `python3`) works in a terminal, then start a new Claude Code session.

The scripts use only the standard library. PyYAML is optional: when it is installed, the scripts use it.

## Azure DevOps

Plotwork uses Microsoft's **local** Azure DevOps MCP server, [`@azure-devops/mcp`](https://github.com/microsoft/azure-devops-mcp). It runs on your computer through `npx` and needs **Node.js 20 or newer** ([nodejs.org](https://nodejs.org/)). Other Azure DevOps servers, Microsoft's hosted one included, are untested. The push still accepts any server whose tools match.

In the commands below, replace `<organization>` with your organization's name: the part after `dev.azure.com/`. `--scope user` makes the server available in every folder you open Claude Code in, and keeps any token out of the repository.

### Sign in with a browser

This is Microsoft's default. The first time a tool is used, a browser opens, and you sign in with an account that has access to the organization.

```bash
claude mcp add azure-devops --scope user -- npx -y @azure-devops/mcp <organization>
```

### Sign in with a personal access token (PAT)

Use this when your company blocks browser sign-in.

1. In Azure DevOps, open **User settings → Personal access tokens**. Create a token for the organization with the scopes **Work Items: Read & write** and **Project and Team: Read**.
2. The server doesn't take the token as it is. It takes the base64 of `<email>:<token>` (any email works). Make it in PowerShell:

   ```powershell
   [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes('me@example.com:<token>'))
   ```

   or in bash: `printf '%s' 'me@example.com:<token>' | base64 | tr -d '\n'`. Without `tr`, some systems split the result over two lines.
3. Add the server, with the result in place of `<base64>`:

   ```bash
   claude mcp add azure-devops --scope user -e PERSONAL_ACCESS_TOKEN=<base64> -- npx -y @azure-devops/mcp <organization> --authentication pat
   ```

The token is saved in your own Claude Code settings (`~/.claude.json`), not in the project. **Never add it with `--scope project`,** which writes it into the repository's `.mcp.json`. When the token expires, remove the server and add it again with a new token:

```bash
claude mcp remove azure-devops --scope user
```

Microsoft's [getting-started page](https://github.com/microsoft/azure-devops-mcp/blob/main/docs/GETTINGSTARTED.md) lists the other sign-in methods, such as the Azure CLI.

### Check it

```bash
claude mcp list
```

The server must show as **Connected**. Then start a new Claude Code session.

### More than one organization

Add one server per organization, each under its own name:

```bash
claude mcp add ado-personal --scope user -- npx -y @azure-devops/mcp <personal organization>
```

With more than one connected, the push needs `--mcp <name>`, the name `claude mcp list` shows. Without it, the push stops before calling Azure DevOps, and prints the command to run for each server.

### What the project needs

- It must exist. The push needs its exact name.
- It must use the same process as the breakdown (Basic, Agile, Scrum or CMMI). The push checks the work-item types to confirm it.
- The account must be allowed to create work items.
- Any area path used with `--area` must already exist (**Project settings → Boards → Project configuration → Areas**). Plotwork never creates areas or iterations.

## Figma

`--figma` needs **Figma's remote MCP server**, because it imports HTML. Figma's desktop server can't do that.

- Connect it as Figma's own instructions say, or install a Figma connector from the Claude marketplace. A connector's server name can be an ID: that is fine, the user never types it.
- The first `--figma` run finds the server, asks the user to confirm it, and saves its name in `~/.plotwork/figma-server.txt`. That file is shared by every project.
- After "yes figma", Plotwork confirms the server by calling its account tool (`whoami`), and uses only three of its tools: the account tool, the HTML import (`html_to_figma`) and the script tool (`use_figma`).
- The user needs a Figma **design file** they can edit. Figma imports screens only into design files, not FigJam boards, Slides or Make files. Plotwork never creates a file.
- `curl` must be available: the HTML is uploaded with it, to a `figma.com` address the import call returns.

## Technical troubleshooting

| Problem | Fix |
|---|---|
| "Unknown command" for `/plotwork:...` | The session started before the install, or the plugin is off. Check `claude plugin list`, run `claude plugin enable plotwork` if needed, and start a new session |
| Claude says Python isn't available | Install Python 3.14, check `python` or `python3` works in a terminal, start a new session, then ask Claude to "validate and re-render the breakdown" |
| No Azure DevOps server found | Add one (above), check `claude mcp list`, start a new session. A server added without `--scope user` works only in the folder it was added from |
| Azure DevOps answers 401 or 403 | The PAT expired, lacks a scope, or wasn't base64-encoded as `<email>:<token>`. Make a new one and add the server again |
| More than one Azure DevOps server | Run the push with `--mcp <name>`. The push's message gives the command for each server |
| The Figma server can't import screens | It is probably Figma's desktop server. Connect the remote one |
