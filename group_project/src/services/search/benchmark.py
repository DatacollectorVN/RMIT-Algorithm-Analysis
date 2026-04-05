"""Wall-clock timing helpers for search and index build (stdlib ``time`` only)."""

from __future__ import annotations

import time
from collections.abc import Sequence

from services.search.strategies.base import SearchStrategy
from services.similarity.pipeline import NormalizedProfile


def timed_build(strategy: SearchStrategy, corpus: Sequence[NormalizedProfile]) -> float:
    """Call ``strategy.build(corpus)`` and return elapsed seconds."""
    t0 = time.perf_counter()
    strategy.build(corpus)
    return time.perf_counter() - t0


def timed_search(
    strategy: SearchStrategy,
    query_vector: tuple[float, float, float, float, float],
    weights: tuple[float, float, float, float, float],
    k: int,
) -> tuple[list[tuple[str, float]], float]:
    """Run ``strategy.search`` and return ``(hits, elapsed_seconds)``."""
    t0 = time.perf_counter()
    hits = strategy.search(query_vector, weights, k)
    elapsed = time.perf_counter() - t0
    return hits, elapsed
