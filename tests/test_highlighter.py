import pytest
from rich.highlighter import NullHighlighter


def test_wrong_type():
    highlighter = NullHighlighter()
    with pytest.raises(TypeError):
        highlighter([])
