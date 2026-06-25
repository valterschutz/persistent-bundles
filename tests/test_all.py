import json
from pathlib import Path
from typing import Self, override

from persistent_bundles.api import load_bundle, save_bundle
from persistent_bundles.types import Savable, Loadable


class MyObject(Savable, Loadable):
    def __init__(self, number: int):
        self.number: int = number

    @override
    def save(self, path: Path) -> None:
        with (path / "number.json").open("w") as f:
            json.dump({"number": self.number}, f)

    @classmethod
    @override
    def load(cls, path: Path) -> Self:
        with (path / "number.json").open("r") as f:
            d = json.load(f)
        obj = cls.__new__(cls)
        obj.number = d["number"]
        return obj


REGISTERED_CLASSES = {"MyObject": MyObject}


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
