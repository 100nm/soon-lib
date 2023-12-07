from abc import ABC, abstractmethod
from typing import Iterable

from soon.infrastructure.context import Context


class Prerequisite(ABC):
    __slots__ = ()

    @property
    @abstractmethod
    def failure_message(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def verify(self, context: Context) -> bool:
        raise NotImplementedError


class PrerequisiteGroup(Prerequisite):
    __slots__ = ("__prerequisites", "__failure_message")

    def __init__(self, prerequisites: Iterable[Prerequisite], failure_message: str):
        self.__prerequisites = frozenset(prerequisites)
        self.__failure_message = failure_message

    @property
    def failure_message(self) -> str:
        return self.__failure_message

    def verify(self, context: Context) -> bool:
        return all(
            (prerequisite.verify(context) for prerequisite in self.__prerequisites)
        )
