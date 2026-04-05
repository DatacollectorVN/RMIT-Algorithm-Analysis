---
description: "Task list for Scalable Top-k Profile Similarity Search (stdlib only)"
---

# Tasks: Scalable Top-k Profile Similarity Search

**Input**: Design documents from `/Users/nhan.ngo/rmit/RMIT-Algorithm-Analysis/group_project/specs/001-similarity-search-topk/`  
**Prerequisites**: [plan.md](./plan.md), [spec.md](./spec.md), [research.md](./research.md), [data-model.md](./data-model.md), [contracts/](./contracts/)

**Tests**: **In scope** per [spec.md](./spec.md) — all tests use **`unittest`** only (no PyPI).

**Constraint**: Every task MUST respect **no external libraries** (Python Standard Library
only); see `.specify/memory/constitution.md`.

**Roadmap categories** (mapped into phases below):

| # | Category | Primary phases |
|---|----------|----------------|
| 1 | Data generation (100k+ records) | US1 (core generator), US3 (scale hardening) |
| 2 | Feature engineering (normalization / categorical mapping) | US1 (pipeline stages) |
| 3 | Baseline search (full scan) | US1 (`BaselineScanner`) |
| 4 | Optimized search (k-d tree build + query) | US2 (`KDTreeOptimizer`) |
| 5 | Evaluation suite (runtime + complexity benchmarking) | US2–US3 (timing, equivalence, scale smoke) |

**Organization**: Phases follow user-story order (P1 → P2 → P3) per spec; category
numbers are referenced in task descriptions where relevant.

**Format**: `[ID] [P?] [Story?] Description with file path`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Repository layout and import path for `src/lookalike_search` (stdlib only).

- [x] T001 Create package directories per [plan.md](./plan.md): `src/lookalike_search/`, `src/lookalike_search/strategies/`, and `tests/` under `/Users/nhan.ngo/rmit/RMIT-Algorithm-Analysis/group_project/`
- [x] T002 [P] Add `src/lookalike_search/__init__.py` exposing the public package surface (docstring; re-exports optional)
- [x] T003 [P] Add `src/lookalike_search/strategies/__init__.py` and `tests/__init__.py` (empty or module docstring only)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Shared error model, distance engine, and top-k helper — **required before any strategy or pipeline** can be correct.

**⚠️ CRITICAL**: No user story work below until this phase is complete.

- [x] T004 Implement custom exception hierarchy (`LookalikeSearchError`, validation errors) in `/Users/nhan.ngo/rmit/RMIT-Algorithm-Analysis/group_project/src/lookalike_search/exceptions.py`
- [x] T005 [P] Implement weighted squared-distance on five-vectors per [research.md](./research.md) R-01 in `/Users/nhan.ngo/rmit/RMIT-Algorithm-Analysis/group_project/src/lookalike_search/distance.py`
- [x] T006 [P] Implement `heapq`-based streaming top-k (distance ascending, tie-break by `profile_id`) per [research.md](./research.md) R-04 in `/Users/nhan.ngo/rmit/RMIT-Algorithm-Analysis/group_project/src/lookalike_search/topk.py`
- [x] T007 [P] Add `unittest` cases for `distance.py` in `/Users/nhan.ngo/rmit/RMIT-Algorithm-Analysis/group_project/tests/test_distance.py`
- [x] T008 [P] Add `unittest` cases for `topk.py` in `/Users/nhan.ngo/rmit/RMIT-Algorithm-Analysis/group_project/tests/test_topk.py`
- [x] T009 Add `unittest` cases for invalid weights / non-finite inputs raising project exceptions in `/Users/nhan.ngo/rmit/RMIT-Algorithm-Analysis/group_project/tests/test_exceptions.py`

**Checkpoint**: Foundation ready — **Categories 2–4** implementations can import distance + top-k safely.

---

## Phase 3: User Story 1 — Find top-k lookalike profiles (Priority: P1) 🎯 MVP

**Goal**: **Categories 1–3**: synthetic profiles, encoding + Min–Max pipeline, exhaustive **baseline** top-k search.

**Independent test**: Small fixed corpus; assert ≤k results, correct ordering by declared distance, deterministic ties ([spec.md](./spec.md) US1).

### Implementation for User Story 1

