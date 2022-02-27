import typing
import uuid
from dataclasses import dataclass


class InstanceWithId(typing.Protocol):
    @property
    def id(self) -> str:
        ...


def print_instance_id(instance: InstanceWithId) -> None:
    print(f"Received instance with id: {instance.id}")


@dataclass
class MyDataClass:
    id: str


class MyRegularClass:
    def __init__(self) -> None:
        self.id = str(uuid.uuid4())


class MyNamedTuple(typing.NamedTuple):
    id: str


class ClassWithoutId:
    ...


print_instance_id(MyDataClass(id="123"))
print_instance_id(MyRegularClass())
print_instance_id(MyNamedTuple(id="abc"))
print_instance_id(ClassWithoutId())  # mypy gives error
