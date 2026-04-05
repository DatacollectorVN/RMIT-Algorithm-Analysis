#!/usr/bin/env python3
"""CLI entry: generate or load corpus, run weighted top-k similarity search."""

from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

# Repo layout: group_project/src/main.py → import package ``services`` from ``src/``
_SRC_ROOT = Path(__file__).resolve().parent
if str(_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(_SRC_ROOT))

from services.io.jsonio import dump_json, load_corpus_json, load_query_json
from services.search.benchmark import timed_build, timed_search
from services.search.strategies.baseline import BaselineScanner
from services.search.strategies.kdtree import KDTreeOptimizer
from services.similarity.pipeline import build_normalized_corpus, iter_synthetic_profiles, normalize_query_raw


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Top-k weighted profile similarity search (stdlib only).")
    p.add_argument(
        "--strategy",
        choices=("baseline", "kdtree", "both"),
        default="baseline",
        help="Search strategy, or 'both' to compare baseline vs KD-tree with timings.",
    )
    p.add_argument("--generate", type=int, default=None, metavar="N", help="Generate N synthetic profiles.")
    p.add_argument("--corpus", type=str, default=None, help="Path to JSON corpus array.")
    p.add_argument("--query", type=str, required=True, help="Path to JSON query (reference, weights, k).")
    p.add_argument("--seed", type=int, default=None, help="RNG seed for --generate.")
    p.add_argument(
        "--benchmark",
        action="store_true",
        help="Include perf_counter timings in output / comparison summary.",
    )
    return p.parse_args(argv)


def _load_corpus(args: argparse.Namespace) -> list:
    if args.generate is not None and args.corpus is not None:
        raise SystemExit("Use only one of --generate or --corpus")
    if args.generate is not None:
        if args.generate < 1:
            raise SystemExit("--generate N requires N >= 1")
        return list(iter_synthetic_profiles(args.generate, seed=args.seed))
    if args.corpus is not None:
        return load_corpus_json(args.corpus)
    raise SystemExit("Provide --generate N or --corpus path")


def _hits_equal(
    a: list[tuple[str, float]],
    b: list[tuple[str, float]],
    tol: float = 1e-9,
) -> bool:
    if len(a) != len(b):
        return False
    for (ida, da), (idb, db) in zip(a, b, strict=True):
        if ida != idb:
            return False
        if not math.isclose(da, db, rel_tol=0.0, abs_tol=tol):
            return False
    return True


def run(argv: list[str] | None = None) -> int:
    """Parse args, execute search, print JSON to stdout; summary to stderr if benchmark."""
    args = _parse_args(argv)
    corpus_raw = _load_corpus(args)
    normalized, stats = build_normalized_corpus(corpus_raw)
    ref_raw, weights, k = load_query_json(args.query)
    query_vec = normalize_query_raw(ref_raw, stats)

    if args.strategy == "both":
        args.benchmark = True

    if args.strategy in ("baseline", "kdtree"):
        if args.strategy == "baseline":
            strat = BaselineScanner()
            name = "baseline"
        else:
            strat = KDTreeOptimizer()
            name = "kdtree"
        build_elapsed = 0.0
        if args.benchmark:
            build_elapsed = timed_build(strat, normalized)
        else:
            strat.build(normalized)
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

    base = BaselineScanner()
    tree = KDTreeOptimizer()
    b_build = k_build = 0.0
    if args.benchmark:
        b_build = timed_build(base, normalized)
        k_build = timed_build(tree, normalized)
    else:
        base.build(normalized)
        tree.build(normalized)
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
    if not _hits_equal(b_hits, k_hits):
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
    n = len(normalized)
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


if __name__ == "__main__":
    raise SystemExit(run())
