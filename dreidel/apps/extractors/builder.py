from dreidel.common import Registry
from dreidel.common.factory import FuncFactory
from dreidel.apps.extractors import functional as F

EXTRACT_FUNCTIONS = Registry("EXTRACTORS")


class DefaultFunctionFactory(FuncFactory):
    def build(self, cfg):
        return self.fn


EXTRACT_FUNCTIONS.add(F.ext_min)
EXTRACT_FUNCTIONS.add(F.ext_max)
EXTRACT_FUNCTIONS.add(F.ext_avg)
