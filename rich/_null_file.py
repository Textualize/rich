from __future__ import annotations

from types import TracebackType
from typing import IO, AnyStr, Iterable, Iterator, Type


class NullFile(IO[str]):
    def close(self) -> None:
        pass

    def isatty(self) -> bool:
        pass

    def read(self, __n: int = ...) -> AnyStr:
        pass

    def readable(self) -> bool:
        pass

    def readline(self, __limit: int = ...) -> AnyStr:
        pass

    def readlines(self, __hint: int = ...) -> list[AnyStr]:
        pass

    def seek(self, __offset: int, __whence: int = ...) -> int:
        pass

    def seekable(self) -> bool:
        pass

    def tell(self) -> int:
        pass

    def truncate(self, __size: int | None = ...) -> int:
        pass

    def writable(self) -> bool:
        pass

    def writelines(self, __lines: Iterable[AnyStr]) -> None:
        pass

    def __next__(self) -> AnyStr:
        pass

    def __iter__(self) -> Iterator[AnyStr]:
        pass

    def __enter__(self) -> IO[AnyStr]:
        pass

    def __exit__(
        self,
        __t: Type[BaseException] | None,
        __value: BaseException | None,
        __traceback: TracebackType | None,
    ) -> None:
        pass

    def write(self, text: str) -> int:
        return 1

    def flush(self) -> None:
        pass

    def fileno(self) -> int:
        return -1


NULL_FILE = NullFile()
