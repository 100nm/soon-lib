from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from types import FunctionType, MappingProxyType
from typing import Any, Callable, Iterable, Mapping

import parse

from soon.infrastructure.controller import Controller
from soon.infrastructure.prerequisite import Prerequisite


class Resource(ABC):
    __slots__ = ()

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, self.__class__) and self.identifier == other.identifier

    @property
    @abstractmethod
    def key(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def identifier(self) -> Identifier:
        raise NotImplementedError

    @property
    @abstractmethod
    def sub_resources(self) -> Iterable[Resource]:
        raise NotImplementedError

    @property
    @abstractmethod
    def details(self) -> Mapping[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def add_resources(self, *resources: Resource):
        raise NotImplementedError


class Identifier(ABC):
    __slots__ = ()

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, self.__class__) and str(self) == str(other)


class StaticIdentifier(Identifier):
    __slots__ = ("__value",)

    def __init__(self, value: str, /):
        self.__value = value

    def __str__(self) -> str:
        return self.__value

    def __repr__(self) -> str:
        return self.__value

    def __eq__(self, other: Any) -> bool:
        if super().__eq__(other):
            return True

        return self.__value == other


class DynamicIdentifier(Identifier):
    __slots__ = ("__parser",)

    def __init__(self, value: str, /):
        self.__parser = parse.compile(value)

    def __str__(self) -> str:
        return self.__value

    def __repr__(self) -> str:
        return self.__value

    def __eq__(self, other: Any) -> bool:
        if super().__eq__(other):
            return True

        elif isinstance(other, str):
            return bool(self.__parser.parse(other, evaluate_result=False))

        else:
            return False

    @property
    def __value(self) -> str:
        return self.__parser._format

    def parse(self, string: str) -> Mapping[str, str]:
        result = self.__parser.parse(string)

        if result is None:
            raise ValueError(f"`{string}` doesn't match with `{self.__value}`.")

        return MappingProxyType(result.named)

    def format(self, /, **kwargs) -> str:
        return self.__value.format(**kwargs)


@dataclass(repr=False, slots=True)
class Action:
    function: FunctionType = field()
    prerequisites: frozenset[Prerequisite] = field(default=frozenset())
    controller: Controller = field(default=None)

    def __call__(self, /, *args, **kwargs) -> Any:
        return self.callable(*args, **kwargs)

    @property
    def callable(self) -> Callable[..., Any]:
        if (controller := self.controller) is None:
            return self.function

        return self.function.__get__(controller, controller.__class__)
