from pydantic import BaseModel

__all__ = ["Features"]

class Value(BaseModel):
    x: int
    y: int
    value: float


class Feature(BaseModel):
    name: str
    extractor: str
    value: Value


class Features(BaseModel):
    min: Feature
    max: Feature
    avg: Feature
