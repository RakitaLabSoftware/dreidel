from dataclasses import dataclass, field
import numpy as np
from copy import copy


@dataclass
class AlignFeatures:
    kps: list[np.ndarray] | None = None
    des: list[np.ndarray] | None = None
    matched_pts: list[np.ndarray] | None = None


@dataclass
class ImgContainer:
    raw: np.ndarray
    pr: np.ndarray | None = field(default=None)
    features: AlignFeatures = field(default_factory=AlignFeatures)

    def __post_init__(self):
        self.raw = copy.copy(self.raw)


@dataclass
class Vis:
    prepocess_img: np.ndarray
    storage: np.ndarray
    keypoints: np.ndarray


class StepStorage:
    def __init__(self, src, tgt) -> None:
        self.src = ImgContainer(src)
        self.tgt = ImgContainer(tgt)
        self.matches = []
