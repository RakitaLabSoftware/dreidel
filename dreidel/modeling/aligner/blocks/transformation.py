import abc
from typing import Any
import cv2
from dreidel.common.registry import Registry

__all__ = ["TRANSFORMATIONS", "MatrixTransformation", "Tranformation"]

TRANSFORMATIONS = Registry("Transformations")


class Tranformation(abc.ABC):
    homography: Any
    warp: Any

    @abc.abstractmethod
    def run(self, src, matches, shape):
        pass


class MatrixTransformation(Tranformation):
    def __init__(self) -> None:
        super().__init__()
        # self.homography = Homography()
        # self.warp = Warp()

    def run(self, src, matches, shape):
        # Find the homography matrix.
        height, width = shape[0], shape[1]
        image = src.copy()
        homography, _ = cv2.findHomography(
            srcPoints=matches.src_points,
            dstPoints=matches.tgt_points,
            method=cv2.USAC_MAGSAC,
        )

        # Use this matrix to transform the
        transformed_img = cv2.warpAffine(image, homography, (shape.height, shape.width))
        return transformed_img


if __name__ == "__main__":
    pass
