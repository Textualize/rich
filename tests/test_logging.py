import io
import os
import logging
from pathlib import Path
from typing import Optional

import pytest

from rich.console import Console
from rich.logging import RichHandler
from rich._log_render import LogRender
from rich.text import Text

handler = RichHandler(
    console=Console(
        file=io.StringIO(),
        force_terminal=True,
        width=80,
        color_system="truecolor",
        _environ={},
    ),
    enable_link_path=False,
)

logging.basicConfig(
    level="NOTSET", format="%(message)s", datefmt="[DATE]", handlers=[handler]
)
log = logging.getLogger("rich")


skip_win = pytest.mark.skipif(
    os.name == "nt",
    reason="rendered differently on windows",
)


@skip_win
def test_exception():
    console = Console(
        file=io.StringIO(),
        force_terminal=True,
        width=140,
        color_system=None,
        _environ={},
    )
    handler_with_tracebacks = RichHandler(
        console=console, enable_link_path=False, rich_tracebacks=True
    )
    formatter = logging.Formatter("FORMATTER %(message)s %(asctime)s")
    handler_with_tracebacks.setFormatter(formatter)
    log.addHandler(handler_with_tracebacks)
    log.error("foo")
    try:
        1 / 0
    except ZeroDivisionError:
        log.exception("message")

    render = handler_with_tracebacks.console.file.getvalue()
    print(render)

    assert "FORMATTER foo" in render
    assert "ZeroDivisionError" in render
    assert "message" in render
    assert "division by zero" in render


def test_exception_with_extra_lines():
    console = Console(
        file=io.StringIO(),
        force_terminal=True,
        width=140,
        color_system=None,
        _environ={},
    )
    handler_extra_lines = RichHandler(
        console=console,
        enable_link_path=False,
        markup=True,
        rich_tracebacks=True,
        tracebacks_extra_lines=5,
    )
    log.addHandler(handler_extra_lines)

    try:
        1 / 0
    except ZeroDivisionError:
        log.exception("message")

    render = handler_extra_lines.console.file.getvalue()
    print(render)

    assert "ZeroDivisionError" in render
    assert "message" in render
    assert "division by zero" in render


def test_stderr_and_stdout_are_none(monkeypatch):
    # This test is specifically to handle cases when using pythonw on
    # windows and stderr and stdout are set to None.
    # See https://bugs.python.org/issue13807

    monkeypatch.setattr("sys.stdout", None)
    monkeypatch.setattr("sys.stderr", None)

    console = Console(_environ={})
    target_handler = RichHandler(console=console)
    actual_record: Optional[logging.LogRecord] = None

    def mock_handle_error(record):
        nonlocal actual_record
        actual_record = record

    target_handler.handleError = mock_handle_error
    log.addHandler(target_handler)

    try:
        1 / 0
    except ZeroDivisionError:
        log.exception("message")

    finally:
        log.removeHandler(target_handler)

    assert actual_record is not None
    assert "message" in actual_record.msg


def test_link_path_uri_format():
    """link_path must use file:/// (3 slashes) and forward slashes.
    Regression test for https://github.com/Textualize/rich/issues/4093
    """
    console = Console(file=io.StringIO(), _environ={})
    render = LogRender()
    abs_path = str(Path(__file__).resolve())
    table = render(
        console,
        renderables=[Text("msg")],
        path="test_logging.py",
        line_no=1,
        link_path=abs_path,
    )
    expected_uri = Path(abs_path).as_uri()

    path_cell = table.columns[-1]._cells[0]
    assert isinstance(path_cell, Text)
    link_styles = [span.style for span in path_cell._spans if "link" in str(span.style)]
    assert any(expected_uri in str(s) for s in link_styles), (
        f"Expected {expected_uri!r} in link styles, got {link_styles!r}"
    )
    assert not any("file://" + abs_path in str(s) for s in link_styles), (
        "file:// (two slashes) should not appear in link styles"
    )


def test_markup_and_highlight():
    console = Console(
        file=io.StringIO(),
        force_terminal=True,
        width=140,
        color_system="truecolor",
        _environ={},
    )
    handler = RichHandler(console=console)

    # Check defaults are as expected
    assert handler.highlighter
    assert not handler.markup

    formatter = logging.Formatter("FORMATTER %(message)s %(asctime)s")
    handler.setFormatter(formatter)
    log.addHandler(handler)

    log_message = "foo 3.141 127.0.0.1 [red]alert[/red]"

    log.error(log_message)
    render_fancy = handler.console.file.getvalue()
    assert "FORMATTER" in render_fancy
    assert log_message not in render_fancy
    assert "red" in render_fancy

    handler.console.file = io.StringIO()
    log.error(log_message, extra={"markup": True})
    render_markup = handler.console.file.getvalue()
    assert "FORMATTER" in render_markup
    assert log_message not in render_markup
    assert "red" not in render_markup

    handler.console.file = io.StringIO()
    log.error(log_message, extra={"highlighter": None})
    render_plain = handler.console.file.getvalue()
    assert "FORMATTER" in render_plain
    assert log_message in render_plain
