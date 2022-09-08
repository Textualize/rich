from types import TracebackType
from typing import IO, AnyStr, Iterable, Iterator, List, Optional, Type


class NullFile(IO[str]):

    # TODO: "mode", "name" and "closed" are only required for Python 3.6.

    @property
    def mode(self) -> str:
        return ""

    @property
    def name(self) -> str:
        return ""

    def closed(self) -> bool:
        return False

    def close(self) -> None:
        pass

    def isatty(self) -> bool:
        return False

    def read(self, __n: int = ...) -> AnyStr:
        return ""

    def readable(self) -> bool:
        return False

    def readline(self, __limit: int = ...) -> AnyStr:
        return ""

    def readlines(self, __hint: int = ...) -> List[AnyStr]:
        return []

    def seek(self, __offset: int, __whence: int = ...) -> int:
        return 0

    def seekable(self) -> bool:
        return False

    def tell(self) -> int:
        return 0

    def truncate(self, __size: Optional[int] = ...) -> int:
        return 0

    def writable(self) -> bool:
        return False

    def writelines(self, __lines: Iterable[AnyStr]) -> None:
        pass

    def __next__(self) -> AnyStr:
        return ""

    def __iter__(self) -> Iterator[AnyStr]:
        pass

    def __enter__(self) -> IO[AnyStr]:
        pass

    def __exit__(
        self,
        __t: Optional[Type[BaseException]],
        __value: Optional[BaseException],
        __traceback: Optional[TracebackType],
    ) -> None:
        pass

    def write(self, text: str) -> int:
        return 0

    def flush(self) -> None:
        pass

    def fileno(self) -> int:
        return -1


NULL_FILE = NullFile()
