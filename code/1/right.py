from typing import TypeVar

T = TypeVar("T", int, str)


def max_2(var1: T, var2: T) -> T:
    return max(var1, var2)


max_2("foo", 1)
max_2(1, "foo")
max_2("foo", "bar")
max_2(1, 2)
