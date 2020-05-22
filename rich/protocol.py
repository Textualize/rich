from typing import Any


def is_renderable(test_renderable: Any) -> bool:
    """Check if an object may be rendered by Rich."""
    return (
        isinstance(test_renderable, str)
        or hasattr(test_renderable, "__rich_console__")
        or hasattr(test_renderable, "__rich__")
    )
