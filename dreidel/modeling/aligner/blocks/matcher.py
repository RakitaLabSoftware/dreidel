import abc
import cv2
import numpy as np
from typing import Any
from dreidel.common.registry import Registry

MATCHERS = Registry("MATCHERS")
# TODO Visualise Matcher


class Matcher(abc.ABC):
    @abc.abstractmethod
    def run(self, src_features, tgt_features) -> list[Any]:
        """Match features"""

    def show(self):
        """_summary_
        """
        pass


class FlannMatcher(Matcher):
    def __init__(self, low_ratio: float, min_matches: int) -> None:
        super().__init__()
        self.matcher = cv2.FlannBasedMatcher()
        self.low_ratio = low_ratio
        self.min_matches = min_matches

    def _filter_matches(self, all_matches):
        for m, n in all_matches:
            if m.distance < self.low_ratio * n.distance:
                self.matches.append(m)
        # TODO refactor try ecxept

    def run(self, src_features, tgt_features):
        self.matches = []

        if src_features.des is not None and len(tgt_features.des) > 2:
            all_matches = self.matcher.knnMatch(src_features.des, tgt_features.des, k=2)

            self._filter_matches(all_matches)

        if len(self.matches) > self.min_matches:
            src_features.matched_pts = np.array(
                [src_features.kps[m.queryIdx].pt for m in self.matches]
            ).reshape(-1, 1, 2)
            tgt_features.matched_pts = np.array(
                [tgt_features.kps[m.trainIdx].pt for m in self.matches]
            ).reshape(-1, 1, 2)

        return self.matches


class BruteForceMatcher(Matcher):
    def __init__(self) -> None:
        super().__init__()

    def run(self):
        pass


if __name__ == "__main__":
    MATCHERS.add("FlannMatcher")
