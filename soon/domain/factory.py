from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from .entity import Entity

E = TypeVar("E", bound=Entity)


class AbstractFactory(Generic[E], ABC):
    __slots__ = ()

    @abstractmethod
    def build(self, **kwargs) -> E:
        raise NotImplementedError
