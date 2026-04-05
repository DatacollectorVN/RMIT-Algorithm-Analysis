# Data Model: Two-Phase CLI (002)

This feature does **not** introduce new persisted entities; it reuses types from `services.similarity.pipeline` and JSON contracts from `services.io.jsonio`.

## Entities

### RawProfile (existing)

- **Purpose**: One user record before normalization / one corpus row.
- **Fields**: `profile_id` (str), `age`, `monthly_income`, `daily_learning_hours` (float), `highest_degree`, `favourite_domain` (str catalog labels).
- **Validation**: Enforced on JSON load via `load_corpus_json` / `load_query_json` (`reference` uses same shape as a corpus row).

### NormalizedProfile (existing)

- **Purpose**: Corpus point in scaled feature space for distance + indexes.
- **Fields**: `profile_id`, `vector` (5-tuple float in [0, 1] per dimension after Min–Max using corpus stats).

### ScalingStats (existing)

- **Purpose**: Per-dimension min/max from the corpus pre-vectors; required to normalize the query reference consistently.

### Query document (JSON object, existing)

- **Fields**:
  - `reference`: object with same keys as a corpus record.
  - `weights`: object with keys `age`, `monthly_income`, `education`, `daily_learning_hours`, `domain` (floats).
  - `k`: positive integer (≥ 1).

## Relationships

- **generate-corpus** writes **`corpus.json`** (JSON array, corpus record shape) under **`.rmit/corpus/YYYYMMDD_HHMMSS/`**; **search** loads that path (or any compatible file) via `load_corpus_json`.
- **search** loads corpus from disk → `NormalizedProfile` list + `ScalingStats` → loads query → normalizes `reference` → strategies run.

## State transitions

- **None** (stateless process). Each invocation either writes timestamped files under **`.rmit/corpus/`** plus path lines on stdout, or runs **search** (stdout result JSON, optional stderr benchmark).

## Validation rules (feature-specific)

| Rule | Enforcement |
|------|-------------|
| Missing or unknown **subcommand** | CLI error + usage |
| **generate-corpus**: **N** from `--N` must be ≥ 1 | `SystemExit` / parser error |
| **search** without `--corpus` or `--query` | `SystemExit` naming missing option |
| Malformed JSON / schema | `ValidationError` from `jsonio` / `pipeline` (non-zero exit per existing behavior) |
