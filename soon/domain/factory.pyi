from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from soon import Entity

_E = TypeVar("_E", bound=Entity)

class AbstractFactory(Generic[_E], ABC):
    @abstractmethod
    def build(self, **kwargs) -> _E: ...
