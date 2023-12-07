from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, Self

from soon.infrastructure.resources.basis import Action, Identifier, Resource


@dataclass(repr=False, frozen=True, slots=True)
class HTTPResource(Resource):
    key: str = field()
    identifier: Identifier = field()
    sub_resources: set[Resource] = field(default_factory=set)
    methods: dict[HTTPMethods, Action] = field(default_factory=dict)

    def __str__(self) -> str:
        return str(self.identifier)

    @property
    def details(self) -> dict[str, Any]:
        return {"methods_allowed": tuple(method.value for method in self.methods)}

    def add_resources(self, *resources: Resource) -> Self:
        self.sub_resources.update(resources)
        return self


class HTTPMethods(StrEnum):
    GET = "GET"
    HEAD = "HEAD"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    CONNECT = "CONNECT"
    OPTIONS = "OPTIONS"
    TRACE = "TRACE"
    PATCH = "PATCH"