- [x] T010 [US1] Implement **Category 1 — data generation**: configurable `random` generator yielding ≥100k-capable synthetic `RawProfile` records (fields: `profile_id`, `age`, `monthly_income`, `daily_learning_hours`, `highest_degree`, `favourite_domain`) in `/Users/nhan.ngo/rmit/RMIT-Algorithm-Analysis/group_project/src/lookalike_search/pipeline.py`
- [x] T011 [US1] Implement **Category 2 — categorical mapping**: ordered `highest_degree` catalog + finite `favourite_domain` catalog → numeric codes in `/Users/nhan.ngo/rmit/RMIT-Algorithm-Analysis/group_project/src/lookalike_search/pipeline.py`
- [x] T012 [US1] Implement **Category 2 — normalization**: corpus-wide Min–Max `ScalingStats` and `normalize_profile` / batch normalize in `/Users/nhan.ngo/rmit/RMIT-Algorithm-Analysis/group_project/src/lookalike_search/pipeline.py`
- [x] T013 [US1] Define `SearchStrategy` ABC (`build`, `search`) in `/Users/nhan.ngo/rmit/RMIT-Algorithm-Analysis/group_project/src/lookalike_search/strategies/base.py`
- [x] T014 [US1] Implement **Category 3 — baseline full scan**: `BaselineScanner` using `distance.py` + `topk.py` over all normalized profiles in `/Users/nhan.ngo/rmit/RMIT-Algorithm-Analysis/group_project/src/lookalike_search/strategies/baseline.py`

### Tests for User Story 1

- [x] T015 [P] [US1] Add pipeline unit tests (encoding, Min–Max edge `max==min`, invalid catalog) in `/Users/nhan.ngo/rmit/RMIT-Algorithm-Analysis/group_project/tests/test_pipeline.py`
- [x] T016 [US1] Add baseline unit tests (k > n, k=1, tie-break id order) in `/Users/nhan.ngo/rmit/RMIT-Algorithm-Analysis/group_project/tests/test_baseline.py`

**Checkpoint**: MVP delivers correct top-k on small corpora without k-d tree.

---

## Phase 4: User Story 2 — Compare baseline vs accelerated (Priority: P2)

**Goal**: **Category 4** k-d tree + **Category 5** start: equivalence so benchmarks are valid; record search timings.

**Independent test**: Same query/corpus/k → baseline and k-d tree outputs match per [research.md](./research.md) R-06 ([spec.md](./spec.md) US2).

### Implementation for User Story 2

- [x] T017 [US2] Implement **Category 4 — optimized search**: 5D `KDTreeOptimizer` (median split, cyclic axis, k-NN pruning) using the **same** distance function as baseline in `/Users/nhan.ngo/rmit/RMIT-Algorithm-Analysis/group_project/src/lookalike_search/strategies/kdtree.py`
- [x] T018 [US2] Export `SearchStrategy`, `BaselineScanner`, `KDTreeOptimizer` from `/Users/nhan.ngo/rmit/RMIT-Algorithm-Analysis/group_project/src/lookalike_search/strategies/__init__.py`
- [x] T019 [US2] Add **Category 5 — timing hooks**: small helper using `time.perf_counter()` around `search()` (and optional `build()`) in `/Users/nhan.ngo/rmit/RMIT-Algorithm-Analysis/group_project/src/lookalike_search/benchmark.py` (new file, stdlib only)

### Tests for User Story 2

- [x] T020 [P] [US2] Add k-d tree tests: small n, brute-force reference inside test in `/Users/nhan.ngo/rmit/RMIT-Algorithm-Analysis/group_project/tests/test_kdtree.py`
- [x] T021 [US2] Add equivalence tests baseline vs `KDTreeOptimizer` for multiple seeds/corpora (tolerance `1e-9`, tie rules) in `/Users/nhan.ngo/rmit/RMIT-Algorithm-Analysis/group_project/tests/test_equivalence.py`

**Checkpoint**: Accelerated path matches baseline on test suite; timings can be collected in code.

---

## Phase 5: User Story 3 — Large corpus + evaluation reporting (Priority: P3)

**Goal**: **Category 1 & 5**: 100k+ operationally; JSON I/O; CLI benchmark output for complexity write-ups.

**Independent test**: Generate or load ≥100k profiles, run both strategies, capture timing; accelerated faster on at least one documented workload or document exception ([spec.md](./spec.md) US3).

### Implementation for User Story 3

