# Implementation Plan: Two-Phase CLI (Subcommands: generate-corpus / search)

**Branch**: `002-two-phase-cli` | **Date**: 2026-04-05 | **Spec**: [spec.md](./spec.md)  
**Input**: Feature specification from `/specs/002-two-phase-cli/spec.md`

## Summary

Refactor the CLI to use **`argparse` subparsers**: **`generate-corpus`** requires **`--N`** (integer ≥ 1) and optional **`--seed`**. It writes **`corpus.json`** (JSON array, `load_corpus_json`-compatible) and **`metadata.txt`** (`N=` / `seed=` lines) under **`<cwd>/.rmit/corpus/YYYYMMDD_HHMMSS/`**, creates directories as needed, and prints **absolute paths** for those two files on stdout (not the JSON body). **`search`** requires `--corpus` and `--query`, optional `--strategy` and **`--benchmark`**, then runs top-k retrieval unchanged in semantics vs the pre-subcommand engine for the same files. Document **`uv run python src/main.py <subcommand> …`** as an example; keep **`PYTHONPATH` including `src`** (no `sys.path` mutation). Implement **`get_synthetic_corpus`** / **`get_synthetic_query`** for the search path only. Tests use a temp cwd to isolate **`.rmit/`** output.

## Technical Context

**Language/Version**: Python 3.12+  
**Primary Dependencies**: **None (stdlib only)** per `.specify/memory/constitution.md` — no PyPI/third-party packages  
**Storage**: UTF-8 JSON on disk; **generate-corpus** persists under **`.rmit/corpus/<timestamp>/`**; **search** reads user-supplied corpus/query paths; **search** stdout is JSON results  
**Testing**: **`unittest` (stdlib)** — no pytest or other third-party test runners  
**Target Platform**: macOS/Linux (developer CLI); portable stdlib only  
**Project Type**: single-package CLI + library modules under `src/services/`  
**CLI parsing**: **`argparse` subparsers** for `generate-corpus` and `search` (no third-party CLI libraries)  
**Performance Goals**: Same as feature 001 — acceptable interactive use on 100k+ profiles; generation uses iterator then writes one **`corpus.json`** via `dump_json` (memory profile unchanged vs streaming stdout)  
**Constraints**: No `sys.path` hacks; strict typing; domain errors via `services.core.exceptions`  
**Scale/Scope**: `src/main.py` refactor + `tests/test_main.py` + feature docs (`contracts/`, `quickstart.md`, this plan, `research.md`)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Verify against `.specify/memory/constitution.md` (RMIT group project):

- [x] **Standard Library First**: Subparsers via stdlib `argparse` only; no new PyPI deps.
- [x] **PEP 8 & type hints**: `run()` / subcommand handlers and `get_synthetic_corpus` / `get_synthetic_query` fully typed and documented.
- [x] **Functional-first modularity**: Search path composes existing `jsonio`, `pipeline`, strategies; no new global mutable state.
- [x] **Complexity & memory**: Unchanged asymptotics vs 001 for generation and search.
- [x] **Documentation**: Google-style docstrings; per-subcommand `--help` text.
- [x] **Errors**: `ValidationError` for JSON/schema; `SystemExit` with clear messages for usage mistakes.
- [x] **Testing**: `unittest` only; argv lists include subcommand as first token.

## Project Structure

### Documentation (this feature)

```text
specs/002-two-phase-cli/
├── plan.md              # This file
├── research.md          # Phase 0 (CLI shape revised for subcommands)
├── data-model.md        # Phase 1
├── quickstart.md        # Phase 1 (uv + subcommand examples)
├── contracts/
│   └── cli-invocation.md
└── checklists/
    └── requirements.md
```

### Source Code (repository root)

```text
group_project/
├── src/
│   ├── main.py                 # CLI: subparsers generate-corpus / search + helpers
│   └── services/
│       └── …                   # unchanged services layer
└── tests/
    └── test_main.py            # argv: ["generate-corpus", "--N", …] etc.
```

**Structure Decision**: Single project; behavioral change in `main.py` and tests only.

## Complexity Tracking

No constitution violations; table not used.

## Phase 0: Research

See [research.md](./research.md). **Update**: §1 now selects **subparsers** (revises earlier flat-flag decision).

## Phase 1: Design & Contracts

- [data-model.md](./data-model.md) — entities + subcommand-scoped validation rules  
- [contracts/cli-invocation.md](./contracts/cli-invocation.md) — subcommand argv contract  
- [quickstart.md](./quickstart.md) — `uv run` and plain `python` examples  

## Post-Design Constitution Check

Re-verified after subcommand plan: stdlib-only, unittest, typing, and complexity assumptions hold.

## Refine log

- **2026-04-06** (`/speckit.refine`): **`generate-corpus`** implementation now writes **`./.rmit/corpus/YYYYMMDD_HHMMSS/corpus.json`** + **`metadata.txt`** and prints absolute **Corpus:** / **Metadata:** paths on stdout; **`--count`** removed from parser (only **`--N`**). Plan/tasks/contracts/quickstart/spec adjusted to match [`src/main.py`](../../src/main.py).
