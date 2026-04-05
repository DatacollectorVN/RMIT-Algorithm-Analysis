"""Abstract search strategy interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence

from services.similarity.pipeline import NormalizedProfile


class SearchStrategy(ABC):
    """Builds an index from a corpus and answers weighted top-k queries."""

    @abstractmethod
    def build(self, corpus: Sequence[NormalizedProfile]) -> None:
        """Load or construct internal state from normalized profiles.

        Args:
            corpus: Non-empty sequence of normalized profiles.
        """

    @abstractmethod
    def search(
        self,
        query_vector: tuple[float, float, float, float, float],
        weights: tuple[float, float, float, float, float],
        k: int,
    ) -> list[tuple[str, float]]:
        """Return up to ``k`` best neighbors as ``(profile_id, distance)``.

        Results are sorted by ascending distance, then ``profile_id``.
        """
