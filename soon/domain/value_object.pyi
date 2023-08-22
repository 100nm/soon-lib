from abc import ABC
from typing import Self

class ValueObject(ABC):
    def validate(self): ...
    @classmethod
    def create_without_validate(cls, *args, **kwargs) -> Self: ...

class StringValueObject(str, ValueObject, ABC): ...
