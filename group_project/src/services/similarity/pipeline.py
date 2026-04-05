"""Synthetic profile generation, categorical encoding, and Min–Max normalization."""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Final, Iterator, Sequence

from services.core.exceptions import ValidationError
from services.helper import VECTOR_DIM, minmax_scalar

# Ordered education levels (ordinal index = rank for encoding).
DEGREE_CATALOG: Final[tuple[str, ...]] = (
    "none",
    "certificate",
    "associate",
    "bachelor",
    "master",
    "doctorate",
    "postdoc",
)

# Finite professional domains (index used before Min–Max).
DOMAIN_CATALOG: Final[tuple[str, ...]] = (
    "software",
    "data_science",
    "finance",
    "healthcare",
    "education",
    "manufacturing",
    "retail",
    "research",
    "design",
    "operations",
)


@dataclass(frozen=True, slots=True)
class RawProfile:
    """One raw user record before normalization."""

    profile_id: str
    age: float
    monthly_income: float
    daily_learning_hours: float
    highest_degree: str
    favourite_domain: str


@dataclass(frozen=True, slots=True)
class NormalizedProfile:
    """Corpus point in [0, 1]^5 after Min–Max scaling."""

    profile_id: str
    vector: tuple[float, float, float, float, float]


@dataclass(frozen=True, slots=True)
class ScalingStats:
    """Per-dimension Min–Max parameters from a corpus."""

    mins: tuple[float, float, float, float, float]
    maxs: tuple[float, float, float, float, float]


def degree_to_rank(degree: str) -> float:
    """Map ``highest_degree`` string to ordinal rank as float.

    Args:
        degree: Label in :data:`DEGREE_CATALOG`.

    Raises:
        ValidationError: If degree is unknown.
    """
    try:
        return float(DEGREE_CATALOG.index(degree))
    except ValueError as exc:
        raise ValidationError(f"unknown highest_degree: {degree!r}") from exc


def domain_to_index(domain: str) -> float:
    """Map ``favourite_domain`` string to catalog index as float.

    Args:
        domain: Label in :data:`DOMAIN_CATALOG`.

    Raises:
        ValidationError: If domain is unknown.
    """
    try:
        return float(DOMAIN_CATALOG.index(domain))
    except ValueError as exc:
        raise ValidationError(f"unknown favourite_domain: {domain!r}") from exc


def raw_to_prevector(raw: RawProfile) -> tuple[float, float, float, float, float]:
    """Encode raw profile to five numeric features before Min–Max.

    Order: age, monthly_income, education_rank, daily_learning_hours, domain_index.
    """
    return (
        float(raw.age),
        float(raw.monthly_income),
        degree_to_rank(raw.highest_degree),
        float(raw.daily_learning_hours),
        domain_to_index(raw.favourite_domain),
    )


def apply_minmax(
    pre: tuple[float, float, float, float, float],
    stats: ScalingStats,
) -> tuple[float, float, float, float, float]:
    """Scale one pre-vector using corpus Min–Max stats."""
    return tuple(minmax_scalar(pre[i], stats.mins[i], stats.maxs[i]) for i in range(VECTOR_DIM))


def compute_scaling_stats(pre_vectors: Sequence[tuple[float, float, float, float, float]]) -> ScalingStats:
    """Compute per-dimension min and max over a sequence of pre-vectors.

    Args:
        pre_vectors: Non-empty sequence of 5-tuples.

    Raises:
        ValidationError: If sequence is empty.
    """
    if not pre_vectors:
        raise ValidationError("cannot compute scaling stats on empty corpus")
    mins = list(pre_vectors[0])
    maxs = list(pre_vectors[0])
    for row in pre_vectors[1:]:
        for i in range(VECTOR_DIM):
            mins[i] = min(mins[i], row[i])
            maxs[i] = max(maxs[i], row[i])
    return ScalingStats(
        mins=(mins[0], mins[1], mins[2], mins[3], mins[4]),
        maxs=(maxs[0], maxs[1], maxs[2], maxs[3], maxs[4]),
    )


def iter_synthetic_profiles(count: int, *, seed: int | None = None) -> Iterator[RawProfile]:
    """Yield ``count`` synthetic profiles (stdlib ``random`` only).

    Attributes:
        - age: integer in ``[18, 70]`` inclusive.
        - monthly_income: float in ``[5, 100]``.
        - daily_learning_hours: float in ``[0, 8]``.
        - highest_degree / favourite_domain: valid catalog entries.

    Args:
        count: Number of profiles (must be non-negative).
        seed: Optional RNG seed for reproducibility.

    Yields:
        :class:`RawProfile` instances with ids ``synth-0`` ...

    Raises:
        ValidationError: If count is negative.
    """
    if count < 0:
        raise ValidationError("count must be non-negative")
    rng = random.Random(seed)
    for i in range(count):
        yield RawProfile(
            profile_id=f"synth-{i}",
            age=float(rng.randint(18, 70)),
            monthly_income=rng.uniform(5.0, 100.0),
            daily_learning_hours=rng.uniform(0.0, 8.0),
            highest_degree=rng.choice(DEGREE_CATALOG),
            favourite_domain=rng.choice(DOMAIN_CATALOG),
        )


def build_normalized_corpus(raw_profiles: Sequence[RawProfile]) -> tuple[list[NormalizedProfile], ScalingStats]:
    """Two-pass Min–Max: encode, stats, then normalize (suitable for 100k+ rows).

    Args:
        raw_profiles: Non-empty sequence of raw profiles.

    Returns:
        Tuple of normalized profiles and the stats used (for query encoding).

    Raises:
        ValidationError: If corpus is empty or encoding fails.
    """
    if not raw_profiles:
        raise ValidationError("corpus must be non-empty")
    pre = [raw_to_prevector(r) for r in raw_profiles]
    stats = compute_scaling_stats(pre)
    normalized: list[NormalizedProfile] = []
    for r, pv in zip(raw_profiles, pre, strict=True):
        normalized.append(NormalizedProfile(r.profile_id, apply_minmax(pv, stats)))
    return normalized, stats


def normalize_query_raw(raw: RawProfile, stats: ScalingStats) -> tuple[float, float, float, float, float]:
    """Normalize a query :class:`RawProfile` with corpus :class:`ScalingStats`."""
    return apply_minmax(raw_to_prevector(raw), stats)
