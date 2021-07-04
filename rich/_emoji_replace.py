from typing import Callable, Match, Optional

import re

from ._emoji_codes import EMOJI


_ReStringMatch = Match[str]  # regex match object
_ReSubCallable = Callable[[_ReStringMatch], str]  # Callable invoked by re.sub
_EmojiSubMethod = Callable[[_ReSubCallable, str], str]  # Sub method of a compiled re


def _emoji_replace(
    text: str,
    variant: Optional[str] = None,
    _emoji_sub: _EmojiSubMethod = re.compile(r"(:(\S*?):)").sub,
) -> str:
    """Replace emoji code in text."""
    get_emoji = EMOJI.get
    variant_code = ("\uFE0E" if variant == "emoji_" else "\uFE0F") if variant else ""

    def do_replace(match: Match[str]) -> str:
        emoji_code, emoji_name = match.groups()
        return get_emoji(emoji_name.lower(), emoji_code) + variant_code

    return _emoji_sub(do_replace, text)
