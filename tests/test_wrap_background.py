from io import StringIO
from rich.console import Console
from rich.text import Text

def test_wrap_background_reset():
    console = Console(file=StringIO(), force_terminal=True, color_system="truecolor", width=15)
    t = Text.assemble(
        ("RED-CHUNK", "on red"),
        (" ", ""),  # explicit space after the red chunk
        ("no background after wrap", None),
    )
    console.print(t)
    output = console.file.getvalue()

    # Red background appears for the first chunk
    assert "\x1b[41mRED-CHUNK" in output

    # A reset appears before the following (wrapped) text
    # (there may be a newline after the reset depending on wrapping)
    assert "\x1b[0m" in output

    # Make sure the red background style doesn’t continue after the reset
    post_reset = output.split("\x1b[0m", 1)[1]
    assert "\x1b[41m" not in post_reset
