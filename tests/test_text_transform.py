"""Text transformation renderables unit tests."""

from rich.text_transform import TextTransform, Upper, Lower, SwapCase
from rich.console        import Console

SOURCE_TEXT = "Wait a minute – it's you! The man from Maybury Hill!"

def _as_text( to_test: TextTransform ) -> str:
    return Console().render_lines( to_test )[ 0 ][ 0 ].text

def test_basic_text():
    assert _as_text( Upper( SOURCE_TEXT ) ) == SOURCE_TEXT.upper()
    assert _as_text( Lower( SOURCE_TEXT ) ) == SOURCE_TEXT.lower()
    assert _as_text( SwapCase( SOURCE_TEXT ) ) == SOURCE_TEXT.swapcase()

### test_text_transform.py ends here
