import abc
from ...common import Registry

__all__ = ["ADownloader", "DOWNLOADERS"]


class ADownloader(abc.ABC):
    @abc.abstractmethod
    def download(self, url: str, output: str) -> None:
        """
        _summary_
        
        Args:
            url (str): _description_
        """


DOWNLOADERS = Registry("DOWNLOADERS")
