# from dataclasses import dataclass, field

# from .factory import AbstractFactory

# __all__ = ["Registry"]

# FactoryType = TypeVar("FactoryType", bound=AbstractFactory)

# ObjectMap = Dict[str, "FactoryType"]


# @dataclass(frozen=True, slots=True)
# class Registry(Generic[FactoryType]):
#     name: str
#     obj_map: ObjectMap = field(init=False, default_factory=dict)

#     def _reg(self, name: str, factory: FactoryType) -> None:
#         try:
#             self.obj_map[name] = factory
#         except KeyError as e:
#             raise KeyError(e)

#     def register(self, factory: FactoryType | None = None) -> Any:
#         if factory is None:
#             # used as a decorator
#             def deco(func_or_class: Any) -> Any:
#                 name = func_or_class.name
#                 self._reg(name, func_or_class)
#                 return func_or_class

#             return deco

#         # used as a function call
#         name = factory.name
#         self._reg(name, factory)

#     def get(self, key: str) -> FactoryType:
#         ret = self.obj_map.get(key)
#         if ret is None:
#             raise KeyError(
#                 "No object named '{}' found in '{}' registry!".format(key, self.name)
#             )
#         return ret


from functools import singledispatchmethod
import inspect
from typing import Any, Dict, Generic, Iterable, Iterator, TypeVar


class Registry:
    def __init__(self, namespace: str) -> None:
        self.namespace = namespace
        self._obj_map = {}

    @singledispatchmethod
    def add(self, obj):
        if inspect.isclass(obj):
            self._obj_map[obj.__name__] = (
                obj,
                inspect.getfullargspec(obj.__init__),
                "this is class",
            )
        elif inspect.isfunction(obj):
            self._obj_map[obj.__name__] = (
                obj,
                inspect.getfullargspec(obj),
                "this is function",
            )

    @add.register
    def _(self, obj: None = None):
        pass

    def get(self, name):
        return self._obj_map[name]

    def list(self) -> Iterable[str]:
        """Returns list with names of all registered items."""
        return self._obj_map.keys()

    def __str__(self) -> str:
        """Returns a string of registered items."""
        return self.list().__str__()

    def __repr__(self) -> str:
        """Returns a string representation of registered items."""
        return self.list().__str__()

    def __len__(self) -> int:
        """Returns length of registered items."""
        return len(self._obj_map)

    def __getitem__(self, name: str) -> Any:
        """Returns a value from the registry by name."""
        return self.get(name)

    def __iter__(self) -> Iterator[str]:
        """Iterates over all registered items."""
        return self._obj_map.__iter__()

    def __contains__(self, name: str) -> bool:
        """Check if a particular name was registered."""
        return self._obj_map.__contains__(name)

    def __delitem__(self, name: str) -> None:
        """Removes object by giving name."""
        self._obj_map.pop(name)


if __name__ == "__main__":
    registry = NewRegistry("registry")

    class Dummy:
        def __init__(self, x, *, y: int = 5) -> None:
            pass

        def some_fn(self, z):
            pass

    def dummy_fn(a, b: int) -> float:
        return a / b

    registry.add(dummy_fn)
    registry.add(Dummy)

    dummy_cls = registry.get("Dummy")
    dummy_f = registry.get("dummy_fn")

    print(f"{dummy_f=}")
    print(f"{dummy_cls=}")
