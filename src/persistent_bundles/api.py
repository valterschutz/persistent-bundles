from collections.abc import Mapping
import json
from pathlib import Path
from typing import Any

from persistent_bundles.exceptions import IncompatibleBundleVersionError
from persistent_bundles.types import Loadable, Savable
from persistent_bundles.utils import is_same_major_semver


def save_bundle(
    obj: Savable,
    path: Path,
    metadata: Mapping[str, Any] | None = None,
) -> None:
    """Save an object and the metadata needed to load it later."""
    assert str(path).endswith(".bundle")

    object_path = path / "object"
    object_path.mkdir(parents=True)
    obj.save(object_path)

    with (path / "manifest.json").open("w") as f:
        json.dump(
            {
                "class_name": obj.__class__.__name__,
                "class_version": obj.get_class_version(),
            },
            f,
        )

    if metadata is not None:
        with (path / "metadata.json").open("w") as f:
            json.dump(metadata, f)


def load_bundle(
    path: Path,
    class_mapping: Mapping[str, type[Loadable]],
    accept_incompatible_classes: bool = False,
    **kwargs,  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
) -> tuple[Loadable, Mapping[str, Any]]:
    """Load a bundle object, returning both the object and metadata."""
    assert str(path).endswith(".bundle")

    with (path / "manifest.json").open("r") as f:
        manifest = json.load(f)

    class_name = manifest["class_name"]
    class_to_be_loaded = class_mapping[class_name]
    current_class_version = class_to_be_loaded.get_class_version()
    saved_class_version = manifest["class_version"]

    if not accept_incompatible_classes and not is_same_major_semver(
        saved_class_version, current_class_version
    ):
        raise IncompatibleBundleVersionError(
            "The loaded bundle does not have the same major class version as the current class"
        )

    obj = class_to_be_loaded.load(path / "object", **kwargs)

    if (path / "metadata.json").exists():
        with (path / "metadata.json").open("r") as f:
            metadata = json.load(f)
    else:
        metadata = {}

    return obj, metadata
