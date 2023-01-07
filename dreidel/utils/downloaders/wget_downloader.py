from ...common.factory import ObjectFactory
from .base import DOWNLOADERS, ADownloader


class WgetDownloader(ADownloader):
    def download(self, url: str, output: str) -> None:
        return None
