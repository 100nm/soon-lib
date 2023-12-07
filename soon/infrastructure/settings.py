from inspect import getmembers
from os import environ
from typing import Any


class Settings:
    def __init__(self, obj: Any):
        for name, value in getmembers(obj):
            if name.isupper() is False:
                continue

            setattr(self, name, value)


def checkenv(key: str) -> str:
    try:
        return environ[key]
    except KeyError as exc:
        raise ValueError(f"`{key}` missing in the environment.") from exc
