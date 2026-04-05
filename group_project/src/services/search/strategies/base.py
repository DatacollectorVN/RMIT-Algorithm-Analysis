"""Abstract search strategy interface."""

from __future__ import annotations

from abc import ABC, abstractmethod


class SearchStrategy(ABC):
    """Weighted top-k query over a corpus fixed at construction time."""

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
