from pytest_cases import fixture, parametrize


@fixture
def fixture1() -> str:
    return "foo"


@fixture
@parametrize("value", ["bar", "baz"])
def fixture2(value: str) -> str:
    return value


@parametrize("value", [fixture1, fixture2])
def test_just_a_dummy_example(value: str) -> None:
    assert value in ("foo", "bar", "baz")
