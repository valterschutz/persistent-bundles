from pathlib import Path
from typing import Protocol, Self


class Savable(Protocol):
    def save(self, path: Path) -> None: ...

    @classmethod
    def get_class_version(cls) -> str:
        """Return the class version according to semantic versioning. A differing major version indicates incompatible states."""
        ...


class Loadable(Protocol):
    @classmethod
    def load(cls, path: Path) -> Self: ...

    @classmethod
    def get_class_version(cls) -> str:
        """Return the class version according to semantic versioning. A differing major version indicates incompatible states."""
        ...
