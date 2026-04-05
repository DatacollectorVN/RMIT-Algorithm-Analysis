# Quickstart: 003 refactor (developer)

**Plan**: [plan.md](./plan.md)

## Commands (unchanged)

```bash
cd group_project
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
python -m unittest discover -s tests -p 'test_*.py'
python src/main.py generate-corpus --N 10 --seed 1
python src/main.py search --corpus /path/to/corpus.json --query /path/to/query.json --strategy baseline
```

## Import changes (cheat sheet)

```python
# Before → After
from services.core.exceptions import ValidationError
from services.helper import ValidationError  # same class, new location

from services.io.jsonio import load_corpus_json
from services.jsonio import load_corpus_json

from services.similarity.pipeline import NormalizedProfile, build_normalized_corpus
from services.dto import NormalizedProfile
from services.dataset import build_normalized_corpus
```

## `Corpuses` + searchers (Phase 8 / 9)

```python
from services.dataset import Corpuses, get_synthetic_corpus, get_synthetic_query
from services.search.strategies import BaselineSearcher, KDTreeSearcher
from services.helper import hits_equal

corpuses = Corpuses.from_json_path("corpus.json")  # or Corpuses.from_raw / from_normalized
query_vec, weights, k = corpuses.load_query("query.json")
# 002 names: get_synthetic_corpus(path), get_synthetic_query(path, corpuses)

baseline = BaselineSearcher(corpuses)
tree = KDTreeSearcher(corpuses)
b_hits = baseline.search(query_vec, weights, k)
k_hits = tree.search(query_vec, weights, k)
assert hits_equal(b_hits, k_hits)
```

## Verify refactor

```bash
grep -R "services\.core\|services\.io\|similarity\.pipeline" src tests --include="*.py"
# expect: no matches (except comments if any)
```
