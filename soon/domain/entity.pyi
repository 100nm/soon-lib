from abc import ABC
from dataclasses import dataclass
from uuid import UUID

@dataclass
class Entity(ABC):
    id: UUID = ...
    def __init__(self, id: UUID | str = ..., **kwargs): ...
