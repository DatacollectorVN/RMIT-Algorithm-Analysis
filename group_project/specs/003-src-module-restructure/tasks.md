---
description: "Task list for 003-src-module-restructure (DTO, helper, dataset, flat jsonio)"
---

# Tasks: Source layout consolidation (003)

**Input**: Design documents from `/specs/003-src-module-restructure/`  
**Prerequisites**: [plan.md](./plan.md), [spec.md](./spec.md), [data-model.md](./data-model.md), [research.md](./research.md), [contracts/public-imports.md](./contracts/public-imports.md), [quickstart.md](./quickstart.md)  
**Tests**: **Required** — [spec.md](./spec.md) FR-006 / SC-001 mandate full `unittest` suite green after refactor.

**Organization**: Setup → inventory → **US1** DTO package → **US2** merge `core` into `helper` → **US4** flat `jsonio` (after US1+US2 so `jsonio` does not depend on `pipeline`) → **US3** `dataset` + `DataBuilder` + remove `similarity` + rewire `search`/`main`/tests → polish → **US5** (amendment) **`Corpuses`** aggregate + **`BaselineSearcher`** / **`KDTreeSearcher`** → **US6** (amendment) **`Corpuses`** class methods + **`dataset`** load aliases + **`hits_equal`**. **Stdlib only** — [`.specify/memory/constitution.md`](../../.specify/memory/constitution.md).

**Amendment (search API)**: Replace `DataBuilder` with **`Corpuses`** (immutable bundle of normalized corpus + `ScalingStats`); strategies take **`Corpuses`** at construction instead of a separate `build(corpus)` step; rename **`BaselineScanner` → `BaselineSearcher`**, **`KDTreeOptimizer` → `KDTreeSearcher`**. CLI flag strings `baseline` / `kdtree` / `both` stay unchanged.

**Amendment (2026-04-06 c)**: Pipeline functions live as **`Corpuses`** static/class methods; **`Corpuses.from_json_path`**, **`Corpuses.load_query`** (and module aliases **`get_synthetic_corpus`** / **`get_synthetic_query`**) replace **`main.py`** helpers; **`hits_equal`** lives in **`helper.py`**.

**Execution note**: Phases **US4** then **US3** in this file reflect **dependency order** (not spec priority P2 vs P3): `jsonio` must import `RawProfile` from `services.dto` before `similarity/pipeline.py` is deleted.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no blocking dependency on incomplete sibling tasks)
- **[Story]**: User story label from [spec.md](./spec.md) (`US1`–`US4`)

## Path Conventions

- Application root: `group_project/`
- Source: `group_project/src/`
- Tests: `group_project/tests/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Baseline and read contracts before edits.

- [x] T001 Review `group_project/specs/003-src-module-restructure/contracts/public-imports.md` and `group_project/specs/003-src-module-restructure/quickstart.md` for canonical import paths post-refactor
- [x] T002 Run baseline verification: `cd group_project && export PYTHONPATH="${PYTHONPATH}:$(pwd)/src" && python -m unittest discover -s tests -p 'test_*.py'` — record exit code 0 before any refactor edits

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Migration inventory; no story work until complete.

- [x] T003 Enumerate all Python files under `group_project/src/` and `group_project/tests/` that reference `services.core`, `services.io`, or `services.similarity.pipeline` (e.g. `rg 'services\.(core|io)|similarity\.pipeline' src tests --glob '*.py'`) and keep the list for T008–T021

**Checkpoint**: List complete; proceed to US1.

---

## Phase 3: User Story 1 — DTO package (Priority: P1) 🎯 MVP

**Goal**: Domain dataclasses (`RawProfile`, `NormalizedProfile`, `ScalingStats`) defined only under `services/dto/`; `pipeline.py` imports them instead of defining duplicates.

**Independent Test**: `grep -R "class RawProfile\\|class NormalizedProfile\\|class ScalingStats" group_project/src/services --include="*.py"` — definitions appear only under `dto/` (not under `similarity/`).

### Implementation for User Story 1

- [x] T004 [US1] Create `group_project/src/services/dto/profiles.py` containing `RawProfile`, `NormalizedProfile`, `ScalingStats` (move verbatim from `group_project/src/services/similarity/pipeline.py`; no business logic in this file)
- [x] T005 [US1] Create `group_project/src/services/dto/__init__.py` re-exporting the three dataclasses with a short package docstring listing the public surface
- [x] T006 [US1] Edit `group_project/src/services/similarity/pipeline.py` to remove the three `@dataclass` blocks and add `from services.dto import NormalizedProfile, RawProfile, ScalingStats` (keep all other pipeline code unchanged for now)

**Checkpoint**: `python -c "from services.dto import RawProfile, NormalizedProfile, ScalingStats"` with `PYTHONPATH=group_project/src` succeeds; unittest still green.

---

## Phase 4: User Story 2 — `core` merged into `helper` (Priority: P2)

**Goal**: `LookalikeSearchError` and `ValidationError` live in `services/helper.py`; `services/core/` removed.

**Independent Test**: `ValidationError` / `LookalikeSearchError` importable only from `services.helper`; `services.core` path absent on disk.

### Implementation for User Story 2

- [x] T007 [US2] Merge `group_project/src/services/core/exceptions.py` into `group_project/src/services/helper.py` (clear `# Domain exceptions` section; preserve class semantics and docstrings)
- [x] T008 [US2] Update every `from services.core.exceptions import` and `from services.core import` in `group_project/src/services/` to use `services.helper` (files from T003 list; includes `similarity/pipeline.py`, `search/*.py`, `io/jsonio.py` until moved)
- [x] T009 [US2] Delete `group_project/src/services/core/exceptions.py`, `group_project/src/services/core/__init__.py`, and remove the empty `group_project/src/services/core/` directory

