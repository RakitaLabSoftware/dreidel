import abc
import cv2
import numpy as np
from typing import Any
from dreidel.common.registry import Registry
import matplotlib.pyplot as plt

__all__ = ["MATCHERS"]

MATCHERS = Registry("MATCHERS")


class Matcher:
    def __init__(self, match_strategy, lowes_ratio: float, n_matches: int) -> None:
        self._match_strategy = match_strategy
        self.lowes_ratio = lowes_ratio
        self.n_matches = n_matches

    def _match(self, src_features, tgt_features) -> Any:
        self._match_strategy.knnMatch(src_features.des, tgt_features.des, k=2)

    def _number_filter_matches(self, matches, src_feat, tgt_feat):
        if len(matches) > self.n_matches:
            src_feat.matched_pts = np.array(
                [src_feat.kps[m.queryIdx].pt for m in matches]
            ).reshape(-1, 1, 2)
            tgt_feat.matched_pts = np.array(
                [tgt_feat.kps[m.trainIdx].pt for m in matches]
            ).reshape(-1, 1, 2)

    def _distance_filter_matches(self, matches) -> list[np.ndarray]:
        filtered_matches = []
        try:
            for m, n in matches:
                if m.distance < self.lowes_ratio * n.distance:
                    filtered_matches.append(m)
        except ValueError as e:
            print(e)
        return filtered_matches

    def match(self, src_features, tgt_features) -> Any:
        if src_features.des is None and len(tgt_features.des) < 2:
            return None

        matches = self._match(src_features, tgt_features)
        matches = self._distance_filter_matches(matches)
        matches = self._number_filter_matches(matches, src_features, tgt_features)
        return matches, src_features, tgt_features

    def show(self, src, src_kps, tgt, tgt_kps, matches) -> None:
        img_matches = cv2.drawMatches(
            src, src_kps, tgt, tgt_kps, matches, None, flags=2
        )
        plt.imshow(img_matches)


@MATCHERS.add()
class FlannMatcher(Matcher):
    def __init__(self, **kwargs) -> None:
        self.matcher = cv2.FlannBasedMatcher(**kwargs)


@MATCHERS.add()
class BruteForceMatcher(Matcher):
    def __init__(self) -> None:
        self.matcher = cv2.BFMatcher()


def build_matcher(cfg):
    match_strategy = MATCHERS.build(**cfg.strategy)
    return Matcher(match_strategy, cfg.lowes_ratio, cfg.n_matches)
