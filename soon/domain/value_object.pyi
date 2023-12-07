from abc import ABC
from typing import NoReturn

class ValueObject(ABC):
    def validate(self) -> NoReturn: ...

class StringValueObject(str, ValueObject, ABC): ...
