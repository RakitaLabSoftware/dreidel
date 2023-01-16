import abc
import json
from pathlib import Path

from tqdm import tqdm

from dreidel.apps.extractors.builder import EXTRACT_FUNCTIONS
from ..base import App
from .schema import Feature, Values

__all__ = ["FeatureExtractor"]


class FeatureExtractor(App):
    def __init__(self, root: Path) -> None:
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)
        self.extractor = None

    def build_extractor(self, name):
        self.extractor_name = name
        self.extractor = EXTRACT_FUNCTIONS.get(name)

    def run(self, data: list) -> None:
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
