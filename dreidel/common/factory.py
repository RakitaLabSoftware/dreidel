import abc
from typing import Any, Callable

from pydantic import BaseModel

__all__ = ["ObjectFactory", "AbstractFactory"]

Function = Callable[..., Any]


class AbstractFactory(abc.ABC):
    @abc.abstractmethod
    def build(self, cfg: BaseModel):
        pass

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Name of object produced by factory"""
        pass


class ObjectFactory(AbstractFactory):
    def __init__(self, obj) -> None:
        super().__init__()
        self.obj = obj

    @property
    def name(self):
        return self.obj.__class__.__name__


class FuncFactory(AbstractFactory):
    def __init__(self, fn: Function) -> None:
        super().__init__()
        self.fn = fn

    @property
    def name(self) -> str:
        return self.fn.__name__
