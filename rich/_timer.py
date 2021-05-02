"""
Timer context manager, only used in debug.

"""

from time import time

import contextlib
from typing import Iterator


@contextlib.contextmanager
def timer(subject: str = "time") -> Iterator[None]:
    """print the elapsed time. (only used in debugging)"""
    start = time()
    yield
    elapsed = time() - start
    elapsed_ms = elapsed * 1000
    print(f"{subject} elapsed {elapsed_ms:.1f}ms")
