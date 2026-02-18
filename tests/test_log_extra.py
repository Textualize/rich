import io

import pytest

from rich.console import Console
from rich.panel import Panel
from rich.segment import Segment
from rich.style import Style
from rich.text import Text
from rich._log_render import LogRender


def test_log_render_render_path_when_enabled():
    console = Console(record=True)
    log_render = LogRender(show_time=False, show_level=False, show_path=True)
    table = log_render(
        console=console,
        renderables=[Text("msg")],
        path="file.py",
        line_no=None,
        link_path=None,
    )
    console.print(table)
    out = console.export_text()

# assert its in

    assert "file.py" in out

def test_log_render_not_render_line_number_when_none():
    console = Console(record=True)
    log_render = LogRender(show_time=False, show_level=False, show_path=True)

    table = log_render(
        console=console,
        renderables=[Text("msg")],
        path="file.py",
        line_no=None,
        link_path=None,
    )

    console.print(table)
    out = console.export_text()
# assert not 
    assert "file.py:" not in out
