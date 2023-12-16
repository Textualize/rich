import os
import sys
from contextlib import AbstractContextManager
from types import TracebackType

__all__ = ("pipe_cleanup", "SuppressBrokenPipeError")


class SuppressBrokenPipeError(AbstractContextManager):
    def __exit__(
        self,
        __exc_type: type[BaseException] | None,
        __exc_value: BaseException | None,
        __traceback: TracebackType | None,
    ) -> bool | None:
        if __exc_type is BrokenPipeError:
            return pipe_cleanup()
        else:
            return super().__exit__(__exc_type, __exc_value, __traceback)


def pipe_cleanup() -> None:
    """Handle BrokenPipeError: redirect output to devnull"""
    devnull = os.open(os.devnull, os.O_WRONLY)
    os.dup2(devnull, sys.stdout.fileno())
    sys.exit(1)  # Python exits with error code 1 on EPIPE
