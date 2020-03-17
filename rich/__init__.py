from typing import Any, IO, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .console import Console

# Global console used by alternative print
_console: Optional["Console"] = None


def print(
    *objects: Any, sep=" ", end="\n", file: IO[str] = None, flush: bool = False,
):
    global _console
    if _console is None:
        from .console import Console

        _console = Console(log_time=False)

    write_console = _console if file is None else Console(file=file)
    return write_console.print(*objects, sep=sep, end=end)


if __name__ == "__main__":  # pragma: no cover
    print("Hello, **World**")
