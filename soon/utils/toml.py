import tomllib
from pathlib import Path
from typing import Any


def load_toml(path: Path | str) -> dict[str, Any]:
    with open(path, "rb") as file:
        return tomllib.load(file)
