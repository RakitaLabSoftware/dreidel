import abc
from typing import Any


class AlignmentBlock(abc.ABC):
    @abc.abstractmethod
    def run(self) -> Any:
        pass

    @abc.abstractmethod
    def show(self):
        pass
