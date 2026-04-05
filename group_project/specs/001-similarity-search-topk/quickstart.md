# Quickstart: Top-k profile similarity search

**Feature**: `001-similarity-search-topk`  
**Prerequisites**: Python **3.12+**, **stdlib only** (no `pip` dependencies).

## Layout

```text
group_project/
├── src/
│   ├── main.py
│   └── services/
│       ├── helper.py
│       ├── core/
│       ├── similarity/
│       ├── search/
│       │   └── strategies/
│       └── io/
└── tests/
```

## Environment

From the `group_project` directory:

```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
python -m unittest discover -s tests -p 'test_*.py'
```

## CLI examples

```bash
cd /path/to/group_project
export PYTHONPATH="$(pwd)/src"
python src/main.py --strategy baseline --generate 100000 --seed 42 --query query.json --benchmark
python src/main.py --strategy both --generate 50000 --seed 1 --query query.json
python src/main.py --strategy kdtree --corpus corpus.json --query query.json --benchmark
```

### Example `query.json`

```json
{
  "reference": {
    "profile_id": "q1",
    "age": 30,
    "monthly_income": 50.0,
    "daily_learning_hours": 3.0,
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
  "k": 10
}
```

## Heavy test (100k)

```bash
RUN_HEAVY=1 PYTHONPATH=src python -m unittest tests.test_scale_smoke.TestScaleSmoke.test_hundred_thousand_profiles
```

## Contracts

- `specs/001-similarity-search-topk/contracts/corpus-record.schema.json`
- `specs/001-similarity-search-topk/contracts/query-request.schema.json`
- `specs/001-similarity-search-topk/contracts/search-response.schema.json`
