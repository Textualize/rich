from typing import Any


def is_rich_object(check_object: Any) -> bool:
    """Check if an object is a Rich renderable."""
    return hasattr(check_object, "__rich_console__") or hasattr(
        check_object, "__rich__"
    )


def is_renderable(check_object: Any) -> bool:
    """Check if an object may be rendered by Rich."""
    return (
        isinstance(check_object, str)
        or hasattr(check_object, "__rich_console__")
        or hasattr(check_object, "__rich__")
    )
