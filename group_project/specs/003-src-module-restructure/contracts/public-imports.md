# Contract: Public import paths (post–003 refactor)

**Feature**: [spec.md](../spec.md)  
**Purpose**: Single reference for supported `services.*` imports after layout consolidation.

## Supported paths (canonical)

| Capability | Import from |
|------------|-------------|
| Domain errors | `from services.helper import LookalikeSearchError, ValidationError` |
| Hit-list compare (baseline vs k-d tree) | `from services.helper import hits_equal` |
| Numeric / KD helpers | `from services.helper import VECTOR_DIM, minmax_scalar, …` |
| DTOs | `from services.dto import RawProfile, NormalizedProfile, ScalingStats` |
| JSON I/O | `from services.jsonio import dump_json, load_corpus_json, load_query_json` |
| Corpus bundle + normalization | `from services.dataset import Corpuses, build_normalized_corpus, iter_synthetic_profiles, normalize_query_raw, get_synthetic_corpus, get_synthetic_query, …` |
| Search strategies | `from services.search.strategies import BaselineSearcher, KDTreeSearcher, SearchStrategy` |
| Timing helpers | `from services.search.benchmark import timed_searcher_construct, timed_search` |

### `Corpuses` entry points

- **`Corpuses.from_json_path(path)`** — load corpus JSON → bundle (search CLI).
- **`Corpuses.from_raw(raw_profiles)`** — normalize in memory.
- **`Corpuses.from_normalized(...)`** — tests / hand-built corpora.
- **`Corpuses.iter_synthetic_profiles(...)`** — synthetic raw rows (generate-corpus).
- **`corpuses.load_query(query_path)`** — query JSON → `(query_vec, weights, k)`.
- **`corpuses.normalize_query(raw)`** — normalize a reference using bundle stats.
- Implementation helpers on **`Corpuses`** use a leading **`_`** (e.g. **`_raw_to_prevector`**); prefer module functions **`degree_to_rank`**, **`normalize_query_raw`**, **`build_normalized_corpus`**, etc. for a stable public API outside the class.
- **`get_synthetic_corpus(path)`** / **`get_synthetic_query(path, corpuses)`** — 002-compatible names; thin aliases in `dataset.py`.

## Deprecated / removed (MUST NOT appear in new code)

- `services.core` (package deleted)
- `services.io.jsonio` → use `services.jsonio`
- `services.similarity.pipeline` → use `services.dataset` and `services.dto`
- `DataBuilder` → use `Corpuses`
- `BaselineScanner` / `KDTreeOptimizer` → `BaselineSearcher` / `KDTreeSearcher`
- `timed_build` → `timed_searcher_construct`
- Corpus/query prep only in **`main.py`** → use **`services.dataset`** (`Corpuses` / **`get_synthetic_*`**)

## CLI / PYTHONPATH

Unchanged: run with `PYTHONPATH` including `group_project/src` (or project-documented equivalent).

## Compatibility

- On-disk JSON: **no version bump**; same files as 001/002 specs.
