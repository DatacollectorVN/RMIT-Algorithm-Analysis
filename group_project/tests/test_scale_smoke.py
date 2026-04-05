"""Scale smoke: large synthetic corpus, both strategies complete."""

import os
import unittest

from services.search.strategies.baseline import BaselineScanner
from services.search.strategies.kdtree import KDTreeOptimizer
from services.similarity.pipeline import build_normalized_corpus, iter_synthetic_profiles


class TestScaleSmoke(unittest.TestCase):
    def test_ten_thousand_profiles(self) -> None:
        n = 10_000
        raw = list(iter_synthetic_profiles(n, seed=7))
        norm, stats = build_normalized_corpus(raw)
        w = (1.0, 1.0, 1.0, 1.0, 1.0)
        from services.similarity.pipeline import normalize_query_raw

        qv = normalize_query_raw(raw[100], stats)
        k = 10
        b = BaselineScanner()
        t = KDTreeOptimizer()
        b.build(norm)
        t.build(norm)
        hb = b.search(qv, w, k)
        hk = t.search(qv, w, k)
        self.assertEqual(hb, hk)

    @unittest.skipUnless(os.environ.get("RUN_HEAVY") == "1", "set RUN_HEAVY=1 for 100k local run")
    def test_hundred_thousand_profiles(self) -> None:
        n = 100_000
        raw = list(iter_synthetic_profiles(n, seed=11))
        norm, stats = build_normalized_corpus(raw)
        w = (1.0, 1.0, 1.0, 1.0, 1.0)
        from services.similarity.pipeline import normalize_query_raw

        qv = normalize_query_raw(raw[5000], stats)
        k = 5
        b = BaselineScanner()
        t = KDTreeOptimizer()
        b.build(norm)
        t.build(norm)
        self.assertEqual(b.search(qv, w, k), t.search(qv, w, k))


if __name__ == "__main__":
    unittest.main()
