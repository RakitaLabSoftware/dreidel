import gdown
from pathlib import Path
from .base import ADownloader


class GDownDowloader(ADownloader):
    def __init__(self, *, root: Path, quiet: bool = True) -> None:
        super().__init__()
        self.quiet = quiet
        self.root = root

    def download(self, url: str, output: Path) -> None:
        output_path = self.root / output
        gdown.download(url=url, output=output_path, quiet=self.quiet)