**Checkpoint**: Unittest green; no remaining imports of `services.core`.

---

## Phase 5: User Story 4 — Flat JSON I/O (Priority: P3)

**Goal**: `load_corpus_json` / `load_query_json` / `dump_json` live in `services/jsonio.py`; `services/io/` removed.

**Independent Test**: `from services.jsonio import load_corpus_json` works; `services.io` does not exist.

### Implementation for User Story 4

- [x] T010 [US4] Add `group_project/src/services/jsonio.py` by moving the full implementation from `group_project/src/services/io/jsonio.py`; set imports to `from services.dto import RawProfile` and `from services.helper import ValidationError`
- [x] T011 [US4] Delete `group_project/src/services/io/jsonio.py`, `group_project/src/services/io/__init__.py`, and remove empty `group_project/src/services/io/` directory
- [x] T012 [US4] Update `group_project/src/main.py` to import JSON helpers from `services.jsonio` (not `services.io.jsonio`) so the tree is never left in a broken state before Phase 6

**Checkpoint**: Tests that only need jsonio + dto + helper pass; `grep services\.io` on `src/` is clean.

---

## Phase 6: User Story 3 — `dataset` + `DataBuilder` (Priority: P2)

**Goal**: Former `similarity/pipeline.py` logic lives in `services/dataset.py` with a `DataBuilder` façade; `services/similarity/` removed; search and CLI import from `dataset` / `dto`.

**Independent Test**: `from services.dataset import iter_synthetic_profiles, build_normalized_corpus, normalize_query_raw, DataBuilder` works; `similarity.pipeline` imports are gone; equivalence/baseline tests still pass.

### Implementation for User Story 3

- [x] T013 [US3] Implement `group_project/src/services/dataset.py`: move **all** remaining logic from `group_project/src/services/similarity/pipeline.py` (catalogs `DEGREE_CATALOG` / `DOMAIN_CATALOG`, `degree_to_rank`, `domain_to_index`, `raw_to_prevector`, `minmax_stats`, `build_normalized_corpus`, `normalize_query_raw`, `iter_synthetic_profiles`, etc.); add `class DataBuilder` with methods delegating to the same implementations per [research.md](./research.md) R-01; top-level functions remain available for minimal CLI diff
- [x] T014 [US3] Delete `group_project/src/services/similarity/pipeline.py` and `group_project/src/services/similarity/__init__.py`; remove empty `group_project/src/services/similarity/` directory
- [x] T015 [US3] Update `group_project/src/main.py`: replace `services.similarity.pipeline` imports with `services.dataset` (and `services.dto` only if needed for type hints); keep `services.jsonio` imports as set in T012
- [x] T016 [US3] Update `group_project/src/services/search/strategies/base.py` to import `NormalizedProfile` from `services.dto`
- [x] T017 [US3] Update `group_project/src/services/search/strategies/baseline.py` to import `NormalizedProfile` from `services.dto` and `ValidationError` from `services.helper` as needed
- [x] T018 [US3] Update `group_project/src/services/search/strategies/kdtree.py` to import `NormalizedProfile` from `services.dto` and `ValidationError` from `services.helper` as needed
- [x] T019 [US3] Update `group_project/src/services/search/benchmark.py` to import `NormalizedProfile` from `services.dto`
- [x] T020 [US3] Update `group_project/src/services/search/topk.py` and `group_project/src/services/search/distance.py` to import `ValidationError` from `services.helper`
- [x] T021 [US3] Update `group_project/src/services/__init__.py` to re-export from `services.helper`, `services.dto`, `services.dataset`, and `services.jsonio` per [contracts/public-imports.md](./contracts/public-imports.md) (remove `core` and `similarity.pipeline`)

