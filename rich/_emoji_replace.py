import re
from typing import Callable, Literal, Match, Optional

from ._emoji_codes import EMOJI

_ReStringMatch = Match[str]  # regex match object
_ReSubCallable = Callable[[_ReStringMatch], str]  # Callable invoked by re.sub
_EmojiSubMethod = Callable[[_ReSubCallable, str], str]  # Sub method of a compiled re
_StripMode = Literal["keep", "strip"]


def _emoji_replace(
    text: str,
    default_variant: Optional[str] = None,
    _emoji_sub: _EmojiSubMethod = re.compile(r"(:(\S*?)(?:(?:\-)(emoji|text))?:)").sub,
    strip: bool = False,
) -> str:
    """Replace emoji code in text."""
    get_emoji = EMOJI.__getitem__
    variants = {"text": "\uFE0E", "emoji": "\uFE0F"}
    get_variant = variants.get
    default_variant_code = variants.get(default_variant, "") if default_variant else ""

    def do_replace(match: Match[str]) -> str:
        if strip:
            return ""
        emoji_code, emoji_name, variant = match.groups()
        try:
            return get_emoji(emoji_name.lower()) + get_variant(
                variant, default_variant_code
            )
        except KeyError:
            return emoji_code

    return _emoji_sub(do_replace, text)


def process_emoji_in_text(
    text: str,
    default_variant: Optional[str] = None,
    strip_mode: Optional[_StripMode] = None,
) -> str:
    """Process text with emoji codes."""
    if strip_mode is not None and strip_mode == "keep":
        # fast track, keep emojicodes -> return original text
        return text
    should_strip = strip_mode is not None and strip_mode == "strip"
    return _emoji_replace(text, default_variant, strip=should_strip)
