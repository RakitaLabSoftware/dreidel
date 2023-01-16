import abc
from typing import Any


class App(abc.ABC):
    def run(self, *args, **kwargs) -> Any:
        """
        _summary_

        Returns
        -------
        Any
            _description_
        """