### Tests (import path updates)

- [x] T022 [P] [US3] Update `group_project/tests/test_topk.py` — `ValidationError` from `services.helper`
- [x] T023 [P] [US3] Update `group_project/tests/test_exceptions.py` — `ValidationError` from `services.helper`
- [x] T024 [P] [US3] Update `group_project/tests/test_distance.py` — `ValidationError` from `services.helper`
- [x] T025 [P] [US3] Update `group_project/tests/test_baseline.py` — imports from `services.dto` and `services.dataset`; `ValidationError` from `services.helper`
- [x] T026 [P] [US3] Update `group_project/tests/test_kdtree.py` — `NormalizedProfile` from `services.dto`
- [x] T027 [P] [US3] Update `group_project/tests/test_pipeline.py` — pipeline symbols from `services.dataset` and DTOs from `services.dto`; `ValidationError` from `services.helper`
- [x] T028 [P] [US3] Update `group_project/tests/test_jsonio.py` — `services.jsonio`; `RawProfile` from `services.dto`; corpus helpers from `services.dataset`
- [x] T029 [P] [US3] Update `group_project/tests/test_equivalence.py` and `group_project/tests/test_scale_smoke.py` — replace `services.similarity.pipeline` with `services.dataset`

**Checkpoint**: `rg 'services\.(core|io)\b|similarity\.pipeline' group_project/src group_project/tests --glob '*.py'` returns **no** matches; full unittest green.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Docs, agent rules, final verification.

- [x] T030 [P] Align `group_project/docs/specify-cli-guide.md` and `.cursor/rules/specify-rules.mdc` with post-refactor tree (remove `core`/`io`/`similarity` as current paths; document `dto`, `dataset`, flat `jsonio`) if they still describe the old layout
- [x] T031 Run `cd group_project && export PYTHONPATH="${PYTHONPATH}:$(pwd)/src" && python -m unittest discover -s tests -p 'test_*.py' -v` and fix any remaining failures until **OK**
- [x] T032 Optional: `python src/main.py generate-corpus --N 5 --seed 1` and `search` on the printed `corpus.json` with a fixture query — smoke-check CLI parity (SC-003)

---

## Phase 8: User Story 5 — `Corpuses` + renamed searchers (Amendment)

**Goal**: In `group_project/src/services/dataset.py`, replace **`DataBuilder`** with **`Corpuses`**: a small immutable type holding **`normalized`** profiles and **`stats`** (`ScalingStats`), with **`Corpuses.from_raw(raw: Sequence[RawProfile]) -> Corpuses`** (delegates to `build_normalized_corpus`). **`BaselineScanner`** becomes **`BaselineSearcher`**, **`KDTreeOptimizer`** becomes **`KDTreeSearcher`**, each constructed as **`Searcher(corpuses: Corpuses)`** — move current `build()` logic into **`__init__`** (or a single private `_index()` called from `__init__`). Remove **`build`** from **`SearchStrategy`**; update **`timed_build`** in `benchmark.py` to time **`searcher_cls(corpuses)`** (rename helper to e.g. **`timed_searcher_construct`** if clearer).

**Independent Test**: Full `unittest` green; JSON stdout from `search` unchanged for same inputs; `rg 'DataBuilder|BaselineScanner|KDTreeOptimizer' group_project/src group_project/tests --glob '*.py'` returns no matches (except specs/docs history if any).

### Implementation for User Story 5

