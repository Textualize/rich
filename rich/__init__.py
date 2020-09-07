"""Rich text and beautiful formatting in the terminal."""

from typing import Any, IO, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .console import Console

# Global console used by alternative print
_console: Optional["Console"] = None


def get_console() -> "Console":
    """Get a global Console instance.

    Returns:
        Console: A console instance.
    """
    global _console
    if _console is None:
        from .console import Console

        _console = Console()

    return _console


def print(
    *objects: Any,
    sep=" ",
    end="\n",
    file: IO[str] = None,
    flush: bool = False,
):
    from .console import Console

    write_console = get_console() if file is None else Console(file=file)
    return write_console.print(*objects, sep=sep, end=end)


def inspect(
    obj: Any,
    *,
    console: "Console" = None,
    title: str = None,
    help: bool = False,
    methods: bool = False,
    docs: bool = True,
    private: bool = False,
    dunder: bool = False,
    sort: bool = True,
    all: bool = False,
):
    """Inspect any Python object.

    Args:
        obj (Any): An object to inspect.
        title (str, optional): Title to display over inspect result, or None use type. Defaults to None.
        help (bool, optional): Show full help text rather than just first paragraph. Defaults to False.
        methods (bool, optional): Enable inspection of callables. Defaults to False.
        docs (bool, optional): Also render doc strings. Defaults to True.
        private (bool, optional): Show private attributes (begining with underscore). Defaults to False.
        dunder (bool, optional): Show attributes starting with double underscore. Defaults to False.
        sort (bool, optional): Sort attributes alphabetically. Defaults to True.
        all (bool, optional): Show all attributes. Defaults to False.
    """
    _console = console or get_console()
    from rich._inspect import Inspect

    _inspect = Inspect(
        obj,
        title=title,
        help=help,
        methods=methods,
        docs=docs,
        private=private,
        dunder=dunder,
        sort=sort,
        all=all,
    )
    _console.print(_inspect)


if __name__ == "__main__":  # pragma: no cover
    print("Hello, **World**")
