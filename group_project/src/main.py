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
import math
import sys
from datetime import datetime
from dataclasses import asdict
from pathlib import Path

from services.io.jsonio import dump_json, load_corpus_json, load_query_json
from services.search.benchmark import timed_build, timed_search
from services.search.strategies.baseline import BaselineScanner
from services.search.strategies.kdtree import KDTreeOptimizer
from services.similarity.pipeline import (
    NormalizedProfile,
    ScalingStats,
    build_normalized_corpus,
    iter_synthetic_profiles,
    normalize_query_raw,
)


def get_synthetic_corpus(corpus_path: str | Path) -> tuple[list[NormalizedProfile], ScalingStats]:
    """Load a corpus JSON file and return normalized profiles plus Min–Max stats.

    Used by the ``search`` subcommand only (not by ``generate-corpus``).

    Args:
        corpus_path: Path to a UTF-8 JSON array of corpus records.

    Returns:
        Tuple of normalized profiles and scaling statistics for query normalization.

    Raises:
        ValidationError: If JSON shape or values are invalid (from ``jsonio`` / ``pipeline``).
    """
    raw = load_corpus_json(corpus_path)
    return build_normalized_corpus(raw)


def get_synthetic_query(
    query_path: str | Path,
    stats: ScalingStats,
) -> tuple[tuple[float, float, float, float, float], tuple[float, float, float, float, float], int]:
    """Load query JSON and normalize the reference profile using corpus ``stats``.

    Args:
        query_path: Path to query object (``reference``, ``weights``, ``k``).
        stats: Min–Max stats from the corpus.

    Returns:
        ``(normalized_query_vector, weights_tuple, k)``.
    """
    ref_raw, weights, k = load_query_json(query_path)
    query_vec = normalize_query_raw(ref_raw, stats)
    return query_vec, weights, k


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="main.py",
        description="Top-k weighted profile similarity search (stdlib only).",
    )
    subs = p.add_subparsers(dest="command", required=True, help="Available commands")

    gen = subs.add_parser(
        "generate-corpus",
        help="Write N synthetic profiles to .rmit/corpus/YYYYMMDD_HHMMSS/corpus.json (+ metadata).",
    )
    gen.add_argument(
        "--N",
        type=int,
        dest="n_profiles",
        metavar="N",
        required=True,
        help="Number of synthetic profiles (integer ≥ 1).",
    )
    gen.add_argument("--seed", type=int, default=None, help="Optional RNG seed for reproducibility.")

    sea = subs.add_parser("search", help="Run weighted top-k similarity search.")
    sea.add_argument("--corpus", required=True, help="Path to JSON corpus array.")
    sea.add_argument("--query", required=True, help="Path to JSON query (reference, weights, k).")
    sea.add_argument(
        "--strategy",
        choices=("baseline", "kdtree", "both"),
        default="baseline",
        help="Search strategy (default: baseline).",
    )
    sea.add_argument(
        "--benchmark",
        action="store_true",
        help="Include perf_counter timings in output / stderr summary.",
    )
    return p


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
    normalized, stats = get_synthetic_corpus(args.corpus)
    query_vec, weights, k = get_synthetic_query(args.query, stats)

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


def run(argv: list[str] | None = None) -> int:
    """Parse argv, dispatch subcommand; ``search`` prints JSON; ``generate-corpus`` writes files and paths."""
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "generate-corpus":
        return _run_generate_corpus(args)
    return _run_search(args)


if __name__ == "__main__":
    raise SystemExit(run())