- [x] T033 [US5] In `group_project/src/services/dataset.py`: remove class **`DataBuilder`**; add **`Corpuses`** (`frozen` `dataclass` or `NamedTuple` with slots) with fields **`normalized`** and **`stats`**; add **`from_raw`** classmethod; optional **`normalize_query(self, raw: RawProfile)`** delegating to **`normalize_query_raw(raw, self.stats)`**; update module docstring
- [x] T034 [US5] Update `group_project/src/services/__init__.py`: export **`Corpuses`** instead of **`DataBuilder`**; adjust **`__all__`**
- [x] T035 [US5] In `group_project/src/services/search/strategies/base.py`: rename **`SearchStrategy`** docstrings; drop abstract **`build`**; keep abstract **`search`** only
- [x] T036 [US5] In `group_project/src/services/search/strategies/baseline.py`: rename **`BaselineScanner` → `BaselineSearcher`**; **`__init__(self, corpuses: Corpuses)`** stores corpus from **`corpuses.normalized`**; remove **`build`**; preserve **`search`** behavior
- [x] T037 [US5] In `group_project/src/services/search/strategies/kdtree.py`: rename **`KDTreeOptimizer` → `KDTreeSearcher`**; **`__init__(self, corpuses: Corpuses)`** builds KD-tree from **`corpuses.normalized`**; remove **`build`**; preserve **`search`** behavior
- [x] T038 [US5] In `group_project/src/services/search/benchmark.py`: replace **`timed_build(strategy, corpus)`** with a helper that times **`searcher_cls(corpuses: Corpuses)`** and returns **`(instance, elapsed)`** or **`elapsed`** only — match call sites in **`main.py`**
- [x] T039 [US5] Update `group_project/src/services/search/strategies/__init__.py` **`__all__`** and imports to **`BaselineSearcher`**, **`KDTreeSearcher`**
- [x] T040 [US5] Update `group_project/src/main.py`: build **`Corpuses`** from loaded raw rows (e.g. **`Corpuses.from_raw(load_corpus_json(...))`** or helper **`get_synthetic_corpus` → returns `Corpuses`**); construct **`BaselineSearcher(corpuses)`** / **`KDTreeSearcher(corpuses)`**; update **`--strategy both`** path
- [x] T041 [P] [US5] Update tests: `group_project/tests/test_baseline.py`, `test_kdtree.py`, `test_equivalence.py`, `test_scale_smoke.py`, `test_main.py` (if it references class names) — use **`Corpuses`** and new searcher class names
- [x] T042 [P] [US5] `grep` **`group_project/docs/`**, **`group_project/specs/`**, **`group_project/.cursor/rules/`** for old names; update **`contracts/public-imports.md`**, **`quickstart.md`**, **`specify-cli-guide.md`**, **`specify-rules.mdc`** as needed
- [x] T043 [US5] Run `cd group_project && export PYTHONPATH="${PYTHONPATH}:$(pwd)/src" && python -m unittest discover -s tests -p 'test_*.py' -v` until **OK**
- [x] T044 [US5] Optional CLI smoke: `generate-corpus` + `search` with **`--strategy`** baseline, kdtree, both

**Checkpoint**: No **`DataBuilder`**, **`BaselineScanner`**, or **`KDTreeOptimizer`** in **`src/`** or **`tests/`**; behavior parity.

---

## Phase 9: `Corpuses`-centric dataset + `hits_equal` in helper (Amendment)

**Goal**: Move encoding/normalization/synthetic generation onto **`Corpuses`** static/class methods; move corpus/query loading off **`main.py`** into **`dataset.py`** (**`Corpuses.from_json_path`**, **`Corpuses.load_query`**, plus **`get_synthetic_corpus`** / **`get_synthetic_query`** aliases for 002 naming); move hit-list comparison to **`services.helper.hits_equal`**; keep thin module-level wrappers in **`dataset.py`** for existing tests.

**Independent Test**: Full **`unittest`** green; **`main.py`** has no **`get_synthetic_*`** or **`_hits_equal`**.

### Implementation for Phase 9

- [x] T045 [US6] Refactor `group_project/src/services/dataset.py`: implement **`degree_to_rank`**, **`domain_to_index`**, **`raw_to_prevector`**, **`apply_minmax`**, **`compute_scaling_stats`**, **`iter_synthetic_profiles`**, **`build_normalized_pair`**, **`normalize_query_raw`** as **`Corpuses`** static/class methods; **`from_raw`**, **`from_json_path`**, **`from_normalized`**; instance **`load_query`** / **`normalize_query`**; module-level one-line aliases preserving **`build_normalized_corpus`**, **`iter_synthetic_profiles`**, etc.
- [x] T046 [US6] Add `group_project/src/services/dataset.py` module functions **`get_synthetic_corpus`** → **`Corpuses`**, **`get_synthetic_query(path, corpuses)`** → **`corpuses.load_query`**; optional **`load_corpus_from_path`**
- [x] T047 [US6] Add **`hits_equal`** to `group_project/src/services/helper.py` (replaces **`main._hits_equal`**)
- [x] T048 [US6] Slim `group_project/src/main.py`: use **`Corpuses.from_json_path`** and **`corpuses.load_query`**; **`from services.helper import hits_equal`**; remove **`math`** if unused
- [x] T049 [P] [US6] Update `group_project/specs/003-src-module-restructure/contracts/public-imports.md` and **`quickstart.md`** for **`Corpuses.from_json_path`**, **`load_query`**, **`hits_equal`**
- [x] T050 [US6] Run full **`unittest`** from `group_project` with **`PYTHONPATH`** including **`src`**
- [x] T051 [US6] In `group_project/src/services/dataset.py`, prefix **`Corpuses`** implementation helpers with ``_`` (e.g. **`_degree_to_rank`**, **`_raw_to_prevector`**, **`_apply_minmax`**, **`_compute_scaling_stats`**, **`_build_normalized_pair`**, **`_normalize_query_raw`**); keep **`iter_synthetic_profiles`**, factories (**`from_*`**), **`normalize_query`**, **`load_query`** public; module-level **`degree_to_rank`**, **`build_normalized_corpus`**, etc. remain the stable import surface

