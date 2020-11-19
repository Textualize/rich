from typing import Any

from .abc import RichRenderable


def is_renderable(check_object: Any) -> bool:
    """Check if an object may be rendered by Rich."""
    return isinstance(check_object, str) or isinstance(check_object, RichRenderable)
