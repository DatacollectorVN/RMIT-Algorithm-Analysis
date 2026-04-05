# Data Model: 001-similarity-search-topk

**Date**: 2026-04-04  
**Spec**: [spec.md](./spec.md)

## Overview

Entities support synthetic profile generation, normalized feature vectors, queries,
search results, and benchmark metadata. All validation errors map to the project
exception hierarchy (see `exceptions` module in plan).

---

## RawProfile (synthetic / input record)

| Field | Type | Constraints |
|-------|------|-------------|
| `profile_id` | `str` | Non-empty; unique within a corpus |
| `age` | `int` or `float` | Sensible bound, e.g. 18–80 (configurable constant) |
| `monthly_income` | `float` | Non-negative |
| `daily_learning_hours` | `float` | Non-negative, upper cap e.g. ≤ 24 |
| `highest_degree` | `str` | Member of ordered catalog (education) |
| `favourite_domain` | `str` | Member of finite domain catalog |

**Relationships**: Many `RawProfile` form a **Corpus** (ordered collection for
deterministic iteration).

---

## NormalizedProfile

| Field | Type | Constraints |
|-------|------|-------------|
| `profile_id` | `str` | Same as source |
| `vector` | `tuple[float, float, float, float, float]` | All components finite; typically in `[0, 1]` after pipeline |

**Invariant**: `vector` order is fixed:
`(age, monthly_income, education, learning_hours, domain_slot)`.

---

## ScalingStats (Min–Max)

| Field | Type | Purpose |
|-------|------|---------|
| `mins` | `tuple[float, ...]` | Per-dimension minimum after encoding |
| `maxs` | `tuple[float, ...]` | Per-dimension maximum |

Used to normalize new queries with the **same** stats as the corpus.

---

## QuerySpec

| Field | Type | Constraints |
|-------|------|-------------|
| `reference` | `RawProfile` or pre-normalized vector + id | Must be encodable with corpus `ScalingStats` |
| `weights` | `tuple[float, float, float, float, float]` | Each ≥ 0; at least one > 0 (reject all-zero) |
| `k` | `int` | ≥ 1 |

---

## SearchHit

| Field | Type | Constraints |
|-------|------|-------------|
| `profile_id` | `str` | From corpus |
| `distance` | `float` | Non-negative; lower is more similar |

**Ordering**: Ascending `distance`, tie-break ascending `profile_id`.

---

## BenchmarkRecord

| Field | Type | Notes |
|-------|------|-------|
| `strategy` | `str` | e.g. `baseline`, `kdtree` |
| `corpus_size` | `int` | `n` |
| `k` | `int` | Requested k |
| `elapsed_seconds` | `float` | `perf_counter` delta for `search` |
| `build_seconds` | `float` | Optional; separate from search |

---

## SearchStrategy (conceptual)

- **State**: Built index or flat list of `NormalizedProfile`.
- **Operations**: `build(corpus: Sequence[NormalizedProfile])`, `search(query:
  QuerySpec) -> list[SearchHit]`.

No ORM or persistence layer in v1; optional JSON file I/O for profiles uses
`json` module and validates against [contracts](./contracts/).
