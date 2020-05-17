import io

import pytest

from rich.console import Console
from rich.align import Align


def test_bad_align_legal():

    # Legal
    Align("foo", "left")
    Align("foo", "center")
    Align("foo", "right")

    # illegal
    with pytest.raises(ValueError):
        Align("foo", None)
    with pytest.raises(ValueError):
        Align("foo", "middle")
    with pytest.raises(ValueError):
        Align("foo", "")
    with pytest.raises(ValueError):
        Align("foo", "LEFT")


def test_render():
    console = Console(file=io.StringIO(), width=10)
    console.print(Align("foo", "left"))
    assert console.file.getvalue() == "foo\n"
