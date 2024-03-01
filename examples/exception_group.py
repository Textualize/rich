"""

Demonstrates Rich tracebacks for recursion errors.

Rich can exclude frames in the middle to avoid huge tracebacks.

"""

from rich.console import Console

console = Console()

def a():
    b()

def b():
    try:
        c()
    except Exception as exception:
        raise ExceptionGroup(
            "Created in B",
            [exception, exception]
        )

def c():
    raise RuntimeError("I was raised in C")
    raise ExceptionGroup(
        "exception group",
        [RuntimeError("I'm a runtime error"), ValueError("I'm a value error")]
    )

try:
    a()
except Exception:
    console.print_exception(max_frames=20)
    raise
