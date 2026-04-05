"""Baseline vs KD-tree equivalence on synthetic corpora."""

import unittest

from services.search.strategies.baseline import BaselineScanner
from services.search.strategies.kdtree import KDTreeOptimizer
from services.similarity.pipeline import build_normalized_corpus, iter_synthetic_profiles


class TestEquivalence(unittest.TestCase):
    def test_multiple_seeds(self) -> None:
        w = (1.0, 2.0, 0.5, 1.5, 1.0)
        for seed in (0, 1, 42, 99):
            raw = list(iter_synthetic_profiles(80, seed=seed))
            norm, stats = build_normalized_corpus(raw)
            base = BaselineScanner()
            tree = KDTreeOptimizer()
            base.build(norm)
            tree.build(norm)
            q_raw = raw[0]
            from services.similarity.pipeline import normalize_query_raw

            qv = normalize_query_raw(q_raw, stats)
            for k in (1, 5, 20, 50):
                hb = base.search(qv, w, k)
                hk = tree.search(qv, w, k)
                self.assertEqual(hb, hk, msg=f"seed={seed} k={k}")


if __name__ == "__main__":
    unittest.main()
