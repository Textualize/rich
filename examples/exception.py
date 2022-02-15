"""
Basic example to show how to print an traceback of an exception
"""
from typing import List, Tuple

from rich.console import Console

console = Console()


def divide_by(number: float, divisor: float) -> float:
    """Divide any number by zero."""
    # Will throw a ZeroDivisionError if divisor is 0
    result = number / divisor
    return result


def divide_all(divides: List[Tuple[float, float]]) -> None:
    """Do something impossible every day."""

    for number, divisor in divides:
        console.print(f"dividing {number} by {divisor}")
        try:
            result = divide_by(number, divisor)
        except Exception:
            console.print_exception(extra_lines=8, show_locals=True)
        else:
            console.print(f" = {result}")


DIVIDES = [
    (1000, 200),
    (10000, 500),
    (1, 0),
    (0, 1000000),
    (3.1427, 2),
    (888, 0),
    (2**32, 2**16),
]

divide_all(DIVIDES)
