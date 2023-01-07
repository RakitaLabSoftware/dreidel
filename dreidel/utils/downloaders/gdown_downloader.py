from pathlib import Path
import gdown
import zipfile
from .base import ADownloader


class GDownDownloader(ADownloader):
    def __init__(self, *, root: Path, quiet: bool = True) -> None:
        super().__init__()
        self.quiet = quiet
        self.root = root

    def _check_path(self, path: Path):
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)

    def download(self, url: str, output: Path | str) -> None:
        output_path = self.root / output
        self._check_path(output_path)
        filename = output_path / "data.zip"
        gdown.download(url=url, output=str(filename), quiet=self.quiet)
        with zipfile.ZipFile(filename, "r") as zip:
            zip.extractall(output_path)
        filename.unlink()
