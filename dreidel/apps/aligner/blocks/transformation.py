import abc
from typing import Any
import cv2
from dreidel.common.registry import Registry
import numpy as np

__all__ = ["TRANSFORMATIONS", "MatrixTransformation", "Tranformation"]

TRANSFORMATIONS = Registry("Transformations")
WARPINGS = Registry("Warpings")


class Warp(abc.ABC):
    @abc.abstractmethod
    def warp(self, image: np.ndarray, transformation_matrix: np.ndarray, shape: tuple):
        pass


@TRANSFORMATIONS.add()
class AfinneWarp(Warp):
    def warp(self, image, transformation_matrix, shape):
        return cv2.warpAffine(image, transformation_matrix, shape)


@TRANSFORMATIONS.add()
class PerspectiveWarp(Warp):
    def warp(self, image: np.ndarray, transformation_matrix: np.ndarray, shape: tuple):
        return cv2.warpPerspective(image, transformation_matrix, shape)


class MatrixTransformation:
    def __init__(self, transforms) -> None:
        super().__init__()
        self.transforms = transforms

    def transform(self, src, src_features, tgt_features, shape):
        # Find the homography matrix.
        image = src.copy()

        # FIXME: Should I use Homography or affine would be enough. Sould I apply it sequentially?
        M = cv2.getAffineTransform(
            src_features.matched_pts,
            tgt_features.matched_pts,
        )
        self.transforms.warp(image, M, shape)
        return PerspectiveWarp().warp(image, M, shape)


def build_transform(cfg):
    transformation_strategy = TRANSFORMATIONS.build(**cfg.strategy)
    return MatrixTransformation(transforms=transformation_strategy)
