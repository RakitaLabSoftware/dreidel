import abc
from typing import Any

import cv2
import matplotlib.pyplot as plt
import numpy as np

from dreidel.common.registry import Registry

from .base import AlignmentBlock

__all__ = ["KEYPOINT_DETECTORS", "KeypointDetector", "ORBDetector"]

KEYPOINT_DETECTORS = Registry("KEYPOINT_DETECTOR")


class KeypointDetector(AlignmentBlock):
    img: np.ndarray
    features: Any

    @abc.abstractmethod
    def run(self, img) -> tuple:
        """Detect keypoints"""

    def show(self):
        if getattr(self, "img", None) or getattr(self, "kps", None) is None:
            raise KeyError

        img_kps = cv2.drawKeypoints(
            self.img,
            self.features.kps,
            0,
            flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS,
        )
        plt.imshow(img_kps)
        return img_kps


class ORBDetector(KeypointDetector):
    def __init__(self, features: int, scale_factor: float) -> None:
        self.orb = cv2.ORB_create(
            nfeatures=features, scaleFactor=scale_factor, scoreType=cv2.ORB_HARRIS_SCORE
        )

    def run(self, img) -> tuple:
        self.img = img
        self.features = self.orb.detectAndCompute(img, None)
        return self.features
