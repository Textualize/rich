from typing import Any, Iterable, List, Union, Tuple, Type, TypeVar


T = TypeVar("T")


RichReprResult = Iterable[Union[Any, Tuple[Any], Tuple[str, Any], Tuple[str, Any, Any]]]


def rich_repr(cls: Type[T]) -> Type[T]:
    """Class decorator to create __repr__ from __rich_repr__"""

    def auto_repr(self) -> str:
        repr_str: List[str] = []
        append = repr_str.append
        for arg in self.__rich_repr__():
            if isinstance(arg, tuple):
                if len(arg) == 1:
                    append(repr(arg[0]))
                else:
                    key, value, *default = arg
                    if len(default) and default[0] == value:
                        continue
                    append(f"{key}={value!r}")
            else:
                append(repr(arg))
        return f"{self.__class__.__name__}({', '.join(repr_str)})"

    auto_repr.__doc__ = "Return repr(self)"
    cls.__repr__ = auto_repr  # type: ignore

    return cls
