"""Exhaustive O(n) scan baseline for top-k similarity."""

from __future__ import annotations

from collections.abc import Sequence

from services.core.exceptions import ValidationError
from services.search.distance import weighted_squared_distance
from services.search.strategies.base import SearchStrategy
from services.search.topk import finalize_top_k, push_top_k
from services.similarity.pipeline import NormalizedProfile


class BaselineScanner(SearchStrategy):
    """Full dataset scan with weighted distance and heap top-k."""

    __slots__ = ("_corpus",)

    def __init__(self) -> None:
        self._corpus: list[NormalizedProfile] = []

    def build(self, corpus: Sequence[NormalizedProfile]) -> None:
        if not corpus:
            raise ValidationError("corpus must be non-empty for BaselineScanner")
        self._corpus = list(corpus)

    def search(
        self,
        query_vector: tuple[float, float, float, float, float],
        weights: tuple[float, float, float, float, float],
        k: int,
    ) -> list[tuple[str, float]]:
        if k < 1:
            raise ValidationError("k must be at least 1")
        heap: list = []
        for p in self._corpus:
            d = weighted_squared_distance(query_vector, p.vector, weights)
            push_top_k(heap, d, p.profile_id, k)
        return finalize_top_k(heap)
