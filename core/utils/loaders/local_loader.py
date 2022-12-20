from .base import LoadStrategy
from typing import Type
from pydantic import BaseModel
import os


class LocalFileLoader(LoadStrategy):
    def __init__(self, root: str, schema: Type[BaseModel]) -> None:
        super().__init__()
        self.root = root
        self.schema = schema

    def get_items(self) -> list[str]:
        return [file for file in os.listdir(self.root)]

    def parse(self, item):
        return self.schema.parse_file(item)
