from typing import Match

import re

from ._emoji_codes import EMOJI


def _emoji_replace(text: str, _emoji_sub=re.compile(r"(:(\S*?):)").sub) -> str:
    """Replace emoji code in text."""
    get_emoji = EMOJI.get

    def do_replace(match: Match[str]) -> str:
        """Called by re.sub to do the replacement."""
        emoji_code, emoji_name = match.groups()
        return get_emoji(emoji_name.lower(), emoji_code)

    return _emoji_sub(do_replace, text)
