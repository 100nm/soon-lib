from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any
from uuid import UUID

class Entity(ABC):
    @property
    @abstractmethod
    def id(self) -> Any: ...

@dataclass
class EntityUUID(Entity, ABC):
    id: UUID = ...
