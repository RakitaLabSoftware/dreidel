import json
import os
import abc

from pydantic import BaseModel

__all__ = ["FeatureExtractor"]


class AFeatureExtractor(abc.ABC):
    @abc.abstractmethod
    def extract(self):
        pass

    @property
    def extract_strategy(self):
        """_summary_
        """
        return self._extract_strategy()

    @extract_strategy.setter
    def extract_strategy(self, extract_strategy):
        """_summary_
        """
        self._extract_strategy = extract_strategy