**Checkpoint**: **`rg 'get_synthetic_corpus|get_synthetic_query' group_project/src/main.py`** has no matches; loading helpers importable from **`services.dataset`**.

---

## Dependencies & Execution Order

### Phase Dependencies

| Phase | Depends on | Notes |
|-------|------------|--------|
| Phase 1 Setup | — | |
| Phase 2 Foundational | Phase 1 | |
| Phase 3 US1 | Phase 2 | DTO definitions first |
| Phase 4 US2 | Phase 3 | Exceptions can merge after DTO split (pipeline still exists) |
| Phase 5 US4 | Phase 3, Phase 4 | `jsonio` needs `dto` + `helper` |
| Phase 6 US3 | Phase 3, Phase 4, Phase 5 | Remove `pipeline` last; `main` uses `jsonio` + `dataset` |
| Phase 7 Polish | Phase 6 | |
| Phase 8 US5 | Phase 7 (003 layout complete) | `Corpuses` in `dataset`; depends on `dto` types |
| Phase 9 US6 | Phase 8 | `Corpuses` API surface + `hits_equal` |

### User Story Dependencies

- **US1**: No dependency on US3/US4 for type definitions; blocks clean removal of classes from `pipeline`.
- **US2**: Independent of US4/US3 except must finish before deleting modules that still imported `core`.
- **US4**: Depends on US1+US2; should complete before US3 deletes `pipeline` if any code still imported `RawProfile` from `pipeline` (eliminated by T010).
- **US3**: Depends on US1, US2, US4.
- **US5**: Depends on US3 complete; sequential **T033 → T040** before parallel test/doc tasks **T041–T042**.
- **US6** (Phase 9): Depends on US5; **`Corpuses`** surface + **`hits_equal`** (T045–T051).

### Parallel Opportunities

- **T022–T029** all touch different files under `tests/` — can be one commit or parallel edits after **T021** is done.
- **T030** can proceed in parallel with final test runs if different author.
- **T041** and **T042** can run in parallel after **T040** lands.

### Parallel Example: Tests

```bash
# After T021 (services/__init__.py) and src/search updates:
# Batch-edit tests: test_topk, test_exceptions, test_distance, test_baseline,
# test_kdtree, test_pipeline, test_jsonio, test_equivalence, test_scale_smoke
```

---

## Implementation Strategy

### MVP First (User Story 1 only)

1. Complete Phase 1–2  
2. Complete Phase 3 (T004–T006)  
3. **STOP**: confirm DTO-only definitions and green tests  

### Full feature (recommended order)

1. Phase 1–2 → baseline + inventory  
2. Phase 3 → `dto/`  
3. Phase 4 → `helper` + delete `core`  
4. Phase 5 → flat `jsonio`  
5. Phase 6 → `dataset` + `DataBuilder` + delete `similarity` + wire `search`, `main`, `services/__init__.py`, tests  
6. Phase 7 → docs + final unittest + optional CLI smoke  
7. Phase 8 → **`Corpuses`**, **`BaselineSearcher`**, **`KDTreeSearcher`** (T033–T044)  
8. Phase 9 → **`Corpuses`** methods + **`dataset`** load helpers + **`hits_equal`** + **`_`** internal helpers (T045–T051)

---

## Notes

- Total tasks: **51** (T001–T051 complete).  
- **Private** types (e.g. `_WorstKey` in `topk.py`) stay put per [spec.md](./spec.md) assumption A-001 — no task to move them into `dto`.  
- If a mid-step breaks imports, prefer **small commits** per phase boundary above.  
- Format validation: every task uses `- [ ]` / `- [x]`, sequential **T###** ID, optional **[P]**, **[US#]** only on story-phase tasks, and explicit `group_project/` paths.
