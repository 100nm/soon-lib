from abc import ABCMeta
from dataclasses import dataclass
from typing import Any
from uuid import UUID, uuid4


class EntityMeta(ABCMeta):
    def __new__(mcs, *args, **kwargs):
        cls = super().__new__(mcs, *args, **kwargs)
        return dataclass(cls, repr=False, eq=False, kw_only=True)

    def __call__(cls, id: UUID | str = None, **kwargs):
        instance = super().__call__(**kwargs)
        setattr(instance, "$id", cls.__parse_uuid(id))
        return instance

    @staticmethod
    def __parse_uuid(uuid: UUID | str) -> UUID:
        if not uuid:
            return uuid4()

        elif isinstance(uuid, UUID):
            return uuid

        else:
            return UUID(uuid)


class Entity(metaclass=EntityMeta):
    def __repr__(self) -> str:  # pragma: no cover
        class_name = self.__class__.__name__
        return f"<{class_name} {self.id}>"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, type(self)) and self.id == other.id

    @property
    def id(self) -> UUID:
        return getattr(self, "$id")


del EntityMeta
