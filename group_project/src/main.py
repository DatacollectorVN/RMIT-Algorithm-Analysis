#!/usr/bin/env python3
"""CLI entry: subcommands ``generate-corpus`` and ``search`` (top-k similarity).

- ``generate-corpus``: required ``--N``, optional ``--seed`` → writes ``corpus.json`` and
  ``metadata.txt`` under ``./.rmit/corpus/YYYYMMDD_HHMMSS/``; prints those absolute paths
  (no corpus JSON on stdout).
- ``search``: ``--corpus``, ``--query``, optional ``--strategy``, ``--benchmark``.

Imports assume ``PYTHONPATH`` includes the ``src`` directory (no runtime ``sys.path`` mutation).
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from dataclasses import asdict
from pathlib import Path

from services.dataset import Corpuses, iter_synthetic_profiles
from services.helper import hits_equal
from services.jsonio import dump_json
from services.search.benchmark import timed_search, timed_searcher_construct
from services.search.strategies.baseline import BaselineSearcher
from services.search.strategies.kdtree import KDTreeSearcher
from services.search.strategies.base import SearchStrategy
from services.args import build_parser

def _run_generate_corpus(args: argparse.Namespace) -> int:
    if args.n_profiles < 1:
        raise SystemExit("--N requires an integer >= 1")
    profiles = list(iter_synthetic_profiles(args.n_profiles, seed=args.seed))
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = Path.cwd() / ".rmit" / "corpus" / stamp
    out_dir.mkdir(parents=True, exist_ok=True)
    corpus_path = out_dir / "corpus.json"
    meta_path = out_dir / "metadata.txt"
    payload = dump_json([asdict(p) for p in profiles])
    corpus_path.write_text(payload, encoding="utf-8")
    seed_repr = "null" if args.seed is None else str(args.seed)
    meta_path.write_text(f"N={args.n_profiles}\nseed={seed_repr}\n", encoding="utf-8")
    print(f"Corpus: {corpus_path.resolve()}\nMetadata: {meta_path.resolve()}")
    return 0


def _run_search(args: argparse.Namespace) -> int:
    corpuses = Corpuses.from_json_path(args.corpus)
    query_vec, weights, k = corpuses.load_query(args.query)

    if args.strategy == "both":
        args.benchmark = True

    if args.strategy in ("baseline", "kdtree"):
        searcher_cls: SearchStrategy
        if args.strategy == "baseline":
            searcher_cls = BaselineSearcher
            name = "baseline"
        else:
            searcher_cls = KDTreeSearcher
            name = "kdtree"
        build_elapsed = 0.0
        if args.benchmark:
            strat, build_elapsed = timed_searcher_construct(searcher_cls, corpuses)
        else:
            strat = searcher_cls(corpuses)
        hits, search_elapsed = (
            timed_search(strat, query_vec, weights, k)
            if args.benchmark
            else (strat.search(query_vec, weights, k), 0.0)
        )
        out: dict = {"strategy": name, "hits": [{"profile_id": h[0], "distance": h[1]} for h in hits]}
        if args.benchmark:
            out["timing"] = {"search_seconds": search_elapsed, "build_seconds": build_elapsed}
        print(dump_json(out))
        return 0

    b_build = k_build = 0.0
    if args.benchmark:
        base, b_build = timed_searcher_construct(BaselineSearcher, corpuses)
        tree, k_build = timed_searcher_construct(KDTreeSearcher, corpuses)
    else:
        base = BaselineSearcher(corpuses)
        tree = KDTreeSearcher(corpuses)
    b_hits, b_search = (
        timed_search(base, query_vec, weights, k)
        if args.benchmark
        else (base.search(query_vec, weights, k), 0.0)
    )
    k_hits, k_search = (
        timed_search(tree, query_vec, weights, k)
        if args.benchmark
        else (tree.search(query_vec, weights, k), 0.0)
    )
    if not hits_equal(b_hits, k_hits):
        print("Equivalence check FAILED: baseline vs kdtree differ", file=sys.stderr)
        print("baseline:", b_hits, file=sys.stderr)
        print("kdtree:", k_hits, file=sys.stderr)
        return 1
    print(
        dump_json(
            {
                "strategy": "both_match",
                "hits": [{"profile_id": h[0], "distance": h[1]} for h in b_hits],
                "timing": {
                    "baseline_build_seconds": b_build,
                    "baseline_search_seconds": b_search,
                    "kdtree_build_seconds": k_build,
                    "kdtree_search_seconds": k_search,
                },
            }
        )
    )
    n = len(corpuses.normalized)
    if k_search > 0.0:
        speedup = b_search / k_search
        summary = (
            f"\n[benchmark] corpus_size={n} k={k}\n"
            f"  Baseline: O(n) full scan — build {b_build:.6f}s, search {b_search:.6f}s\n"
            f"  KD-tree:  O(n log n) build typical; O(log n) average-case query vs O(n) scan — "
            f"build {k_build:.6f}s, search {k_search:.6f}s\n"
            f"  Search speedup (baseline_time / kdtree_time): {speedup:.2f}x\n"
        )
    else:
        summary = f"\n[benchmark] corpus_size={n} k={k}\n  KD-tree search time rounded to zero.\n"
    print(summary, file=sys.stderr)
    return 0


def run(argv: list[str] | None = None) -> int:
    """Parse argv, dispatch subcommand; ``search`` prints JSON; ``generate-corpus`` writes files and paths."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "generate-corpus":
        return _run_generate_corpus(args)
    return _run_search(args)


if __name__ == "__main__":
    raise SystemExit(run())
