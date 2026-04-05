---
description: "Task list for 002-two-phase-cli (generate vs search CLI)"
---

# Tasks: Two-Phase CLI (Generate vs Search)

**Input**: Design documents from `/specs/002-two-phase-cli/`  
**Prerequisites**: [plan.md](./plan.md), [spec.md](./spec.md), [contracts/cli-invocation.md](./contracts/cli-invocation.md), [research.md](./research.md)  
**Tests**: **Required** — spec FR-006 mandates automated coverage for generation-only, search-only, and conflicting invocations.

**Organization**: remove bootstrap → **generate-corpus subcommand (US1)** → **search subcommand (US2)** → **usage errors (US3)** → polish. **Stdlib only** — no PyPI/runtime dependencies ([`.specify/memory/constitution.md`](../../.specify/memory/constitution.md)).

**Amendment (2026-04-05)**: Subcommand CLI in `main.py` / `test_main.py` per [contracts/cli-invocation.md](./contracts/cli-invocation.md). **Refine (2026-04-06)**: `generate-corpus` writes **`.rmit/corpus/<stamp>/corpus.json`** + **`metadata.txt`**, prints paths on stdout; **`--count`** dropped ( **`--N`** only).

**Related system (001)**: Data generation at scale, normalization, baseline scan, k-d tree, and benchmarking already live under `src/services/similarity/` and `src/services/search/`. This feature only changes the **CLI** and adds **`tests/test_main.py`**; do not re-implement 001 algorithms here.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no blocking dependency on incomplete sibling tasks)
- **[Story]**: User story label from [spec.md](./spec.md) (`US1`, `US2`, `US3`)

## Path Conventions

