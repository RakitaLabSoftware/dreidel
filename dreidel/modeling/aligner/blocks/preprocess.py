import abc
import cv2
import numpy as np
from dreidel.common.registry import Registry

__all__ = ["Preprocessor", "PREPROCESSORS"]

PREPROCESSORS = Registry("PREPROCESSORS")


class Preprocessor(abc.ABC):
    @abc.abstractmethod
    def run(self, img) -> np.ndarray:
        """Preprocess image before matching"""


class PreprocessorList(Preprocessor):
    def __init__(self, preprocessor_list: list[Preprocessor]):
        self.preprocessor_list = preprocessor_list

    def run(self):
        for preprocessor in self.preprocessor_list:
            yield preprocessor

    def __iter__(self):
        for preprocessor in self.preprocessor_list:
            yield preprocessor


class Canny(Preprocessor):
    def run(self, img):
        return cv2.Canny(img, 30, 60)


class TurnGray(Preprocessor):
    def run(self, img: np.ndarray) -> np.ndarray:
        return cv2.cvtColor(img, code=cv2.COLOR_BGR2GRAY)


if __name__ == "__main__":
    pass
