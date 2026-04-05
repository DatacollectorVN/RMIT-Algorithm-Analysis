# Research: Two-Phase CLI (002)

## 1. CLI shape: subcommands vs flat flags *(revised)*

**Decision**: Use **`argparse` subparsers** with verbs **`generate-corpus`** and **`search`**. The first argument after the script selects the workflow; each subparser owns its options. This matches the updated feature spec and product-owner expectation (`uv run python src/main.py <command> …`).

**Rationale**: Structural separation—operators cannot pass search flags on the generate subcommand without argparse rejecting unknown options (after correct parser setup). Help text is grouped per workflow.

**Alternatives considered**:

- **Flat flags** (prior 002 draft): rejected after stakeholder update; harder to document and easier to combine incompatible flags in one argv.
- **Two entry scripts**: duplication; rejected.

## 2. Profile count flag: `--N` vs `--count`

**Decision** *(refined 2026-04-06)*: Only **`--N`** is implemented on **`generate-corpus`** (required). **`--count`** was removed from the parser to simplify the interface; docs/spec no longer promise a synonym.

**Rationale**: Current code and tests standardize on **`--N`**.

**Alternatives considered**:

- Restore **`--count`** as synonym: easy future addition if stakeholders want it again.

## 3. `get_synthetic_corpus` scope

**Decision**: **`search`** subcommand only. Implement `get_synthetic_corpus(corpus_path: str | Path) -> tuple[list[NormalizedProfile], ScalingStats]` as `load_corpus_json` + `build_normalized_corpus`. **generate-corpus** uses `iter_synthetic_profiles` + stdout JSON only.

**Rationale**: Aligns with FR-002 and FR-001 separation; no synthetic count on the search subcommand.

## 4. Generation stdout format

**Decision**: Emit a **JSON array** of corpus-shaped objects using `dump_json` (stable key order).

**Rationale**: SC-002 determinism and compatibility with `load_corpus_json` for the search subcommand.

## 5. Removing `sys.path` injection

**Decision**: No import-time `sys.path` mutation; document `PYTHONPATH=$(pwd)/src` (and `uv run` example in quickstart).

**Rationale**: Repository constraint; standard import hygiene.

## 6. Backward compatibility of flat flags

**Decision**: **Out of scope** for 002 per updated spec—tests and docs target subcommands only. A future shim could parse legacy `--generate` if needed.

**Rationale**: Single supported interface reduces maintenance; SC-003 still holds for equivalent *data* and *options* via new argv.
