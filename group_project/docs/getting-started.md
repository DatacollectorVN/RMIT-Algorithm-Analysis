# Getting started — CLI and developer workflow

This document is for developers working in **`group_project`**. It covers environment setup, every CLI option, input/output behavior, and how to run tests.

## Prerequisites

- **Python 3.12+**
- **Application runtime** uses the **standard library only** (`json`, `argparse`, `unittest`, `dataclasses`, etc.) — no required PyPI packages for executing the CLI or course deliverables.
- **Optional**: [uv](https://docs.astral.sh/uv/) plus the **`dev`** extra in `pyproject.toml` for pytest, coverage, Black, Ruff, Flake8, isort, and Pyrefly.

## Environment

### A. Plain Python (`PYTHONPATH`)

Python must resolve the `services` package. From the **`group_project`** directory:

```bash
cd group_project
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

Use the same `PYTHONPATH` when running tests or invoking `main.py` **unless** you use **uv** (below), which puts `src` on the path for `uv run pytest`.

Optional: add the `export` line to your shell profile if you work on this repo often.

### B. uv (optional dev environment)

```bash
cd group_project
uv sync --extra dev
```

This creates **`.venv`**, installs the **`rmit-group-project`** package in editable mode (the `services` package from `src/services`), and installs linters/formatters/test tools.

Common commands:

```bash
uv run pytest
uv run black src tests
uv run ruff check src tests
uv run ruff format src tests
uv run isort src tests
uv run flake8 src tests
uv run pyrefly check src
uv run python src/main.py --help
uv run python -m unittest discover -s tests -p 'test_*.py'
```

Coverage reports (HTML) are written to **`htmlcov/`** when using the default pytest `addopts` in `pyproject.toml`.

## CLI overview

The entry point is **`src/main.py`**. It exposes two subcommands:

| Subcommand | Purpose |
|------------|---------|
| **`generate-corpus`** | Create a synthetic corpus on disk under `.rmit/corpus/<timestamp>/`. |
| **`search`** | Load a corpus and query from JSON, run top-k similarity search, print results as JSON. |

Global help:

```bash
python src/main.py --help
```

Help per subcommand:

```bash
python src/main.py generate-corpus --help
python src/main.py search --help
```

---

## `generate-corpus`

Writes **`corpus.json`** (JSON array of profiles) and **`metadata.txt`** (run parameters) under:

```text
<current working directory>/.rmit/corpus/YYYYMMDD_HHMMSS/
```

### Arguments

| Option | Required | Description |
|--------|----------|-------------|
| **`--N`** | Yes | Number of synthetic profiles; integer **≥ 1**. |
| **`--seed`** | No | Integer seed for `random.Random`; omit for non-deterministic runs. |

### Example

```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
python src/main.py generate-corpus --N 100 --seed 42
```

### Log output (corpus paths)

`generate-corpus` logs two lines at **INFO** with **absolute paths** (default handler: **stderr** when `main.py` configures logging):

```text
Corpus: /path/to/.rmit/corpus/20260405_120000/corpus.json
Metadata: /path/to/.rmit/corpus/20260405_120000/metadata.txt
```

Exit code **`0`** on success. Invalid **`--N`** (not an integer ≥ 1) exits with an error message.

### Corpus file shape

Each element is an object with:

- `profile_id` (string)
- `age` (number)
- `monthly_income` (number)
- `daily_learning_hours` (number)
- `highest_degree` (string — must be encodable when used with search; synthetic data uses built-in catalogs)
- `favourite_domain` (string)

---

## `search`

Loads a corpus and a query, normalizes the reference profile with the **same Min–Max statistics** as the corpus, then returns the **k** nearest profiles by **weighted squared Euclidean distance** in normalized feature space.

### Arguments

| Option | Required | Description |
|--------|----------|-------------|
| **`--corpus`** | Yes | Path to UTF-8 JSON **array** of corpus records (same shape as generated corpus objects). |
| **`--query`** | Yes | Path to UTF-8 JSON **object** with `reference`, `weights`, and `k` (see below). |
| **`--strategy`** | No | `baseline` (default), `kdtree`, or `both`. |
| **`--benchmark`** | No | Flag: include `perf_counter` timings in the JSON (single-strategy modes only). |

### Examples

Baseline search (default):

```bash
python src/main.py search --corpus path/to/corpus.json --query path/to/query.json
```

KD-tree:

```bash
python src/main.py search --corpus path/to/corpus.json --query path/to/query.json --strategy kdtree
```

Baseline with timings:

```bash
python src/main.py search --corpus path/to/corpus.json --query path/to/query.json --strategy baseline --benchmark
```

Run **both** strategies, check results match, then log JSON plus a human-readable benchmark summary (both at **INFO**):

```bash
python src/main.py search --corpus path/to/corpus.json --query path/to/query.json --strategy both
```

### Log output (JSON)

Search results are logged at **INFO** as a single message (pretty-printed JSON), not written to raw stdout. With the default **`logging.basicConfig`** in **`main.py`**, that usually appears on **stderr**.

**`baseline`** / **`kdtree`**: one JSON object, e.g.:

```json
{
  "strategy": "baseline",
  "hits": [
    { "profile_id": "p1", "distance": 0.12 },
    { "profile_id": "p2", "distance": 0.45 }
  ]
}
```

With **`--benchmark`**, a **`timing`** object is added:

```json
"timing": {
  "search_seconds": 0.000123,
  "build_seconds": 0.000045
}
```

**`both`**: `strategy` is **`both_match`**, same `hits` as baseline (verified against KD-tree), and **`timing`** includes separate baseline and k-d tree build/search seconds. A second **INFO** log line carries the benchmark summary (corpus size, k, timings, speedup).

To capture output in scripts, add a **`logging.Handler`** (e.g. **`StreamHandler`** to a **`StringIO`**) on the **`services.runner`** logger, or parse the default log stream.

### Query JSON shape

Top-level object with three keys:

1. **`reference`** — same object shape as one corpus row (raw features).
2. **`weights`** — object with exactly these keys (order in file does not matter; values are read in this order):

   - `age`
   - `monthly_income`
   - `education` (weight on the encoded degree dimension)
   - `daily_learning_hours`
   - `domain` (weight on the encoded favourite_domain dimension)

3. **`k`** — positive integer (at least **1**).

Minimal example:

```json
{
  "reference": {
    "profile_id": "q0",
    "age": 30.0,
    "monthly_income": 50.0,
    "daily_learning_hours": 2.0,
    "highest_degree": "bachelor",
    "favourite_domain": "software"
  },
  "weights": {
    "age": 1.0,
    "monthly_income": 1.0,
    "education": 0.5,
    "daily_learning_hours": 1.0,
    "domain": 1.0
  },
  "k": 3
}
```

Invalid JSON, missing keys, or bad **`k`** raise errors; the CLI exits with code **`1`** and logs the error (logging must be configured if you want INFO on stderr; errors use the root logger when `main.py` calls `basicConfig`).

---

## Running tests

**unittest** (matches course / spec workflow; no extra packages):

```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
python -m unittest discover -s tests -p 'test_*.py'
```

Verbose:

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
```

**pytest** (optional; requires `uv sync --extra dev` or an equivalent env with dev dependencies):

```bash
uv run pytest
```

---

## Using the library from Python

Same `PYTHONPATH` as above, then import from `services`, for example:

```python
from services.dataset import Corpuses
from services.search.strategies import BaselineSearcher

corpuses = Corpuses.from_json_path("corpus.json")
q, w, k = corpuses.load_query("query.json")
searcher = BaselineSearcher(corpuses)
hits = searcher.search(q, w, k)  # list[tuple[str, float]]
```

Canonical import paths are summarized in **`specs/003-src-module-restructure/contracts/public-imports.md`**.

---

## End-to-end snippet

```bash
cd group_project
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

python src/main.py generate-corpus --N 20 --seed 1
# Copy the printed corpus path, then create query.json (see shape above).

python src/main.py search --corpus "<paste-corpus-path>" --query query.json --strategy both
```

---

## Further reading

- [README.md](../README.md) — high-level architecture and module map.
- `specs/` — feature requirements and design notes for similarity search and layout refactors.
