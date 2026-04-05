"""Profile generation, encoding, and Min–Max normalization."""

from services.similarity.pipeline import (
    NormalizedProfile,
    RawProfile,
    ScalingStats,
    build_normalized_corpus,
    iter_synthetic_profiles,
    normalize_query_raw,
)

__all__ = [
    "RawProfile",
    "NormalizedProfile",
    "ScalingStats",
    "build_normalized_corpus",
    "iter_synthetic_profiles",
    "normalize_query_raw",
]
