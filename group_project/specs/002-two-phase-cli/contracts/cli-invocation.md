# CLI Contract: Subcommand workflow (002)

**Entrypoint**: `python src/main.py <subcommand> [options]` with `PYTHONPATH` including `group_project/src`.

**Example (optional runner)**: `uv run python src/main.py <subcommand> [options]` — same argv after `python`.

---

## Subcommand: `generate-corpus`

| Option | Required | Description |
|--------|----------|-------------|
| `--N` | Yes | Integer ≥ 1; number of synthetic profiles |
| `--seed` | No | Integer RNG seed for reproducibility |

**Working directory**: Output is rooted at **current working directory** (`Path.cwd()`).

**Filesystem**: Creates **`.rmit/corpus/YYYYMMDD_HHMMSS/`** (local timestamp) containing:

- **`corpus.json`** — UTF-8 JSON array of records (schema matches `load_corpus_json`).
- **`metadata.txt`** — lines `N=<n>` and `seed=<int>|null`.

**Stdout**: Two lines with **absolute** paths, e.g. `Corpus: …/corpus.json` and `Metadata: …/metadata.txt` (exact labels as implemented in `main.py`).

**Stderr**: empty on success.

**Exit code**: `0` on success; non-zero on validation / usage errors.

**Notes**: No `--corpus`, `--query`, `--strategy`, or `--benchmark` on this subcommand (unknown options error). There is **no** `--count` flag in the current implementation (only `--N`).

---

## Subcommand: `search`

| Option | Required | Description |
|--------|----------|-------------|
| `--corpus` | Yes | Path to UTF-8 JSON corpus array file |
| `--query` | Yes | Path to UTF-8 JSON query object (`reference`, `weights`, `k`) |
| `--strategy` | No | `baseline` (default), `kdtree`, or `both` |
| `--benchmark` | No | Flag only; if present, include timing fields / stderr summary |

**Stdout**: JSON with `strategy`, `hits`, optional `timing` (same shape as pre-subcommand search).

**Stderr**: Benchmark summary when applicable (`both` or `--benchmark`).

**Exit code**: `0` on success; `1` when `both` strategies disagree within tolerance; non-zero on errors.

**Notes**: No `--generate`, `--seed`, or generate-corpus-only options on this subcommand.

---

## Global behavior

- **Missing subcommand** or **unknown subcommand**: non-zero exit; print usage listing `generate-corpus` and `search`.
- **`run()` argv convention for tests**: first element is the subcommand name, e.g. `["generate-corpus", "--N", "10", "--seed", "1"]` or `["search", "--corpus", path, "--query", path, "--strategy", "baseline"]`.

---

## Internal preparation API (repository contract)

| Function | Inputs | Outputs |
|----------|--------|---------|
| `get_synthetic_corpus` | Corpus file path | `(list[NormalizedProfile], ScalingStats)` |
| `get_synthetic_query` | Query file path, `ScalingStats` | `(query_vector_5_tuple, weights_5_tuple, k)` |

Used only on the **search** subcommand path. **generate-corpus** does not call these.

---

## Equivalence

- For the same corpus file, query file, **k**, weights, and strategy, **search** results must match the pre-subcommand baseline within existing numerical tolerance (SC-003).
