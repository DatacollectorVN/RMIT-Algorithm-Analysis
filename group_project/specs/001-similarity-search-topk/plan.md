# Implementation Plan: Scalable Top-k Profile Similarity Search

**Branch**: `001-similarity-search-topk` | **Date**: 2026-04-04 | **Spec**: [spec.md](./spec.md)  
**Input**: Feature specification from `/specs/001-similarity-search-topk/spec.md`  
**Architecture label**: High-Speed Sorting Facility (stdlib similarity engine)

## Summary

Deliver a **top-k lookalike search** over **100,000+** synthetic user profiles using
five weighted attributes. Provide two interchangeable strategies: an exhaustive
**baseline** for ground truth and a **KD-tree** accelerated spatial partitioner
for fast queries. Use a **multi-stage pipeline** (categorical encoding → corpus
Min–Max normalization), a **weighted squared-distance** metric, **`heapq`** for
streaming top-k selection, and **`src/main.py`** as the CLI entry. All work stays in
**Python 3.12+** with **stdlib only**, matching the project constitution and the
feature spec’s benchmarking goals.

## Technical Context

**Language/Version**: Python **3.12+**  
**Primary Dependencies**: **None** — stdlib only per
`/Users/nhan.ngo/rmit/RMIT-Algorithm-Analysis/group_project/.specify/memory/constitution.md`
(no PyPI). Primary modules: `abc`, `argparse`, `dataclasses`, `heapq`, `json`,
`math`, `random`, `time`, `typing`, `collections.abc`; also `logging` and
`unittest` as required by the constitution for diagnostics and tests.  
**Storage**: Optional JSON files for corpus/query I/O (`json`); in-memory
structures for search indices  
**Testing**: `unittest` only (discovery under `tests/`)  
**Target Platform**: macOS / Linux / Windows — CPython 3.12+  
**Project Type**: CLI + importable library package under `src/`  
**Performance Goals**: Baseline completes 100k queries within SC-001 (~30s search
budget on reference hardware or documented actuals); accelerated strategy
faster than baseline on at least one documented workload (spec SC-004)  
**Constraints**: No external packages; strict type hints and Google docstrings;
custom exceptions for all contract violations  
**Scale/Scope**: ≥ **100,000** profiles; configurable **k**; single-process v1

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Verify against `.specify/memory/constitution.md` (RMIT group project):

- [x] **Standard Library First**: No PyPI/third-party runtime or test dependencies;
      plan and file layout do not assume external packages.
- [x] **PEP 8 & type hints**: Approach is compatible with strict typing and PEP 8;
      public API surfaces identified for docstrings and hints.
- [x] **Functional-first modularity**: Boundaries (modules/packages) are clear;
      shared mutable state is minimal and justified.
- [x] **Complexity & memory**: Primary data paths target O(n)-time (or better)
      typical behavior; extra space proportional unless justified in Complexity
      Tracking below.
- [x] **Documentation**: Plan names modules/functions that will use Google-style
      docstrings.
- [x] **Errors**: Custom exception hierarchy covers expected domain/contract
      failures for this feature.
- [x] **Testing**: Test strategy uses `unittest` (stdlib) only.

**Post–Phase 1 re-check (2026-04-04)**: Design artifacts (`research.md`,
`data-model.md`, `contracts/`) remain stdlib-only; KD-tree build cost documented
below; no constitution waivers required.

## Project Structure

### Documentation (this feature)

```text
specs/001-similarity-search-topk/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── README.md
│   ├── corpus-record.schema.json
│   ├── query-request.schema.json
│   └── search-response.schema.json
├── spec.md
└── tasks.md              # Phase 2 (/speckit.tasks) — not created by this command
```

### Source Code (repository root)

```text
group_project/
├── src/
│   ├── main.py
│   └── services/
│       ├── helper.py
│       ├── core/exceptions.py
│       ├── similarity/pipeline.py
│       ├── search/
│       │   ├── distance.py
│       │   ├── topk.py
│       │   ├── benchmark.py
│       │   └── strategies/
│       │       ├── base.py
│       │       ├── baseline.py
│       │       └── kdtree.py
│       └── io/jsonio.py
└── tests/
    └── test_*.py
```

**Structure Decision**: CLI at `src/main.py`; services under `src/services/` by
domain (`core`, `similarity`, `search`, `io`) plus `helper.py` for pure utilities.
Strategy pattern unchanged (`SearchStrategy` → `BaselineScanner` |
`KDTreeOptimizer`).

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| KD-tree **build** time **O(n log n)** | Spec requires spatial partitioning (FR-006); tree construction is standard | Flat scan only = baseline already; no index for acceleration |
| k-NN query **not** strict O(n) worst case | KD-tree average-case sublinear pruning; worst-case can degrade | Baseline already covers O(n) **per query**; index targets typical speedup for report |

**Baseline**: O(n) distance evaluations per query; top-k accumulation O(n log k)
with `heapq`. **KD-tree**: build O(n log n); query expected much better than
linear on structured data with pruning; must match baseline outputs (see
[research.md](./research.md) R-06).

## Phase 0 & Phase 1 outputs

| Artifact | Path |
|----------|------|
| Research | [research.md](./research.md) |
| Data model | [data-model.md](./data-model.md) |
| Contracts | [contracts/](./contracts/) |
| Quickstart | [quickstart.md](./quickstart.md) |

## Design highlights (from stakeholder architecture input)

1. **Data pipeline**: Generator for **100,000+** synthetic profiles; stages for
   categorical encoding (`highest_degree`, `favourite_domain`) and **Min–Max**
   normalization using corpus statistics ([research.md](./research.md) R-02).
2. **Strategy pattern**: `SearchStrategy` ABC; **`BaselineScanner`** (exhaustive
   O(n) evaluations per query); **`KDTreeOptimizer`** (5D KD-tree, same distance
   function) ([research.md](./research.md) R-05).
3. **Distance engine**: Weighted sum of per-dimension **squared differences** on
   normalized vectors ([research.md](./research.md) R-01).
4. **Priority retrieval**: **`heapq`** maintains top-k during scan ([research.md](./research.md) R-04).
5. **Orchestration**: **`main.py`** selects strategy, loads/generates data, runs
   search, emits results and optional **`time.perf_counter()`** benchmarks
   ([research.md](./research.md) R-07–R-08).
