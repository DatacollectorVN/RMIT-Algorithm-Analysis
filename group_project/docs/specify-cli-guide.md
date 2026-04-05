# Specify (Spec Kit) — team guide

This folder (`group_project/`) is a **Specify** project: spec-driven workflows with templates under `.specify/` and Cursor commands under `.cursor/commands/`. The **`specify`** CLI scaffolds and maintains that layout; day-to-day feature work uses **Cursor slash commands** (or the same flows in another supported agent).

---

## 1. Install the CLI

Pick one:

```bash
# Recommended (isolated tool install)
uv tool install specify-cli

# Upgrade later
uv tool install specify-cli --upgrade
```

Other options are documented in the [Spec Kit installation guide](https://github.github.com/spec-kit/installation.html).

Check it works:

```bash
specify --help
specify version
```

---

## 2. Commands overview

| Command | Purpose |
|--------|---------|
| `specify init` | Create or refresh Specify scaffolding (`.specify/`, agent commands, optional git). |
| `specify check` | Verify required tools on your machine. |
| `specify version` | Show CLI and environment info. |
| `specify extension` | Add/remove/update **extensions** from catalogs (`list`, `add`, `search`, …). |
| `specify preset` | Add/remove **presets** (curated template packs) (`list`, `add`, `search`, …). |

Use `--help` on any command or subcommand, e.g. `specify init --help`, `specify extension add --help`.

---

## 3. `specify init` — when you need it

Use **`specify init`** when:

- You are **creating a new** Specify project, or
- You want to **re-run setup** in an existing directory (merge/update; use `--here` and read prompts carefully).

### This repo’s setup

`group_project/.specify/init-options.json` records how this tree was initialized, for example:

- **AI**: `cursor-agent` (Cursor)
- **Scripts**: `sh` (Bash under `.specify/scripts/bash/`)
- **`--here`**: initialized in the current directory (not a new subfolder)

New teammates usually **clone the repo** and do **not** need to run `init` again unless you are fixing a broken or partial install.

### Fresh init examples (reference)

```bash
# New folder
specify init my-app --ai cursor-agent

# Current directory (like this group project)
specify init --here --ai cursor-agent

# No network / GitHub release has no ZIP assets — use bundled templates
specify init --here --ai cursor-agent --offline
```

Useful flags:

| Flag | Meaning |
|------|---------|
| `--ai <agent>` | Target assistant (`cursor-agent`, `claude`, `copilot`, …). |
| `--here` | Initialize in the current directory. |
| `--offline` | Use templates **bundled inside** `specify-cli` (no GitHub download). Use this if init fails with “No matching release asset…”. |
| `--force` | With `--here`, skip the “directory not empty” confirmation. |
| `--no-git` | Do not create or touch a git repo. |
| `--script sh\|ps` | Bash vs PowerShell scripts. |
| `--ignore-agent-tools` | Skip checks for external CLIs (e.g. Claude Code). |
| `--preset <id>` | Apply a catalog preset during init. |

After init, open the project in **Cursor** so `.cursor/commands/` is picked up.

---

## 4. Working in Cursor (daily workflow)

In Chat or Agent, use the **Spec Kit** slash commands (files in `.cursor/commands/`). Typical flow:

1. **`/speckit.specify`** — Turn a short feature description into a spec (creates/updates feature branch and spec artifacts per the command instructions).
2. **`/speckit.plan`** — Technical plan from the spec.
3. **`/speckit.tasks`** — Task breakdown.
4. **`/speckit.implement`** — Implementation pass against tasks.
5. **`/speckit.analyze`**, **`/speckit.clarify`**, **`/speckit.checklist`**, **`/speckit.constitution`** — As needed for quality and governance.

Each command file describes what the agent must do (prerequisites, scripts to run, handoffs). Prefer following that order unless your instructor says otherwise.

### Shell helpers (optional)

Scripts live under `.specify/scripts/bash/` (on macOS/Linux). Examples:

- `create-new-feature.sh` — New feature branch + scaffold paths (often invoked from slash-command instructions).
- `check-prerequisites.sh` — Environment checks.
- `setup-plan.sh`, `update-agent-context.sh` — Plan/context updates.

If a slash command tells you to run a script, run it from the **repository root** (or as documented in that command file).

---

## 5. Extensions and presets

- **`specify extension search`** / **`specify extension add`** — Optional add-ons (see `specify extension --help`).
- **`specify preset search`** / **`specify preset add`** — Curated packs for domains or stacks (see `specify preset --help`).

These are optional for coursework unless the brief requires them.

---

## 6. Troubleshooting

| Issue | What to try |
|-------|-------------|
| **“No matching release asset…”** on `specify init` | Run init with **`--offline`**, or **upgrade** the CLI: `uv tool install specify-cli --upgrade`. |
| **GitHub API rate limit** | Set `GH_TOKEN` or `GITHUB_TOKEN` for higher limits (if your CLI version still uses the GitHub download path). |
| **Slash command missing in Cursor** | Ensure you opened the **`group_project`** folder (or repo root that contains `.cursor/commands/`). Reload the window if needed. |
| **Wrong branch / numbering** | Check `branch_numbering` in `.specify/init-options.json` (`sequential` vs `timestamp`) and follow the slash command’s script examples. |

---

## 7. Official references

- [github/spec-kit](https://github.com/github/spec-kit) — Source and releases.
- [Spec Kit documentation](https://github.github.com/spec-kit/) — Install, upgrade, concepts.

For the exact behavior of this CLI build, prefer **`specify <command> --help`** on your machine.
