---
description: Reconcile feature artifacts (spec, plan, tasks, contracts, quickstart) with code or design changes the user already made—or with explicit edits they describe.
handoffs:
  - label: Regenerate Tasks
    agent: speckit.tasks
    prompt: Regenerate or extend tasks.md after spec/plan changes from /speckit.refine
  - label: Technical Plan Refresh
    agent: speckit.plan
    prompt: Refresh plan.md if architecture shifted during refine
  - label: Consistency Check
    agent: speckit.analyze
    prompt: Run cross-artifact analysis after refine edits
---

## User Input

```text
$ARGUMENTS
```

You **MUST** treat the user input as the **refine brief**: what changed (paths, behavior, task IDs, new flags, API shape) and which artifacts to prioritize. If empty, infer scope from **git diff**, **recently edited files**, or **open editors** when available; otherwise ask one short clarifying question (feature folder + what diverged).

## Goal

Keep **spec-driven truth** aligned with **reality**: after the user edits code, CLI, tests, or manually tweaks a task, update the minimum set of Spec Kit files so teammates and future `/speckit.implement` runs see accurate requirements and checklists.

This command **does edit files** (unlike `/speckit.analyze`, which is read-only).

## Operating Constraints

- **Constitution**: `.specify/memory/constitution.md` remains authoritative. Do not “relax” MUST rules in specs/plans to match code—either document a justified exception in `plan.md` **Complexity Tracking** or fix the code.
- **Scope**: Prefer **surgical** edits (single sections, one FR, one contract table) over rewriting entire specs unless the user asks for a full resync.
- **Paths**: Use `group_project/` as the app root when resolving `src/`, `tests/`, and `specs/NNN-feature/`.

## Pre-Execution Checks

**Extension hooks** (`.specify/extensions.yml`): if present, apply `hooks.before_implement`-style handling only if the file defines `hooks.before_refine`; otherwise skip silently (same pattern as other speckit commands).

## Execution Steps

### 1. Resolve feature context

From **repo root** (`group_project/` or monorepo root as applicable):

1. Run `.specify/scripts/bash/check-prerequisites.sh --json --paths-only` (or `--json --include-tasks` if you need `tasks.md` in `AVAILABLE_DOCS` for validation).

2. Parse JSON for at least: `FEATURE_DIR`, `FEATURE_SPEC`, `IMPL_PLAN`, and `TASKS` if returned.

3. If the user named a feature in `$ARGUMENTS` (e.g. `002-two-phase-cli`), set `SPECIFY_FEATURE=<branch-or-folder-name>` and re-run the script, or construct `FEATURE_DIR` as `specs/<id>-<short-name>/` when unambiguous.

Abort with a clear message if `spec.md` is missing.

### 2. Establish the delta

Using **user input** + **optional** `git diff` / file reads:

- **Code delta**: Which modules, public CLI argv, JSON schemas, or tests changed?
- **Intent delta**: New behavior, renamed flags, removed tasks, deferred scope?
- **Artifact delta**: User says “task T010 is done” or “plan section X is wrong”.

Produce a short internal bullet list: *was → now* for each item to fix in docs.

### 3. Update artifacts (priority order)

Apply edits **only where the delta requires it**. Typical mapping:

| Change type | Likely touch |
|-------------|----------------|
| User-visible behavior, FR, acceptance | `spec.md` (FR, user stories, edge cases, SC if measurable outcomes shift) |
| How we build it, stack, file layout | `plan.md` (Summary, Technical Context, Project Structure) |
| Step breakdown, done/pending, new work | `tasks.md` (checkboxes, descriptions, new T### IDs if needed) |
| CLI / file format contracts | `contracts/*`, `quickstart.md` |
| Entities / validation rules | `data-model.md` |
| Prior decision overturned | `research.md` (new Decision / Rationale block) |

**Tasks file**: If implementation matches a task, set `- [x]` and keep IDs stable. If the user added work not in `tasks.md`, append tasks with the next IDs; do not renumber completed work.

**Checklists**: Update `FEATURE_DIR/checklists/*.md` only when spec changes invalidate prior checklist notes—either refresh the Notes section or tick items to reflect new validation status.

### 4. Consistency pass

- Ensure **terminology** matches across `spec.md`, `plan.md`, `contracts/`, and `quickstart.md` (e.g. same subcommand names, flag spellings).
- Ensure **FR / SC** in `spec.md` remain testable and not contradicted by `plan.md`.
- If the delta is large or ambiguous, append a **“Refine log”** bullet list to `plan.md` or the spec **Assumptions** (one line per refine session with date) so history is clear.

### 5. Optional agent context

If `plan.md` or stack summary changed materially, run:

`bash .specify/scripts/bash/update-agent-context.sh cursor-agent`

with `SPECIFY_FEATURE` set to the active feature when required by the script.

### 6. Report

Return a concise summary:

- Feature directory
- Files modified (paths)
- Notable spec/FR/contract updates
- Open follow-ups (e.g. “run `/speckit.tasks` to split new work into tasks”)

## When to suggest handoffs

- **Many new tasks or re-phased work** → suggest `/speckit.tasks`.
- **Architecture or research decisions changed** → suggest `/speckit.plan` (or manual plan section edits you already did + quick review).
- **User wants verification only** → suggest `/speckit.analyze` after refine.

## Quick usage examples (for the user)

```text
/speckit.refine Updated main.py: search subcommand now accepts --json-out; sync spec + contracts + tasks T010–T012
```

```text
/speckit.refine Feature 002: mark T008–T009 done; plan still mentions flat flags—fix plan and quickstart only
```

```text
/speckit.refine Read git diff and align spec/plan with whatever changed under src/ and tests/
```

## Post-execution hooks

If `.specify/extensions.yml` defines `hooks.after_refine`, output optional/mandatory hook blocks per the same rules as other speckit commands; otherwise skip silently.
