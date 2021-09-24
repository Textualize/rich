"""

Demonstrates Rich tracebacks for recursion errors.

Rich can exclude frames in the middle to avoid huge tracebacks.

"""

from rich.console import Console


def foo(n):
    return bar(n)


def bar(n):
    return foo(n)


console = Console()

try:
    foo(1)
except Exception:
    console.print_exception(max_frames=20)
