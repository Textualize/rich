"""Text transformation renderables unit tests."""

from rich.text_transform import TextTransform, Upper, Lower, SwapCase
from rich.console        import Console
from rich.panel          import Panel

def _as_text( to_test: TextTransform, **console ) -> str:
    return "".join( segment.text for segment in Console( **console ).render( to_test ) ).strip()

PLAIN_TEXT = "Wait a minute – it's you! The man from Maybury Hill!"

def test_plain_text():
    assert _as_text( Upper( PLAIN_TEXT ) ) == PLAIN_TEXT.upper()
    assert _as_text( Lower( PLAIN_TEXT ) ) == PLAIN_TEXT.lower()
    assert _as_text( SwapCase( PLAIN_TEXT ) ) == PLAIN_TEXT.swapcase()

COLOUR_TEXT = (
    "We're looking at a remarkable landscape, littered with different kinds of rocks – "
    "[red]red[/red], [purple]purple[/purple]"
)

def test_colour_text() -> None:
    assert _as_text( Upper( COLOUR_TEXT ) ) == _as_text( COLOUR_TEXT ).upper()
    assert _as_text( Lower( COLOUR_TEXT ) ) == _as_text( COLOUR_TEXT ).lower()
    assert _as_text( SwapCase( COLOUR_TEXT ) ) == _as_text( COLOUR_TEXT ).swapcase()

PANEL_TEXT   = "Halt!"
PANEL_RESULT = f"╭────────╮\n│ {PANEL_TEXT}  │\n╰────────╯"

def test_panel_text() -> None:
    assert _as_text( Upper( Panel( PANEL_TEXT ) ), width=10 ) == PANEL_RESULT.upper()
    assert _as_text( Lower( Panel( PANEL_TEXT ) ), width=10 ) == PANEL_RESULT.lower()
    assert _as_text( SwapCase( Panel( PANEL_TEXT ) ), width=10 ) == PANEL_RESULT.swapcase()

### test_text_transform.py ends here
