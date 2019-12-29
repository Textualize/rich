from typing import Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .console import Console

# Global console used by alternative print
_console: Optional["Console"] = None


def print(*objects: Any, sep=" ", end="\n", log_locals: bool = False):
    global _console
    if _console is None:
        from .console import Console

        _console = Console()
    return _console.log(
        *objects, sep=sep, end=end, log_locals=log_locals, _stack_offset=2
    )


if __name__ == "__main__":
    print("Hello, **World**", log_locals=True)
