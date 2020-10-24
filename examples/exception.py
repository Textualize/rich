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
    try:
        for number, divisor in divides:
            result = divide_by(number, divisor)
            console.print(f"{number} divided by {divisor} is {result}")
    except Exception:
        console.print_exception(extra_lines=5, show_locals=True)


DIVIDES = [
    (1000, 200),
    (10000, 500),
    (0, 1000000),
    (3.1427, 2),
    (2 ** 32, 2 ** 16),
    (1, 0),
]

divide_all(DIVIDES)
