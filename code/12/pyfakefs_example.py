import pathlib

from pyfakefs.fake_filesystem import FakeFilesystem


def my_functionality() -> None:
    with open("foo.txt", "w") as f:
        f.write("foo bar baz")


# fs fixture provides a fake filesystem automatically
def test_my_functionality(fs: FakeFilesystem) -> None:
    path = pathlib.Path("foo.txt")
    assert not path.exists()

    my_functionality()

    assert path.exists()
    with open(path) as f:
        content = f.read()
    assert content == "foo bar baz"
