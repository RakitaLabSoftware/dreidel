from ...common import Registry
from ...common.factory import FuncFactory
from . import functional as F

EXTRACT_FUNCTIONS = Registry("EXTRACT_FUNCTIONS")


@EXTRACT_FUNCTIONS.register()
class DefaultFunctionFactory(FuncFactory):
    def build(self, cfg):
        return self.fn


EXTRACT_FUNCTIONS.register(DefaultFunctionFactory(F.ext_min))
EXTRACT_FUNCTIONS.register(DefaultFunctionFactory(F.ext_max))
EXTRACT_FUNCTIONS.register(DefaultFunctionFactory(F.ext_avg))
