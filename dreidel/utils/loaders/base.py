import abc

from typing import Iterable

from dreidel.common.registry import Registry

LOAD_STRATEGY = Registry("LOAD_STRATEGY")


class LoadStrategy(abc.ABC):
    """Abstract class to specify methods to load data"""

    @property
    @abc.abstractmethod
    def items(self) -> Iterable:
        """Get items in folder/db."""

    @abc.abstractmethod
    def parse_item(self, item):
        """Parse current item from file/db."""

