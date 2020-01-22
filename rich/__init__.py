from colorama import init

from typing import Any, IO, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .console import Console

# Global console used by alternative print
_console: Optional["Console"] = None


def print(
    *objects: Any,
    sep=" ",
    end="\n",
    file: IO[str] = None,
    flush: bool = False,
    log_locals: bool = False
):
    global _console
    if _console is None:
        from .console import Console

        _console = Console(log_time=False)

    write_console = _console if file is None else Console(log_time=False, file=file)
    return write_console.log(
        *objects, sep=sep, end=end, log_locals=log_locals, _stack_offset=2
    )


init()

if __name__ == "__main__":  # pragma: no cover
    print("Hello, **World**", log_locals=True)
