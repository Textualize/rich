import pytest
from rich.text import Text
from rich.errors import MarkupError

def test_invalid_markup_message_is_actionable_mismatched_close():
    bad = "[bold]hello[/italic]"  # mismatched closing tag should raise
    with pytest.raises(MarkupError) as exc:
        Text.from_markup(bad)

    msg = str(exc.value).lower()
    # keep the assertions flexible so they work with current Rich messaging
    assert any(word in msg for word in ("invalid", "mismatch", "closing", "end tag"))
