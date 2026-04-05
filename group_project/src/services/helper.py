"""Shared numeric and geometry helpers (pure functions, no I/O)."""

from __future__ import annotations

# Fixed feature dimensionality for profiles / KD-tree.
VECTOR_DIM: int = 5

Vec5 = tuple[float, float, float, float, float]


def minmax_scalar(x: float, lo: float, hi: float) -> float:
    """Map ``x`` into ``[0, 1]`` using ``[lo, hi]``; constant dimension → ``0.0``."""
    if hi == lo:
        return 0.0
    return (x - lo) / (hi - lo)


def bbox_of_point(v: Vec5) -> tuple[Vec5, Vec5]:
    """Degenerate axis-aligned box for a single point."""
    return v, v


def union_bbox(
    lo1: tuple[float, ...],
    hi1: tuple[float, ...],
    lo2: tuple[float, ...],
    hi2: tuple[float, ...],
) -> tuple[tuple[float, ...], tuple[float, ...]]:
    """Merge two axis-aligned boxes (component-wise min/max)."""
    lo = tuple(min(lo1[i], lo2[i]) for i in range(VECTOR_DIM))
    hi = tuple(max(hi1[i], hi2[i]) for i in range(VECTOR_DIM))
    return lo, hi


def weighted_sq_dist_query_to_box(
    query: Vec5,
    weights: Vec5,
    lo: Vec5,
    hi: Vec5,
) -> float:
    """Lower bound on Σ w_i (q_i - p_i)² for any ``p`` inside ``[lo, hi]``."""
    total = 0.0
    for i in range(VECTOR_DIM):
        qi = query[i]
        if qi < lo[i]:
            t = qi - lo[i]
        elif qi > hi[i]:
            t = qi - hi[i]
        else:
            t = 0.0
        total += weights[i] * t * t
    return total
