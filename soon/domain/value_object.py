from abc import ABC, abstractmethod
from typing import NoReturn


class ValueObject(ABC):
    __slots__ = ()

    @abstractmethod
    def validate(self) -> NoReturn:
        raise NotImplementedError


class StringValueObject(str, ValueObject, ABC):
    __slots__ = ()
