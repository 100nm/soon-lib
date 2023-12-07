from abc import ABC, abstractmethod
from typing import Iterable

from soon.infrastructure.resources import Resource


class Context[T](ABC):
    __slots__ = ()

    @property
    @abstractmethod
    def claimant_id[ID](self) -> ID | None:
        raise NotImplementedError

    @property
    @abstractmethod
    def target(self) -> T | None:
        raise NotImplementedError

    @property
    @abstractmethod
    def resource_path(self) -> Iterable[Resource]:
        raise NotImplementedError
