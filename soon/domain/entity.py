from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4


class Entity(ABC):
    __slots__ = ()

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"<{class_name} {self.id}>"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, type(self)) and self.id == other.id

    @property
    @abstractmethod
    def id(self) -> Any:
        raise NotImplementedError


@dataclass(repr=False, eq=False, slots=True)
class EntityUUID(Entity, ABC):
    id: UUID = field(default_factory=uuid4)
