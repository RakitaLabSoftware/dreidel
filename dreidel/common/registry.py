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


import inspect
from typing import Any, Iterable, Iterator


def default_build_func(obj, *args, **kwargs):
    return obj(*args, **kwargs)


class Registry:
    def __init__(self, namespace: str, builder=default_build_func) -> None:
        self.namespace = namespace
        self.build_func = builder
        self._obj_map = dict()

    def add(self, name=None, force=False, module=None):
        """Register a module.
        A record will be added to `self._module_dict`, whose key is the class
        name or the specified name, and value is the class itself.
        It can be used as a decorator or a normal function.
        Example:
            >>> backbones = Registry('backbone')
            >>> @backbones.register_module()
            >>> class ResNet:
            >>>     pass
            >>> backbones = Registry('backbone')
            >>> @backbones.register_module(name='mnet')
            >>> class MobileNet:
            >>>     pass
            >>> backbones = Registry('backbone')
            >>> class ResNet:
            >>>     pass
            >>> backbones.register_module(ResNet)
        Args:
            name (str | None): The module name to be registered. If not
                specified, the class name will be used.
            force (bool, optional): Whether to override an existing class with
                the same name. Default: False.
            module (type): Module class or function to be registered.
        """
        if not isinstance(force, bool):
            raise TypeError(f"force must be a boolean, but got {type(force)}")
        # NOTE: This is a walkaround to be compatible with the old api,
        # while it may introduce unexpected bugs.

        # use it as a normal method: x.register_module(module=SomeClass)
        if module is not None:
            self._add(module=module, module_name=name, force=force)
            return module

        # use it as a decorator: @x.register_module()
        def wraps(module):
            self._add(module=module, module_name=name, force=force)
            return module

        return wraps

    def _add(self, module, module_name=None, force=False):
        if not inspect.isclass(module) and not inspect.isfunction(module):
            raise TypeError(
                "module must be a class or a function, " f"but got {type(module)}"
            )

        if module_name is None:
            module_name = module.__name__
        if isinstance(module_name, str):
            module_name = [module_name]

        for name in module_name:
            if not force and name in self._obj_map:
                raise KeyError(f"{name} is already registered " f"in {self.namespace}")
            self._obj_map[name] = module

    def get(self, name: str):
        return self._obj_map[name]

    def build(self, **kwargs):
        obj = self.get(kwargs["name"])
        return self.build_func(obj, kwargs)

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
