from pathlib import Path
from typing import ClassVar

from persistent_bundles.base_classes.json_attribute_bundle import JsonAttributeBundle

from persistent_bundles.api import (
    load_bundle,
    save_bundle,
)


class MyObject(JsonAttributeBundle):
    persisted_attributes: ClassVar[tuple[str, ...]] = ("number",)

    def __init__(self, number: int):
        self.number: int = number


REGISTERED_CLASSES = {"MyObject": MyObject}


def test_can_save_and_load_my_object_using_base_class(tmp_path: Path):
    obj = MyObject(number=42)
    save_bundle(obj, tmp_path / "obj.bundle")
    del obj
    obj, _metadata = load_bundle(tmp_path / "obj.bundle", REGISTERED_CLASSES)

    assert isinstance(obj, MyObject)
    assert obj.number == 42
