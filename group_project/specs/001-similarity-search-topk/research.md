# Research: 001-similarity-search-topk

**Date**: 2026-04-04  
**Spec**: [spec.md](./spec.md)  
**Plan**: [plan.md](./plan.md)

Consolidated decisions for Phase 0. No open **NEEDS CLARIFICATION** items; defaults
align with `spec.md` assumptions and the chosen stdlib-only stack.

---

## R-01 — Weighted distance on five attributes

**Decision**: After pipeline normalization, represent each profile as a
5-dimensional vector `(v0..v4)` corresponding to **age**, **monthly_income**,
**education_level**, **daily_learning_hours**, **professional_domain** (all
finite floats in `[0, 1]` after Min–Max on numeric dims; see R-02/R-03). For a
query vector `q` and corpus vector `p`, define per-dimension squared difference
`d_i = (q_i - p_i)²`. Total dissimilarity is:

`distance(q, p) = sum_i w_i * d_i`

where weights `w_i` are non-negative caller-supplied floats (not required to sum
to 1; zero weight ignores that dimension).

**Rationale**: Matches “weighted distance” in the spec, stays smooth for numeric
dims, and keeps a single scalar score for ranking and heap operations.

**Alternatives considered**:

- Weighted Manhattan (`sum w_i |q_i-p_i|`) — simpler but less standard for
  “lookalike” in Euclidean-style feature space; rejected for this v1.
- Separate kernel for categorical domain — covered by encoding domain as 0/1
  numeric after catalog mapping (R-03), then same formula applies.

---

## R-02 — Synthetic data pipeline & Min–Max scaling

**Decision**: A **generator** yields raw synthetic records (dicts or dataclasses)
with fields aligned to the spec. A **multi-stage pipeline**:

1. **Sample / generate** — `random` with fixed optional seed for reproducibility.
2. **Categorical encoding** — map string fields **`highest_degree`** (synonym for
   education level) and **`favourite_domain`** (synonym for professional domain)
   to numeric codes `0 .. K-1`, then divide by `(K-1)` (or map to `[0,1]` via
   fixed ordinal rank) so they live on comparable scales before Min–Max if
   needed.
3. **Corpus Min–Max** — for **age**, **monthly_income**, **daily_learning_hours**,
   and encoded education/domain if treated as numeric in `[0,1]`, compute global
   `min_j`, `max_j` over the **entire corpus** (single pass or two passes), then
   `v_j = (x_j - min_j) / (max_j - min_j)` with guarded `max_j == min_j` → `0.0`.

**Rationale**: Spec assumes normalization by corpus; generator + pipeline keeps
memory bounded (streaming generator) while still allowing two-pass Min–Max when
building the index (documented trade-off).

**Alternatives considered**:

- Per-query normalization — changes distances between queries; rejected.
- Z-score — requires storing mean/std; acceptable but Min–Max matches spec
  example language.

---

## R-03 — Education and domain dissimilarity

**Decision**:

- **Education (`highest_degree`)**: Ordered categories mapped to integer ranks
  `0..E-1`; after Min–Max over corpus the coordinate behaves like other
  dimensions (absolute difference in normalized space reflects ordinal gap).
- **Domain (`favourite_domain`)**: Finite catalog; **same label → identical
  coordinate after encoding**. Different labels map to distinct normalized
  positions; contribution to distance is still via squared difference on that
  single dimension (approximates “0 vs gap” behavior). If strict “0 / constant
  penalty” is required, document as follow-up; v1 uses unified vector formula for
  simplicity and testability.

**Rationale**: One distance implementation (R-01) for all five dimensions;
easier equivalence tests between strategies.

**Alternatives considered**:

- Binary 0/1 same-domain flag with no Min–Max — closer to spec’s “constant for
  different categories”; deferred unless equivalence tests show mismatch with
  stakeholder expectations.

---

## R-04 — Top-k with `heapq`

**Decision**: While scanning candidates, maintain a **fixed-size** heap of the
**k largest distances seen so far among the best k** (max-heap via negated keys
or `heapq` with inverted comparison pattern). When a new candidate has distance
smaller than the worst in the heap, pop and push. Final sort of the k entries by
distance ascending, then apply **tie-break** by `profile_id` ascending.

**Rationale**: `heapq` is stdlib; per-insert `O(log k)`; total `O(n log k)` for
linear scan with `n` candidates.

**Alternatives considered**:

- Full sort `O(n log n)` — simpler but worse for large `n` and small `k`.
- `heapq.nsmallest(k, ...)` on full distance list — `O(n log k)` but needs full
  materialization of distances; acceptable for baseline on medium `n`; for 100k
  still fine; streaming heap preferred for uniformity.

---

## R-05 — Strategy pattern: baseline vs KD-tree

**Decision**:

- **`SearchStrategy`** (`abc.ABC`): methods `build(corpus_vectors)` and
  `search(query_vector, weights, k) -> list[SearchHit]` (exact names in
  implementation).
- **`BaselineScanner`**: `build` stores references to normalized profiles;
  `search` computes distance to **every** profile, uses heap top-k (R-04).
- **`KDTreeOptimizer`**: **5D KD-tree** partitioning on normalized coordinates;
  recursive split on median along cycling axis depth. **k-NN search** with
  branch-and-bound (hyper-rectangle distance to query) to prune subtrees; still
  uses the **same** `distance()` as baseline for all evaluated pairs.

**Rationale**: Satisfies FR-006 spatial partitioning; KD-tree is teachable and
pure-Python friendly without external libs.

**Alternatives considered**:

- Uniform grid — simpler but curse of dimensionality tuning; KD-tree chosen for
  coursework clarity.
- Ball tree — more code; rejected for v1.

---

## R-06 — Equivalence rules (FR-007)

**Decision**:

- Same corpus, query vector, weights, and `k` → both strategies return the **same
  ordered list** of `(profile_id, distance)`.
- Floating-point: distances compared with **absolute tolerance** `1e-9` for
  “equal distance”; ordering ties broken by **`profile_id` lexicographic /
  numeric ascending** so order is deterministic.
- Automated tests: property/synthetic cases where baseline answer is known; full
  corpus sweep on small `n` (e.g. `n <= 200`) comparing both strategies.

**Rationale**: Fair benchmarking (SC-003, SC-004) and clear failure signal if
  KD-tree pruning is buggy.

---

## R-07 — Timing & benchmarking (FR-009)

**Decision**: Use `time.perf_counter()` around `search(...)` only (exclude one-time
`build` unless separately reported). CLI or `main.py` prints JSON or text table:
strategy name, `n`, `k`, elapsed seconds, optional build time.

**Rationale**: Stdlib only; reproducible enough for coursework reports.

---

## R-08 — Orchestration entry point

**Decision**: Repository root **`main.py`** parses CLI args (stdlib
`argparse`), loads or generates corpus, builds selected strategy, runs query,
prints results and optional timings. Internal package under **`src/`** holds
library code so `main.py` stays thin.

**Rationale**: Matches user direction; keeps import path clear for tests
(`python -m` or `PYTHONPATH=src`).
