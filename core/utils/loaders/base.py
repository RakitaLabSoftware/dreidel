import abc

from typing import Iterable

from ...common import Registry

LOAD_STRATEGY = Registry("LOAD_STRATEGY")


class LoadStrategy(abc.ABC):
    """Abstract class to specify methods to load data"""

    @abc.abstractmethod
    def get_items(self) -> Iterable:
        """Get items in folder/db."""

    @abc.abstractmethod
    def parse(self, item):
        """Parse current item from file/db."""

