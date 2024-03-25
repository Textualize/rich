import io
import os
import tempfile

import pytest

from rich.style import Style
from rich.theme import Theme, ThemeStack, ThemeStackError


def test_inherit():
    theme = Theme({"warning": "red"})
    assert theme.styles["warning"] == Style(color="red")
    assert theme.styles["dim"] == Style(dim=True)


def test_config():
    theme = Theme({"warning": "red"})
    config = theme.config
    assert "warning = red\n" in config


def test_from_file():
    theme = Theme({"warning": "red"})
    text_file = io.StringIO()
    text_file.write(theme.config)
    text_file.seek(0)

    load_theme = Theme.from_file(text_file)
    assert theme.styles == load_theme.styles


def test_read():
    theme = Theme({"warning": "red"})
    with tempfile.TemporaryDirectory("richtheme") as name:
        filename = os.path.join(name, "theme.cfg")
        with open(filename, "wt") as write_theme:
            write_theme.write(theme.config)
        load_theme = Theme.read(filename)
        assert theme.styles == load_theme.styles


def test_theme_stack():
    theme = Theme({"warning": "red"})
    stack = ThemeStack(theme)
    assert stack.get("warning") == Style.parse("red")
    new_theme = Theme({"warning": "bold yellow"})
    stack.push_theme(new_theme)
    assert stack.get("warning") == Style.parse("bold yellow")
    stack.pop_theme()
    assert stack.get("warning") == Style.parse("red")
    with pytest.raises(ThemeStackError):
        stack.pop_theme()
