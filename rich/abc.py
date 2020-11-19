from abc import ABC

from .protocol import is_rich_object


class RichRenderable(ABC):
    """An abstract base class for Rich renderables.

    Use this to check if an object supports the Rich renderable protocol. For example::

        if isinstance(my_object, RichRenderable):
            console.print(my_object)

    """

    @classmethod
    def __subclasscheck__(cls, other) -> bool:
        return is_rich_object(other)


if __name__ == "__main__":
    from rich.text import Text

    t = Text()
    print(isinstance(t, RichRenderable))

    class Foo:
        pass

    f = Foo()
    print(isinstance(f, RichRenderable))
    print(isinstance("", RichRenderable))
