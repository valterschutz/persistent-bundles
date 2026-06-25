from pathlib import Path
from typing import Protocol, Self


class Savable(Protocol):
    def save(self, path: Path) -> None: ...


class Loadable(Protocol):
    @classmethod
    def load(cls, path: Path) -> Self: ...
