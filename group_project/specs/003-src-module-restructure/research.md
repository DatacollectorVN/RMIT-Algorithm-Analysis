# Research: 003 Source layout consolidation

**Feature**: [spec.md](./spec.md)  
**Date**: 2026-04-06

## R-01 — `DataBuilder` shape

**Decision**: Provide **`DataBuilder`** as a **thin façade** with instance methods that delegate to the **same implementations** now in `pipeline.py` (either moved as nested logic or as module-level functions in `dataset.py`). Expose **`iter_synthetic_profiles`**, **`build_normalized_corpus`**, **`normalize_query_raw`**, and catalog accessors as today, so **`main.py`** can call **`DataBuilder().build_normalized_corpus(...)`** *or* keep importing module-level **`build_normalized_corpus`** from **`services.dataset`** for minimal churn.

**Rationale**: Spec SC-002/SC-003 require behavior identity; preserving function bodies verbatim reduces risk. The class satisfies FR-003 “primary façade” without forcing every call site to adopt OOP immediately.

**Alternatives considered**:

- **Only** class API, no module functions — fewer entry points but larger diff in `main.py` and tests.
- **Static-only class** — acceptable; slightly less ergonomic for future injectable dependencies.

## R-02 — DTO package layout

**Decision**: New package **`src/services/dto/`** with **`profiles.py`** (or single **`models.py`**) defining **`RawProfile`**, **`NormalizedProfile`**, **`ScalingStats`**. **`dto/__init__.py`** re-exports all three. No imports from **`dataset`** or **`jsonio`** inside **`dto`** (types only).

**Rationale**: Breaks cycles: `jsonio` and `dataset` both depend on DTOs; DTOs depend on nothing in `services`.

**Alternatives considered**:

- One flat **`dto.py`** file — valid; package scales better if more DTOs appear later.

## R-03 — Exceptions in `helper.py`

**Decision**: Append **`LookalikeSearchError`** and **`ValidationError`** to **`helper.py`** (or group after a `# Domain exceptions` banner). Replace **`from services.core.exceptions`** everywhere with **`from services.helper import …`**.

**Rationale**: Matches FR-002 explicitly.

**Alternatives considered**:

- **`services/errors.py`** — cleaner name but violates user’s “put in helper.py” instruction unless plan negotiates; spec says **`helper.py`** is the documented entry.

## R-04 — What stays outside `dto`

**Decision**: **`_WorstKey`** in **`topk.py`** remains **private** to search/top-k per A-001. No move to **`dto`**.

**Rationale**: Not a shared domain record exported across layers; moving it adds coupling.

## R-05 — `jsonio` location

**Decision**: File **`src/services/jsonio.py`** (sibling to **`helper.py`**). Imports: **`services.dto`**, **`services.helper`**.

**Rationale**: FR-004; flattens package graph.

## R-06 — Import inventory (pre-refactor)

Call sites observed:

| From | Imports |
|------|---------|
| `main.py` | `services.io.jsonio`, `services.similarity.pipeline` |
| `services/__init__.py` | `services.core.exceptions`, `services.similarity.pipeline` |
| `services/io/jsonio.py` | `core.exceptions`, `similarity.pipeline.RawProfile` |
| `services/similarity/pipeline.py` | `core.exceptions`, `helper` |
| `search/topk.py`, `distance.py`, `baseline.py`, `kdtree.py`, `benchmark.py` | `core.exceptions`, `helper`, `similarity.pipeline.NormalizedProfile` |
| `search/strategies/base.py` | `NormalizedProfile` |

**Post-refactor**: **`core`** and **`io`** and **`similarity.pipeline`** strings should appear **zero** times outside **`specs/`** and git history.

## R-07 — Tests

**Decision**: Grep **`tests/`** for `services.core`, `services.io`, `services.similarity`; update to new paths. No new third-party test tools.

**Rationale**: FR-006.
