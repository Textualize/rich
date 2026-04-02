import io
import sys

import pytest

from rich.console import Console
from rich.file_proxy import FileProxy


def test_empty_bytes():
    console = Console()
    file_proxy = FileProxy(console, sys.stdout)
    # File should raise TypeError when writing bytes
    with pytest.raises(TypeError):
        file_proxy.write(b"")  # type: ignore
    with pytest.raises(TypeError):
        file_proxy.write(b"foo")  # type: ignore


def test_flush():
    file = io.StringIO()
    console = Console(file=file)
    file_proxy = FileProxy(console, file)
    file_proxy.write("foo")
    assert file.getvalue() == ""
    file_proxy.flush()
    assert file.getvalue() == "foo\n"


def test_new_lines():
    file = io.StringIO()
    console = Console(file=file)
    file_proxy = FileProxy(console, file)
    file_proxy.write("-\n-")
    assert file.getvalue() == "-\n"
    file_proxy.flush()
    assert file.getvalue() == "-\n-\n"


def test_isatty_delegates_to_proxied_file():
    """FileProxy.isatty() must delegate to the underlying file.

    io.TextIOBase.isatty() always returns False, so without an explicit
    override the result would be wrong when the proxied file is a tty.
    Regression test for https://github.com/Textualize/rich/issues/4041
    """
    tty_file = io.StringIO()
    tty_file.isatty = lambda: True  # type: ignore[method-assign]

    non_tty_file = io.StringIO()
    # StringIO.isatty() already returns False, but be explicit
    non_tty_file.isatty = lambda: False  # type: ignore[method-assign]

    console = Console()
    assert FileProxy(console, tty_file).isatty() is True
    assert FileProxy(console, non_tty_file).isatty() is False
