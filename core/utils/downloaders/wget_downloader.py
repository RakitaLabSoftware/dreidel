from ...common.factory import ObjectFactory
from .base import DOWNLOADERS, ADownloader


class WgetDowloader(ADownloader):
    def download(self, url: str, output: str) -> None:
        return None


@DOWNLOADERS.register()
class WgetDownloader(ObjectFactory):
    def build(self, cfg) -> ADownloader:
        return WgetDowloader()
