import time
from contextlib import contextmanager
from typing import Generator


@contextmanager
def measure_execution_time(name: str) -> Generator[None, None, None]:
    start = time.time()
    try:
        yield
    finally:
        print(f"{name} took {time.time() - start} seconds")


@measure_execution_time("case 1")  # as a decorator
def do_work_1() -> None:
    ...


def do_work_2() -> None:
    ...


with measure_execution_time("case 2"):  # as a context manager
    do_work_2()
