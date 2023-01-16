from dreidel.apps.aligner.aligner_app import StepAligner
from omegaconf import OmegaConf
import pytest


def get_cfg():
    return OmegaConf.load("deafault.path")


@pytest.fixture()
def aligner():
    cfg = get_cfg()
    StepAligner(cfg=cfg)


def test_aligner():
    pass


def test_matcher(aligner):
    pass
