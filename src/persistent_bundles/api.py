from collections.abc import Mapping
import json
from pathlib import Path
from typing import Any

from persistent_bundles.types import Loadable, Savable


def save_bundle(
    obj: Savable,
    path: Path,
    metadata: Mapping[str, Any] | None = None,  # pyright: ignore[reportExplicitAny]
) -> None:
    """Save an object and the metadata needed to load it later."""
    assert str(path).endswith(".bundle")

    object_path = path / "object"
    object_path.mkdir(parents=True)
    obj.save(object_path)

    with (path / "manifest.json").open("w") as f:
        json.dump({"class_name": obj.__class__.__name__}, f)

    if metadata is not None:
        with (path / "metadata.json").open("w") as f:
            json.dump(metadata, f)


def load_bundle(
    path: Path,
    class_mapping: Mapping[str, type[Loadable]],
) -> tuple[Loadable, Mapping[str, Any]]:  # pyright: ignore[reportExplicitAny]
    """Load a bundle object, returning both the object and metadata."""
    assert str(path).endswith(".bundle")

    with (path / "manifest.json").open("r") as f:
        class_name = json.load(f)["class_name"]

    obj = class_mapping[class_name].load(path / "object")

    if (path / "metadata.json").exists():
        with (path / "metadata.json").open("r") as f:
            metadata = json.load(f)
    else:
        metadata = {}

    return obj, metadata
