from abc import ABC, abstractmethod
from typing import Any, Mapping


class Error(Exception, ABC):
    __slots__ = ()

    @property
    @abstractmethod
    def status_code(self) -> int:
        raise NotImplementedError

    @property
    @abstractmethod
    def content(self) -> Any:
        raise NotImplementedError


class Invalid(Error):
    __slots__ = ("__reason",)

    def __init__(self, reason: str):
        super().__init__(reason)
        self.__reason = reason

    @property
    def status_code(self) -> int:
        return 422

    @property
    def content(self) -> str:
        return self.__reason


class ValidationError(Invalid):
    __slots__ = ("__errors",)

    def __init__(self, errors: Mapping[str, Any], reason: str = ""):
        super().__init__(reason)
        self.__errors = errors

    @property
    def content(self) -> Mapping[str, Any]:
        return self.__errors
