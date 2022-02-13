from enum import Enum
from typing import NoReturn


class Color(Enum):
    RED = "RED"
    GREEN = "GREEN"
    BLUE = "BLUE"  # I just added this


def handle_color(color: Color) -> None:
    if color is Color.RED:
        ...
    elif color is Color.GREEN:
        ...
    else:
        assert_never(color)


def assert_never(value: NoReturn) -> NoReturn:
    assert False, f"Unknown value: {value}"
