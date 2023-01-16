from dreidel.apps.aligner.blocks.keypoint import build_keypoint_detector
from dreidel.apps.aligner.blocks.matcher import build_matcher
from dreidel.apps.aligner.blocks.preprocess import PREPROCESSORS, Preprocessor, Raw
from dreidel.apps.aligner.blocks.transformation import build_transform
from dreidel.apps.aligner.storage import StepStorage
from dreidel.apps.base import App
import matplotlib.pylab as plt

__all__ = ["Aligner"]


class Aligner(App):
    def __init__(self, cfg) -> None:
        super().__init__()
        self.build(cfg)

    def build_preprocessors(self, cfg) -> list[Preprocessor]:
        preprocessors = []
        preprocessors.append(Raw())
        for preprocessor_cfg in cfg.preprocess:
            preprocessors.append(PREPROCESSORS.build(preprocessor_cfg))
        return preprocessors

    def build_keypoint_detector(self, cfg):
        return build_keypoint_detector(cfg)

    def build_matcher(self, cfg):
        return build_matcher(cfg)

    def build_transformation(self, cfg):
        return build_transform(cfg)

    def build(self, cfg):
        # self.preprocessors = self.build_preprocessors(cfg.preprocessors)
        self.keypoint_detector = self.build_keypoint_detector(cfg.keypoint_detector)
        self.matcher = self.build_matcher(cfg.matcher)
        self.transform = self.build_transformation(cfg.transformation)

    def show_raw(self):
        plt.imshow(self.storage.src.raw)

    def show_preprocess(self):
        if self.storage.src.pr is not None:
            self.preprocessors.show(self.storage.src.pr)

    def show_keypoints(self):
        self.keypoint_detector.show()

    def show_matches(self):
        self.matcher.show()

    def show_transformed(self):
        self.transform.show()

    def _run(self, storage: StepStorage):
        src_pr = storage.src.raw.copy()
        tgt_pr = storage.tgt.raw.copy()
        for preprocessor in self.preprocesors:
            src_pr = preprocessor.run(src_pr)
            tgt_pr = preprocessor.run(tgt_pr)

        # detect keypoints
        storage.src.features = self.keypoint_detector.detect(src_pr)
        storage.tgt.features = self.keypoint_detector.detect(tgt_pr)

        # find matches
        storage.matches = self.matcher.match(
            src_features=storage.src.features, tgt_features=storage.tgt.features
        )

        # Transform image
        transformed_img = self.transform.transform(
            src=storage.src.raw, matches=storage.matches, shape=storage.tgt.raw.shape
        )

        return transformed_img

    def run(self, img, tgt):
        self.storage = Storage(src=img, tgt=tgt)
        transformed_img = self._run(self.storage)
        return transformed_img
