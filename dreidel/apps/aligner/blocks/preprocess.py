import abc
import cv2
import numpy as np
from dreidel.apps.aligner.blocks.base import BaseBlock

from dreidel.common.registry import Registry

__all__ = ["Preprocessor", "PREPROCESSORS", "Raw"]

PREPROCESSORS = Registry("PREPROCESSORS")


class Preprocessor(BaseBlock):
    @abc.abstractmethod
    def preprocess(self, img) -> np.ndarray:
        """Preprocess image before matching"""


class PreprocessorList:
    pass


class Raw(Preprocessor):
    def preprocess(self, img) -> np.ndarray:
        return img


@PREPROCESSORS.add()
class Canny(Preprocessor):
    def preprocess(self, img):
        return cv2.Canny(img, 60, 120)


@PREPROCESSORS.add()
class SelectRoi(Preprocessor):
    def preprocess(self, img: np.ndarray):
        r = cv2.selectROI("select the area", img)
        return img[int(r[1]) : int(r[1] + r[3]), int(r[0]) : int(r[0] + r[2])]


@PREPROCESSORS.add()
class TurnGray(Preprocessor):
    def preprocess(self, img: np.ndarray) -> np.ndarray:
        return cv2.cvtColor(img, code=cv2.COLOR_BGR2GRAY)


def build_preprocessors(cfg):
    pass