- [x] T022 [US3] Harden **Category 1** for scale: document/implement two-pass Min–Max over large n (materialize or stream policy) without PyPI in `/Users/nhan.ngo/rmit/RMIT-Algorithm-Analysis/group_project/src/lookalike_search/pipeline.py`
- [x] T023 [US3] Implement stdlib `json` load/save for corpus + query payloads matching `contracts/` in `/Users/nhan.ngo/rmit/RMIT-Algorithm-Analysis/group_project/src/lookalike_search/jsonio.py`
- [x] T024 [US3] Implement **Category 5 — evaluation CLI**: `argparse` entry in `/Users/nhan.ngo/rmit/RMIT-Algorithm-Analysis/group_project/main.py` (`--strategy`, `--generate`, `--corpus`, `--query`, `--k`, `--seed`, `--benchmark`) printing results JSON shaped like [contracts/search-response.schema.json](./contracts/search-response.schema.json)
- [x] T025 [US3] Write textual **complexity / runtime summary** (stdout or stderr) comparing baseline vs k-d tree on same workload for coursework reports in `/Users/nhan.ngo/rmit/RMIT-Algorithm-Analysis/group_project/main.py`

### Tests for User Story 3

- [x] T026 [P] [US3] Add JSON round-trip tests against [contracts/corpus-record.schema.json](./contracts/corpus-record.schema.json) and [contracts/query-request.schema.json](./contracts/query-request.schema.json) in `/Users/nhan.ngo/rmit/RMIT-Algorithm-Analysis/group_project/tests/test_jsonio.py`
- [x] T027 [US3] Add scale smoke test: default **n ≥ 10_000** synthetic profiles, both strategies complete (optional skip/`@unittest.skipUnless` for **n = 100_000** local runs) in `/Users/nhan.ngo/rmit/RMIT-Algorithm-Analysis/group_project/tests/test_scale_smoke.py`

**Checkpoint**: End-to-end 100k+ path and benchmark narrative supported.

---

## Phase 6: Polish & Cross-Cutting Concerns

- [x] T028 [P] Google-style docstring pass on all public modules under `/Users/nhan.ngo/rmit/RMIT-Algorithm-Analysis/group_project/src/lookalike_search/`
- [x] T029 [P] Update `/Users/nhan.ngo/rmit/RMIT-Algorithm-Analysis/group_project/specs/001-similarity-search-topk/quickstart.md` with final `main.py` examples and `PYTHONPATH`
- [x] T030 Run `python -m unittest discover -s /Users/nhan.ngo/rmit/RMIT-Algorithm-Analysis/group_project/tests -p 'test_*.py'` from repo root and fix failures

---

## Dependencies & Execution Order

### Phase dependencies

- **Phase 1** → **Phase 2** → **Phase 3 (US1)** → **Phase 4 (US2)** → **Phase 5 (US3)** → **Phase 6**
- **US2** depends on **US1** (`BaselineScanner`, normalized corpus types).
- **US3** depends on **US1** and **US2** (CLI compares strategies at scale).

### Category coverage checklist

- [x] **1 — Data generation**: T010, T022, T024 (via `--generate`)
- [x] **2 — Feature engineering**: T011, T012
- [x] **3 — Baseline search**: T014
- [x] **4 — k-d tree**: T017
- [x] **5 — Evaluation**: T019, T024–T025, tests T021, T026–T027

### Parallel opportunities

- **Phase 1**: T002, T003 in parallel after T001.
- **Phase 2**: T005–T008 parallel after T004; T009 after exceptions exist.
- **US1**: T015 in parallel with T016 once T010–T014 land (overlap allowed after T012 for partial tests).
- **US2**: T020 in parallel once T017–T018 exist; T021 after T017–T018.
- **US3**: T026 in parallel with T022–T025 once `jsonio` API is sketched.
- **Phase 6**: T028, T029 in parallel.

---

## Parallel Example: User Story 2

```text
After T017–T018: run T020 (test_kdtree.py) while starting T019 (benchmark.py) in parallel.
T021 (equivalence) must follow T017 and baseline from US1.
```

---

## Implementation Strategy

### MVP first (User Story 1 only)

1. Complete Phases 1–2.
2. Complete Phase 3 (US1) through T016; run `test_pipeline.py`, `test_baseline.py`.
3. **Stop and validate** MVP against US1 acceptance scenarios.

### Incremental delivery

1. Add Phase 4 (US2): k-d tree + equivalence + `benchmark.py`.
2. Add Phase 5 (US3): JSON I/O, `main.py`, scale smoke, report output.
3. Polish (Phase 6).

### Notes

- Do not add `requirements.txt` with PyPI pins; optional `pyproject.toml` without
  dependencies is allowed only if course requires it — default is **no third-party
  deps**.
- All file paths above are **absolute** for copy/paste clarity; relative paths from
  `group_project/` match `src/...` and `tests/...`.
