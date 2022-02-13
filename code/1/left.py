from typing import Union

U = Union[int, str]


def max_1(var1: U, var2: U) -> U:
    return max(var1, var2)


max_1("foo", 1)
max_1(1, "foo")
max_1("foo", "bar")
max_1(1, 2)
