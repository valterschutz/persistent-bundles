import json
from pathlib import Path
from typing import Self, cast

import pytest
from typing_extensions import override

from persistent_bundles.api import (
    load_bundle,
    save_bundle,
)
from persistent_bundles.exceptions import IncompatibleBundleVersionError
from persistent_bundles.types import Loadable, Savable


class MyObject(Savable, Loadable):
    def __init__(self, number: int, extra_arg: int | None = None):
        self.number: int = number
        self.extra_arg = extra_arg

    @override
    def save(self, path: Path) -> None:
        with (path / "number.json").open("w") as f:
            json.dump({"number": self.number}, f)

    @classmethod
    @override
    def load(cls, path: Path, extra_arg: int | None = None) -> Self:
        with (path / "number.json").open("r") as f:
            d = json.load(f)
        obj = cls.__new__(cls)
        obj.number = d["number"]
        obj.extra_arg = extra_arg
        return obj

    @classmethod
    @override
    def get_class_version(cls) -> str:
        return "1.0.0"


class MyNewerObject(MyObject):
    @classmethod
    @override
    def get_class_version(cls) -> str:
        return "2.0.0"


REGISTERED_CLASSES = {"MyObject": MyObject, "MyNewerObject": MyNewerObject}
INCOMPATIBLE_CLASSES = {"MyObject": MyNewerObject}


def test_can_save_and_load_my_object(tmp_path: Path):
    obj = MyObject(number=42)
    save_bundle(obj, tmp_path / "obj.bundle")
    del obj
    obj, _metadata = load_bundle(tmp_path / "obj.bundle", REGISTERED_CLASSES)

    assert isinstance(obj, MyObject)
    assert obj.number == 42


def test_can_save_and_load_metadata(tmp_path: Path):
    obj = MyObject(number=42)
    save_bundle(obj, tmp_path / "obj.bundle", metadata={"some data": 43})
    del obj
    _obj, metadata = load_bundle(tmp_path / "obj.bundle", REGISTERED_CLASSES)

    assert metadata == {"some data": 43}


def test_cannot_load_incompatible_class_versions(tmp_path: Path):
    obj = MyObject(number=42)
    save_bundle(obj, tmp_path / "obj.bundle")
    del obj

    with pytest.raises(
        IncompatibleBundleVersionError, match="same major class version"
    ):
        load_bundle(tmp_path / "obj.bundle", INCOMPATIBLE_CLASSES)


def test_can_load_incompatible_class_versions_if_forced(tmp_path: Path):
    obj = MyObject(number=42)
    save_bundle(obj, tmp_path / "obj.bundle")
    del obj

    load_bundle(
        tmp_path / "obj.bundle", INCOMPATIBLE_CLASSES, accept_incompatible_classes=True
    )


def test_kwargs_passed_during_load(tmp_path: Path):
    obj = MyObject(number=42)
    save_bundle(obj, tmp_path / "obj.bundle")
    del obj
    obj, _ = load_bundle(tmp_path / "obj.bundle", REGISTERED_CLASSES, extra_arg=8)
    obj = cast("MyObject", obj)

    assert obj.extra_arg == 8
