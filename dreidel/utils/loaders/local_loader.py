from .base import LoadStrategy
from typing import Type
from pydantic import BaseModel
import os
from ...common.data_structures import DataObject
from pathlib import Path


class LocalFileLoader(LoadStrategy):
    def __init__(self, root: Path, schema: Type[BaseModel]) -> None:
        super().__init__()
        self.root = root
        self.schema = schema

    @property
    def items(self) -> list[str]:
        return [file for file in os.listdir(self.root)]

    def parse_item(self, item):
        return self.schema.parse_file(item)
