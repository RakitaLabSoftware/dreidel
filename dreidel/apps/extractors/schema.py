from pydantic import BaseModel, Field

__all__ = ["Feature", "Values"]


class Values(BaseModel):
    x: int
    y: int
    value: float


class Feature(BaseModel):
    value: list[Values]
    name: str | None = None
    extractor: str | None = None


class Features:
    min: Feature
    max: Feature
    avg: Feature
