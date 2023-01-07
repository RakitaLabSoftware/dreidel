from dreidel.modeling.aligner.step import StepAligner
import pytest


@pytest.fixture()
def aligner():
    return StepAligner(cfg=cfg)


def test_aligner():
    pass


def test_matcher(aligner):
    pass

