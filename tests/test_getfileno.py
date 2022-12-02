from rich._fileno import get_fileno


def test_get_fileno():
    class FileLike:
        def fileno(self) -> int:
            return 123

    assert get_fileno(FileLike()) == 123


def test_get_fileno_missing():
    class FileLike:
        pass

    assert get_fileno(FileLike()) is None


def test_get_fileno_broken():
    class FileLike:
        def fileno(self) -> int:
            1 / 0
            return 123

    assert get_fileno(FileLike()) is None
