import abc
import json
from pathlib import Path

from tqdm import tqdm

from dreidel.modeling.extractors.builder import EXTRACT_FUNCTIONS

from .schema import Feature, Values

__all__ = ["FeatureExtractor"]


class AFeatureExtractor(abc.ABC):
    @abc.abstractmethod
    def run(self):
        pass

    @property
    @abc.abstractmethod
    def extractor_name(self):
        """_summary_
        """

    @extractor_name.setter
    @abc.abstractmethod
    def extractor_name(self, extract_strategy):
        """_summary_
        """


class FeatureExtractor(AFeatureExtractor):
    def __init__(self, root: Path) -> None:
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    @property
    def extractor_name(self):
        return self._extractor_name

    @extractor_name.setter
    def extractor_name(self, extractor_name):
        self._extractor_name = extractor_name

    def get_extractor(self, name):
        return EXTRACT_FUNCTIONS.get(name).build({})

    def run(self, data: list) -> None:
        self.extractor = self.get_extractor(self.extractor_name)
        value_list = []
        for item in tqdm(data):
            value_list.append(
                Values(
                    value=self.extractor(item.data),
                    x=int(item.attrs.LocalPointer[-12:-8]),
                    y=int(item.attrs.LocalPointer[-7:-3]),
                )
            )
        self.schema = Feature(value=value_list)
        self.schema.name = "ped"
        self.schema.extractor = self.extractor_name
        self.save()

    def save(self):
        with open(self.root / f"{self.extractor_name}.json", "w+") as outfile:
            json.dump(self.schema.dict(), outfile, indent=4)

