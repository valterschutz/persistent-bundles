from collections.abc import Mapping
from pathlib import Path

from persistent_bundles.types import Loadable, Savable


def save_bundle(obj: Savable, path: Path) -> None:
    """Save an object and the metadata needed to load it later."""
    assert str(path).endswith(".bundle")
    object_path = path / "object"
    object_path.mkdir(parents=True)
    obj.save(object_path)
    with (path / "class_name.txt").open("w") as f:
        f.write(obj.__class__.__name__)


def load_bundle(
    path: Path,
    class_mapping: Mapping[str, type[Loadable]],
) -> Loadable:
    """Load a bundle object, returning both the object and metadata."""
    assert str(path).endswith(".bundle")
    with (path / "class_name.txt").open("r") as f:
        class_name = f.read()
    obj = class_mapping[class_name].load(path / "object")
    return obj
