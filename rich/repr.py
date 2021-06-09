from typing import Any, Iterable, List, Union, Tuple, Type, TypeVar


T = TypeVar("T")


RichReprResult = Iterable[Union[Any, Tuple[Any], Tuple[str, Any], Tuple[str, Any, Any]]]


def rich_repr(cls: Type[T]) -> Type[T]:
    """Class decorator to create __repr__ from __rich_repr__"""

    def auto_repr(self: Any) -> str:
        repr_str: List[str] = []
        append = repr_str.append
        angular = getattr(self.__rich_repr__, "angular", False)
        for arg in self.__rich_repr__():
            if isinstance(arg, tuple):
                if len(arg) == 1:
                    append(repr(arg[0]))
                else:
                    key, value, *default = arg
                    if key is None:
                        append(repr(value))
                    else:
                        if len(default) and default[0] == value:
                            continue
                        append(f"{key}={value!r}")
            else:
                append(repr(arg))
        if angular:
            return f"<{self.__class__.__name__} {' '.join(repr_str)}>"
        else:
            return f"{self.__class__.__name__}({', '.join(repr_str)})"

    auto_repr.__doc__ = "Return repr(self)"
    cls.__repr__ = auto_repr  # type: ignore

    return cls


if __name__ == "__main__":

    @rich_repr
    class Foo:
        def __rich_repr__(self) -> RichReprResult:

            yield "foo"
            yield "bar", {"shopping": ["eggs", "ham", "pineapple"]}
            yield "buy", "hand sanitizer"

        __rich_repr__.angular = False  # type: ignore

    foo = Foo()
    from rich.console import Console
    from rich import print

    console = Console()

    console.rule("Standard repr")
    console.print(foo)

    console.print(foo, width=60)
    console.print(foo, width=30)

    console.rule("Angular repr")
    Foo.__rich_repr__.angular = True  # type: ignore

    console.print(foo)

    console.print(foo, width=60)
    console.print(foo, width=30)
