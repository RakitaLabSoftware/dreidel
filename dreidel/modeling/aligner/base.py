from pathlib import Path
from typing import TypeVar

KPS = TypeVar("KPS")
DES = TypeVar("DES")


__all__ = ["Aligner"]
# class Features(NamedTuple):
#     kps: int
#     des: int


# @dataclass
# class Dummy(Generic[KPS, DES]):
#     raw: np.ndarray
#     pr: np.ndarray | None = None
#     # features: Features = field(default_factory=tuple)

#     def __post_init__(self):
#         self.raw = copy.copy(self.raw)


# @dataclass(slots=True)
# class AlignData(meta=DataObject):
#     src: Dummy
#     tgt: Dummy
#     pts: list = field(init=False, default_factory=list)
#     plots: list[None | np.ndarray] = field(init=False, default_factory=list)

#     def __enter__(self):
#         return self

#     def __exit__(self, q, k, v):
#         pass


class Aligner:
    def __init__(self, save_path: Path | None = None) -> None:
        super().__init__()
        if save_path is None:
            save_path = Path("output.png")
        self.save_path = save_path

    def build(self, cfg):
        pass
