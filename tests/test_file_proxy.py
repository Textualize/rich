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
    """FileProxy.isatty() should delegate to the underlying file."""
    import unittest.mock

    console = Console()
    mock_file = unittest.mock.MagicMock()
    mock_file.isatty.return_value = True
    file_proxy = FileProxy(console, mock_file)
    assert file_proxy.isatty() is True
    mock_file.isatty.assert_called_once()

    # Verify False case also delegates correctly
    mock_file.isatty.return_value = False
    assert file_proxy.isatty() is False