- Application root: `group_project/`
- Source: `group_project/src/`
- Tests: `group_project/tests/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Align with contracts before code changes.

- [x] T001 Review [contracts/cli-invocation.md](./contracts/cli-invocation.md) and [quickstart.md](./quickstart.md) for flag matrix and PYTHONPATH invocation

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Import hygiene and argparse shape so both modes can be wired without `sys.path` hacks.

**⚠️ CRITICAL**: Complete before User Story phases.

- [x] T002 Remove `sys.path` insertion block and unused imports tied only to that block from `group_project/src/main.py` (imports MUST resolve with `PYTHONPATH` including `group_project/src` per spec)
- [x] T003 Change `--query` in `group_project/src/main.py` from `required=True` to optional; add a short module docstring note that `--query` is required only in search mode

**Checkpoint**: `python src/main.py --help` (and per-subcommand `--help` after T016) runs under `PYTHONPATH=$(pwd)/src` without import errors.

---

## Phase 3: User Story 1 — Generate synthetic corpus only (Priority: P1) 🎯 MVP

**Goal**: Subcommand **`generate-corpus`** with required **`--N`** and optional **`--seed`** writes **`corpus.json`** + **`metadata.txt`** under **`<cwd>/.rmit/corpus/YYYYMMDD_HHMMSS/`** and prints absolute paths on stdout (two lines: **Corpus:** / **Metadata:**). No JSON corpus body on stdout.

**Independent Test**: From a temp cwd, `python src/main.py generate-corpus --N 10 --seed 1` → exit 0; **`.rmit/corpus/<stamp>/corpus.json`** parses as JSON array length 10; **metadata.txt** matches `N` / `seed`; stdout mentions both file paths.

### Tests for User Story 1

- [x] T004 [US1] `group_project/tests/test_main.py` — `generate-corpus` with **`--N`**, chdir temp dir, asserts **`.rmit/corpus/`** layout, **corpus.json** schema, **metadata.txt**, path lines on stdout, determinism via file contents.

### Implementation for User Story 1

- [x] T005 [US1] Subparser **`generate-corpus`** in `group_project/src/main.py` + `iter_synthetic_profiles` + `dump_json` **written to disk** + **metadata.txt** + **mkdir** under **`.rmit/corpus/<stamp>/`**.
- [x] T006 [US1] Subparser-scoped options (**`--N`** required) + **N ≥ 1** in `_run_generate_corpus`; search-only flags rejected by argparse.

**Checkpoint**: Tests + impl match [contracts/cli-invocation.md](./contracts/cli-invocation.md) **generate-corpus** section.

---

## Phase 4: User Story 2 — Search on a prepared corpus (Priority: P1)

**Goal**: Subcommand **`search`** requires `--corpus` and `--query`; uses `get_synthetic_corpus` and `get_synthetic_query`; preserves search JSON and ranking semantics for equivalent inputs (SC-003).

**Independent Test**: `python src/main.py search --corpus … --query … --strategy baseline` with temp JSON files.

### Tests for User Story 2

- [x] T007 [US2] `test_search_baseline_returns_hits` in `group_project/tests/test_main.py`

### Implementation for User Story 2

- [x] T008 [US2] `get_synthetic_corpus` in `group_project/src/main.py`
- [x] T009 [US2] `get_synthetic_query` in `group_project/src/main.py`
- [x] T010 [US2] **`search`** subparser + `_run_search` using helpers

**Checkpoint**: Search tests pass; preparation uses the two helpers only.

---

## Phase 5: User Story 3 — Clear separation and errors between modes (Priority: P2)

**Goal**: Missing / unknown subcommand and missing required options produce explicit errors (FR-003, FR-004).

**Independent Test**: No subcommand, unknown subcommand, `search` without `--corpus` or `--query` → non-zero exit and readable message.

### Tests for User Story 3

- [x] T011 [US3] `TestMainUsage` in `group_project/tests/test_main.py`

### Implementation for User Story 3

- [x] T012 [US3] `_build_parser()` with `required=True` subparsers + argparse errors for missing options

**Checkpoint**: FR-006 satisfied; all `test_main` cases green.

---

## Phase 3b: Subcommand migration (amendment)

**Purpose**: Align implemented flat-flag CLI with amended spec/contract.

- [x] T016 Subparsers `generate-corpus` / `search` in `group_project/src/main.py`
- [x] T017 `group_project/tests/test_main.py` subcommand argv (**`--count`** synonym **removed** in code; tests use **`--N`** only)
- [x] T018 Flat-flag helpers removed; `get_synthetic_corpus` / `get_synthetic_query` on search path only

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Docs and full-suite verification.

- [x] T013 [P] See §8 in `group_project/docs/specify-cli-guide.md` (subcommand recipes + `PYTHONPATH`)
- [x] T014 [P] `group_project/.cursor/rules/specify-rules.mdc` already lists subcommands / `uv run`
- [x] T015 Full `unittest` discover run green (2026-04-06)
- [x] T019 [P] `group_project/.gitignore` — ignore `.rmit/corpus/` (generated timestamped runs)
- [x] T020 [US2] `test_main.py` — `search --benchmark` timing keys; `search --strategy kdtree`; E2E `generate-corpus` → `search` on written `corpus.json`

---

## Dependencies & Execution Order

### Phase Dependencies

| Phase | Depends on | Notes |
|-------|------------|--------|
| Phase 1 Setup | — | |
| Phase 2 Foundational | Phase 1 | Blocks all stories |
| Phase 3 US1 | Phase 2 | MVP: shippable generate-only CLI |
| Phase 4 US2 | Phase 2, Phase 3* | *Search can be coded after Phase 2 alone, but recommended after US1 to keep “generate first” integration mindset |
| Phase 5 US3 | Phases 3–4 | Hardens validation once both modes exist |
| Phase 6 Polish | Phases 3–5 | |

### User Story Dependencies

- **US1**: After Foundational — no dependency on US2/US3.
- **US2**: After Foundational; logically follows US1 in this roadmap; uses helpers required by spec.
- **US3**: After US1 and US2 so validation covers real code paths.

### Parallel Opportunities

- **T004**, **T007**, and **T011** all extend `group_project/tests/test_main.py` — execute **sequentially** or combine in one edit pass per developer preference; optional split into `tests/test_main_search.py` is not required by this list.
- **T013** and **T014** can run in parallel (different files).
- **T008** and **T009** both touch `group_project/src/main.py` — **not** parallel; do T008 then T009 or combine in one edit.

### Parallel Example: Polish

```bash
# After US1–US3 complete:
# Developer A: T013 docs/specify-cli-guide.md
# Developer B: T014 .cursor/rules/specify-rules.mdc
# Then: T015 full unittest discover
```

---

## Implementation Strategy

### MVP First (User Story 1 only)

1. Complete Phase 1–2  
2. Complete Phase 3 (US1) + T004–T006  
3. **STOP**: validate generation-only per [quickstart.md](./quickstart.md) process 1  

### Full feature (recommended order)

1. Phase 1–2 → import/argparse foundation  
2. Phase 3 → synthetic corpus generation  
3. Phase 4 → search with `get_synthetic_corpus` / `get_synthetic_query`  
4. Phase 5 → conflict and missing-argument handling + tests  
5. Phase 6 → documentation + full suite  

---

## Notes

- Total tasks: **20** (T001–T015 + **T016–T018** migration + **T019–T020** Phase 6 verification).
- Task count by story: **US1** — T004–T006 (3); **US2** — T007–T010, T020 (5); **US3** — T011–T012 (2); Setup/Foundational/Polish — T001–T003, T013–T015, T019 (7); **Migration** — T016–T018 (3).
- Every implementation task names **`group_project/src/main.py`** or **`group_project/tests/test_main.py`** (or docs paths) for LLM executability.
- Format validation: all tasks use `- [ ]`, sequential **T###** IDs, optional **[P]**, **[US#]** only on story-phase tasks, and explicit file paths.
