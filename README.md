# persistent-bundles

Save and load versioned Python object bundles with optional metadata.

`persistent-bundles` is a small library for objects that manage their own on-disk persistence. It writes a bundle directory containing the saved object, a manifest with the object's class name and semantic version, and optional JSON metadata.

## Installation

```bash
pip install persistent-bundles
```

## Usage

```python
import json
from pathlib import Path
from typing import Self, override

from persistent_bundles.api import load_bundle, save_bundle
from persistent_bundles.types import Loadable, Savable


class MyObject(Savable, Loadable):
    def __init__(self, number: int) -> None:
        self.number = number

    @override
    def save(self, path: Path) -> None:
        with (path / "number.json").open("w") as f:
            json.dump({"number": self.number}, f)

    @classmethod
    @override
    def load(cls, path: Path) -> Self:
        with (path / "number.json").open("r") as f:
            data = json.load(f)
        return cls(data["number"])

    @classmethod
    @override
    def get_class_version(cls) -> str:
        return "1.0.0"


path = Path("example.bundle")
save_bundle(MyObject(42), path, metadata={"created_by": "example"})

obj, metadata = load_bundle(path, {"MyObject": MyObject})
```

Bundles require a `.bundle` path suffix. When loading, the saved class version must have the same semantic-version major number as the current class version.

## Development

```bash
uv run pytest
uv build
```
