import abc
from typing import Any, NamedTuple

from .blocks.keypoint import KEYPOINT_DETECTORS, KeypointDetector
from .blocks.matcher import MATCHERS, Matcher
from .blocks.preprocess import PREPROCESSORS, PreprocessorList
from .blocks.transformation import TRANSFORMATIONS, Tranformation

__all__ = ["StepAligner"]

# FIXME: rename
class FeaturesTuple(NamedTuple):
    kps: Any
    des: Any


class AlignRunner(abc.ABC):
    @abc.abstractmethod
    def run(self, src, tgt):
        pass


class DefaultRunner(AlignRunner):
    def __init__(
        self,
        preprocessors: PreprocessorList,
        keypoint_detector: KeypointDetector,
        matcher: Matcher,
        transformation: Tranformation,
        vis: bool = True,
    ) -> None:
        super().__init__()
        self.preprocesors = preprocessors
        self.keypoint_detector = keypoint_detector
        self.matcher = matcher
        self.transformation = transformation
        self.vis = vis

    def run(self, src, tgt):
        # FIXME: refactor this
        src_pr = src.copy()
        tgt_pr = tgt.copy()
        for preprocessor in self.preprocesors:
            src_pr = preprocessor.run(src_pr)
            tgt_pr = preprocessor.run(tgt_pr)

        # detect keypoints
        src_kps, src_des = self.keypoint_detector.run(src_pr)
        tgt_kps, tgt_des = self.keypoint_detector.run(tgt_pr)
        src_ft = FeaturesTuple(src_kps, src_des)
        tgt_ft = FeaturesTuple(tgt_kps, tgt_des)

        # find matches
        matches = self.matcher.run(src_features=src_ft, tgt_features=tgt_ft)

        # Transform image
        transformed_img = self.transformation.run(
            src=src, matches=matches, shape=tgt.shape
        )

        return transformed_img


class StepAligner:
    def __init__(self, cfg) -> None:
        super().__init__()
        self.build(cfg)

    def build_preprocessors(self, cfg):
        preprocessors = []
        for preprocessor in cfg.preprocessors:
            preprocessors.append(PREPROCESSORS.get(preprocessor))
        return PreprocessorList(preprocessors)

    def build_keypoint_detector(self, cfg):
        return KEYPOINT_DETECTORS.get(cfg.keypont_detector).build(cfg.keypointdetector)

    def build_matcher(self, cfg):
        return MATCHERS.get(cfg)

    def build_transformation(self, cfg):
        return TRANSFORMATIONS.get(cfg)

    def build(self, cfg):
        self.preprocessors = self.build_preprocessors(cfg)
        self.keypoint_detector = self.build_keypoint_detector(cfg)
        self.matcher = self.build_matcher(cfg)
        self.transformation = self.build_transformation(cfg)

        # TODO refactor runner
        self.runner = DefaultRunner(
            preprocessors=self.preprocessors,
            keypoint_detector=self.keypoint_detector,
            matcher=self.matcher,
            transformation=self.transformation,
        )

    def preprocess(self):
        self.preprocessors.run()

    def preprocess_show(self):
        self.preprocessors.show()

    def run(self, img, tgt):
        with Storage(src=img, tgt=tgt) as data:
            transformed_img = self.runner.run(data)
        return transformed_img

