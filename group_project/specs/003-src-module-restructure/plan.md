# Implementation Plan: Source layout consolidation (003)

**Branch**: `003-src-module-restructure` | **Date**: 2026-04-06 | **Spec**: [spec.md](./spec.md)  
**Input**: Feature specification from `/specs/003-src-module-restructure/spec.md` — user note: *refactor code* (DTO package, merge `core` into `helper`, `DataBuilder` in `dataset`, flat `jsonio`).

## Summary

Reorganize `group_project/src/services/` so that **domain dataclasses** live under **`services/dto/`**, **domain exceptions** (and former `core` exports) live in **`services/helper.py`** alongside existing math helpers, **corpus/query preparation** currently in **`similarity/pipeline.py`** moves to **`services/dataset.py`** behind a **`DataBuilder`** façade, and **`io/jsonio.py`** moves to **`services/jsonio.py`** with **`services/io/`** and **`services/core/`** removed. **`services/similarity/`** is removed after call sites import from **`dataset`** and **`dto`**. **No JSON schema or CLI behavior change**; full **`unittest`** suite stays green. Private algorithm-local types (e.g. **`_WorstKey`** in `topk.py`) remain colocated per spec assumption A-001.

## Technical Context

**Language/Version**: Python 3.12+  
**Primary Dependencies**: **None (stdlib only)** per `.specify/memory/constitution.md`  
**Storage**: UTF-8 JSON on disk (unchanged contracts)  
**Testing**: **`unittest` (stdlib)** only  
**Target Platform**: macOS/Linux developer CLI + library modules  
**Project Type**: single package under `src/services/` + `src/main.py`  
**Performance Goals**: Identical asymptotics and numeric outputs vs pre-refactor (byte-identical generated corpora where deterministic)  
**Constraints**: No circular imports; dependency direction **dto → helper → jsonio / dataset → search → main**  
**Scale/Scope**: ~15 source modules touched (see [research.md](./research.md) import inventory)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **Standard Library First**: Refactor is moves/renames only; no PyPI.
- [x] **PEP 8 & type hints**: New package `dto`; `DataBuilder` API fully typed; `helper` gains exception classes.
- [x] **Functional-first modularity**: `DataBuilder` orchestrates existing pure logic; avoid god-object beyond façade methods mapping to former free functions.
- [x] **Complexity & memory**: No algorithm changes; same iterators and builds.
- [x] **Documentation**: Google-style docstrings on new public symbols; `dto/__init__.py` documents export surface.
- [x] **Errors**: `LookalikeSearchError` / `ValidationError` preserved (relocated into `helper.py`).
- [x] **Testing**: Same `unittest` discovery; update imports in tests if they reference old paths (grep `services.similarity`, `services.core`, `services.io`).

## Project Structure

### Documentation (this feature)

```text
specs/003-src-module-restructure/
├── plan.md              # This file
├── research.md          # Phase 0
├── data-model.md        # Phase 1
├── quickstart.md        # Phase 1 (import path deltas)
├── contracts/
│   └── public-imports.md
└── checklists/
    └── requirements.md  # (existing from /speckit.specify)
```

### Source Code (target layout)

```text
group_project/src/
├── main.py
└── services/
    ├── __init__.py          # Re-exports updated (see contracts/public-imports.md)
    ├── helper.py            # VECTOR_DIM, geometry/minmax + LookalikeSearchError, ValidationError
    ├── jsonio.py            # Was services/io/jsonio.py
    ├── dataset.py           # DataBuilder + former pipeline.py body (catalogs, normalization, synthetic iter)
    ├── dto/
    │   ├── __init__.py      # Export RawProfile, NormalizedProfile, ScalingStats
    │   └── profiles.py      # Dataclass definitions (optional split; single file OK)
    └── search/
        └── ...              # Unchanged algorithms; imports from dto, helper, dataset
```

**Removed** (after migration): `services/core/`, `services/io/`, `services/similarity/`.

**Structure Decision**: Single `dto` package for shared immutable records; single `helper.py` for errors + numeric helpers per FR-002; `dataset.py` as single module for builder + pipeline logic per FR-003; flat `jsonio.py` per FR-004.

## Phase 0: Research

See [research.md](./research.md) — decisions on **`DataBuilder` API shape**, **import layering**, and **what stays out of dto**.

## Phase 1: Design artifacts

- [data-model.md](./data-model.md) — DTO fields and validation ownership.  
- [contracts/public-imports.md](./contracts/public-imports.md) — supported import paths post-refactor.  
- [quickstart.md](./quickstart.md) — developer commands unchanged; import examples updated.

## Migration order (implementation guide)

1. Add **`services/dto/`** and move **`RawProfile`**, **`NormalizedProfile`**, **`ScalingStats`** from `pipeline.py` into `dto` (no logic, only types + re-exports if needed).
2. Merge **`services/core/exceptions.py`** into **`services/helper.py`** (classes at module top or bottom; keep clear section comments). Delete **`core/`** and fix all `from services.core.exceptions` → `from services.helper`.
3. Move **`pipeline.py`** body into **`dataset.py`**: implement **`DataBuilder`** with methods delegating to former module-level functions (e.g. `build_normalized_corpus`, `normalize_query_raw`, `iter_synthetic_profiles`, catalog maps). Either keep module-level functions as thin wrappers calling a default builder instance, or only expose class methods — pick one style in tasks; default recommendation: **keep same function names at module level in `dataset.py` for minimal diff**, plus **`DataBuilder`** wrapping them for discoverability.
4. Move **`jsonio.py`** to **`services/jsonio.py`**; update imports to `from services.dto import RawProfile` and `from services.helper import ValidationError`. Delete **`io/`**.
5. Update **`search/**`** to import **`NormalizedProfile`** from **`services.dto`**; update **`baseline`**, **`base`**, **`kdtree`**, **`benchmark`**.
6. Update **`main.py`**: `from services.io.jsonio` → `from services.jsonio`; `from services.similarity.pipeline` → `from services.dataset` (or `DataBuilder` only if CLI uses class).
7. Update **`services/__init__.py`** exports.
8. **`grep`** tests and docs for old paths; run **`python -m unittest discover -s tests -p 'test_*.py'`** with **`PYTHONPATH=src`**.

## Complexity Tracking

No constitution violations; table empty.

## Agent context

Run after editing plan: `.specify/scripts/bash/update-agent-context.sh cursor-agent` from `group_project/`.
