# Quickstart: Two-Phase CLI (002) — subcommands

From `group_project/`:

```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

## Process 1 — Generate synthetic corpus

**`generate-corpus`** writes under **`.rmit/corpus/YYYYMMDD_HHMMSS/`** in the **current working directory** and prints absolute paths to **`corpus.json`** and **`metadata.txt`** (it does **not** stream JSON to stdout).

```bash
cd /path/to/your/run/directory
python /path/to/group_project/src/main.py generate-corpus --N 1000 --seed 42
# Then pass the printed corpus.json path to search, e.g.:
python /path/to/group_project/src/main.py search --corpus ./.rmit/corpus/20260406_120000/corpus.json --query query.json --strategy baseline
```

With **uv** (optional), from `group_project/`:

```bash
uv run python src/main.py generate-corpus --N 1000 --seed 42
```

## Process 2 — Run search

```bash
python src/main.py search --corpus /absolute/or/relative/path/to/corpus.json --query query.json --strategy both --benchmark
```

With **uv** (optional):

```bash
uv run python src/main.py search --corpus corpus.json --query query.json --strategy both --benchmark
```

## Verify tests

```bash
python -m unittest discover -s tests -p 'test_*.py'
```

Tests use a **temporary directory** as cwd so **`.rmit/`** output does not pollute the repo.
