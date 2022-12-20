from pydantic import BaseModel

__all__ = ["RawData"]


class ExperimentConfig(BaseModel):
    args: str | None
    configfile: str | None
    configsectrion: str | None
    dataformat: str
    inputfiles: list[str]
    inputpatterns: None
    backgroundfile: str
    openmanual: bool
    listfiles: bool
    createconfig: str
    output: str
    mode: str
    wavelength: None
    rpoly: float
    qmaxinst: float
    composition: str
    bgscale: float
    qmin: float
    qmax: float
    rmin: float
    rmax: float
    rstep: float


class Attrs(BaseModel):
    Description: str
    LocalPointer: str
    type: str
    processor: str
    mode: str
    config: ExperimentConfig


class RawData(BaseModel):
    dims: list[str]
    attrs: Attrs
    data: list
