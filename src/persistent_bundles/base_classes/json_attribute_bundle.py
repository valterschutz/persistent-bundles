import json
from pathlib import Path
from typing import ClassVar, Self

from typing_extensions import override

from persistent_bundles.types import Loadable, Savable


class JsonAttributeBundle(Savable, Loadable):
    """Persist simple classes whose bundle state is a fixed set of JSON attributes."""

    persisted_attributes: ClassVar[tuple[str, ...]]
    class_version: ClassVar[str] = "1.0.0"

    @override
    def save(self, path: Path) -> None:
        data = {name: getattr(self, name) for name in self.persisted_attributes}
        with (path / "data.json").open("w") as f:
            json.dump(data, f)

    @classmethod
    @override
    def load(cls, path: Path) -> Self:
        with (path / "data.json").open("r") as f:
            data = json.load(f)

        obj = cls.__new__(cls)
        for name in cls.persisted_attributes:
            setattr(obj, name, data[name])
        return obj

    @classmethod
    @override
    def get_class_version(cls) -> str:
        return cls.class_version
