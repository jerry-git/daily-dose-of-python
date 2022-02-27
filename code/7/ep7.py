import datetime as dt
from dataclasses import dataclass, field

import apischema
import pytest


def to_timestamp(d: dt.datetime) -> int:
    return int(d.timestamp())


def from_timestamp(ts: int) -> dt.datetime:
    return dt.datetime.fromtimestamp(ts)


@dataclass
class MyNestedClass:
    some_datetime: dt.datetime = field(
        metadata=apischema.metadata.conversion(from_timestamp, to_timestamp)
    )
    some_list: list[str] = field(default_factory=list)


@dataclass
class MyClass:
    foo: str
    bar: int
    baz: MyNestedClass


legit_data = {
    "foo": "value",
    "bar": 123,
    "baz": {"some_datetime": 1642657600, "some_list": ["a", "b"]},
}

my_class_instance = apischema.deserialize(MyClass, legit_data)
serialized = apischema.serialize(MyClass, my_class_instance)
assert serialized == legit_data

bad_data = legit_data | {"bar": "wrong type for bar"}
with pytest.raises(apischema.ValidationError):
    apischema.deserialize(MyClass, bad_data)
