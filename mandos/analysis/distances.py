"""
Calculations of concordance between annotations.
"""
import abc
import math
from collections import defaultdict
from typing import Collection, Sequence

import numpy as np

from mandos.analysis import AnalysisUtils as Au
from mandos.analysis import SimilarityDf
from mandos.model.hits import AbstractHit

# note that most of these math functions are much faster than their numpy counterparts
# if we're not broadcasting, it's almost always better to use them
# some are more accurate, too
# e.g. we're using fsum rather than sum


class MatrixCalculator(metaclass=abc.ABCMeta):
    def calc(self, hits: Sequence[AbstractHit]) -> SimilarityDf:
        raise NotImplemented()


class JPrimeMatrixCalculator(MatrixCalculator):
    def calc(self, hits: Sequence[AbstractHit]) -> SimilarityDf:
        inchikey_to_hits = Au.hit_multidict(hits, "origin_inchikey")
        data = defaultdict(dict)
        for (c1, hits1), (c2, hits2) in zip(inchikey_to_hits.items(), inchikey_to_hits.items()):
            data[c1][c2] = self._j_prime(hits1, hits2)
        return SimilarityDf.from_dict(data)

    def _j_prime(self, hits1: Collection[AbstractHit], hits2: Collection[AbstractHit]) -> float:
        sources = {h.data_source for h in hits1}.intersection({h.data_source for h in hits2})
        if len(sources) == 0:
            return np.nan
        values = [
            self._jx(
                [h for h in hits1 if h.data_source == source],
                [h for h in hits1 if h.data_source == source],
            )
            for source in sources
        ]
        return float(math.fsum(values) / len(values))

    def _jx(self, hits1: Collection[AbstractHit], hits2: Collection[AbstractHit]) -> float:
        pair_to_weights = Au.weights_of_pairs(hits1, hits2)
        values = [self._wedge(ca, cb) / self._vee(ca, cb) for ca, cb in pair_to_weights.values()]
        return float(math.fsum(values) / len(values))

    def _wedge(self, ca: float, cb: float) -> float:
        return math.sqrt(Au.elle(ca) * Au.elle(cb))

    def _vee(self, ca: float, cb: float) -> float:
        return Au.elle(ca) + Au.elle(cb) - math.sqrt(Au.elle(ca) * Au.elle(cb))


__all__ = ["MatrixCalculator", "JPrimeMatrixCalculator"]
