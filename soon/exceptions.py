from typing import Any, Mapping


class Error(Exception):
    ...


class Invalid(Error):
    def __init__(self, reason: str):
        super().__init__(reason)
        self.__reason = reason

    @property
    def reason(self) -> str:
        return self.__reason


class ValidationError(Error):
    def __init__(self, errors: Mapping[str, Any]):
        super().__init__(errors)
        self.__errors = errors

    @property
    def errors(self) -> Mapping[str, Any]:
        return self.__errors
