import abc
import numpy as np
import matplotlib.pyplot as plt


class BaseBlock(abc.ABC):
    @abc.abstractmethod
    def show(self):
        pass
