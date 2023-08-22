from abc import ABC, ABCMeta
from typing import Any, Self


class ValueObjectMeta(ABCMeta):
    def __call__(cls, *args, _validate: bool = True, **kwargs):
        instance = super().__call__(*args, **kwargs)
        setattr(instance, "$is_validated", _validate)
        setattr(instance, "$is_init", True)

        if _validate:
            instance.validate()

        return instance


class ValueObject(metaclass=ValueObjectMeta):
    def __setattr__(self, name: str, value: Any):
        self.__check_init()
        return super().__setattr__(name, value)

    def __delattr__(self, name: str):
        self.__check_init()
        return super().__delattr__(name)

    @property
    def _is_init(self) -> bool:
        return getattr(self, "$is_init", False)

    @property
    def _is_validated(self) -> bool:
        return getattr(self, "$is_validated")

    def validate(self):
        ...

    @classmethod
    def create_without_validate(cls, *args, **kwargs) -> Self:
        return cls(*args, _validate=False, **kwargs)

    def __check_init(self):
        if self._is_init:
            class_name = self.__class__.__name__
            raise TypeError(f"`{class_name}` is immutable.")


del ValueObjectMeta


class StringValueObject(str, ValueObject, ABC):
    ...
