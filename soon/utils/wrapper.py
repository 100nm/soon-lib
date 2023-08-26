from abc import ABC, abstractmethod
from copy import copy
from types import FunctionType, MethodType
from typing import Any, Self


class FunctionWrapper(ABC):
    __slots__ = ("function",)

    def __init__(self, function: FunctionType | MethodType, /):
        self.function = function

    def __call__(self, /, *args, **kwargs) -> Any:
        return self.wrapper(*args, **kwargs)

    def __get__(self, instance: object | None, owner: type) -> Self:
        if instance is None:
            return self

        method = self.function.__get__(instance, owner)
        self_copy = copy(self)
        self_copy.function = method
        return self_copy

    def __getattribute__(self, name: str) -> Any:
        try:
            return super().__getattribute__(name)
        except AttributeError as exc:
            if name == "__wrapped__":
                return self.function

            raise exc

    @abstractmethod
    def wrapper(self, /, *args, **kwargs) -> Any:
        raise NotImplementedError
