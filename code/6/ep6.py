from typing import Final, final

MY_STR: Final = "Can't change me :)"
MY_INT: Final = 13

# error: Cannot assign to final name "MY_STR"
MY_STR = "Something else"
# error: Cannot assign to final name "MY_STR"
MY_STR += "Add this to end"
# error: Cannot assign to final name "MY_INT"
MY_INT = 0


class MyClass:
    CLASS_VARIABLE: Final = "foo"

    @final
    def method(self) -> None:
        ...


class MyChildClass(MyClass):
    # error: Cannot assign to final name "CLASS_VARIABLE"
    CLASS_VARIABLE = "bar"

    # error: Cannot override final attribute "method"
    # (previously declared in base class "MyClass")
    def method(self) -> None:
        ...
