from pathlib import Path
from typing import Any, Iterable

from pydantic import BaseModel

from .base import LoadStrategy


class DBNODE(BaseModel):
    db_root: Path
    db_schema: BaseModel


class DataBaseLoader(LoadStrategy):
    def __init__(self, db_root, db_schema) -> None:
        super().__init__()
        self.db_root = db_root
        self.db_schema = db_schema

    def get_items(self) -> Iterable:
        return []

    def parse(self, item) -> Any:
        return
