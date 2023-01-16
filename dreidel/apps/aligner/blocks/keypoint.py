import cv2
import matplotlib.pyplot as plt
import numpy as np
from dreidel.common.registry import Registry

__all__ = ["KEYPOINT_DETECTORS", "KeypointDetector", "ORBDetector"]

KEYPOINT_DETECTORS = Registry("KEYPOINT_DETECTOR")


class KeypointDetector:
    def __init__(self, detect_strategy) -> None:
        self._detect_strategy = detect_strategy

    def detect(self, img) -> tuple:
        return self._detect_strategy.detectAndCompute(img, None)

    def show(self, img, kps) -> np.ndarray:
        img_kps = cv2.drawKeypoints(
            img, kps, 0, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
        )
        plt.imshow(img_kps)
        return img_kps


@KEYPOINT_DETECTORS.add()
class ORBDetector(KeypointDetector):
    def __init__(self, nfeatures: int, scale_factor: float) -> None:
        self._detector = cv2.ORB_create(nfeatures=nfeatures)


@KEYPOINT_DETECTORS.add()
class SIFTDetector(KeypointDetector):
    def __init__(self, nfeatures) -> None:
        self._detector = cv2.SIFT_create(nfeatures)


@KEYPOINT_DETECTORS.add()
class AKAZEDetector(KeypointDetector):
    def __init__(self, nfeatures) -> None:
        self._detector = cv2.AKAZE_create()


@KEYPOINT_DETECTORS.add()
class SURFDetector(KeypointDetector):
    def __init__(self, nfeatures) -> None:
        self._detector = cv2.xfeatures2d.SURF_create()


def build_keypoint_detector(cfg) -> KeypointDetector:
    detect_strategy = KEYPOINT_DETECTORS.build(**cfg.strategy)
    return KeypointDetector(detect_strategy)
