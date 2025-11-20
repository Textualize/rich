"""Simple markup validator using a stack to check tag pairing.

This validator only checks tag structure like [tag]...[/tag].
It does not parse or validate tag attributes/styles — it extracts the
tag name as the first token inside the brackets (so `[link=http://...]`
has tag name `link`).

Usage:
    validator = MarkupValidator()
    valid = validator.validate("[b]bold[/b]")
"""
from __future__ import annotations

import re
from typing import List

from rich.errors import MarkupError


_TAG_NAME_RE = re.compile(r"^/?\s*([A-Za-z0-9_:-]+)")


class MarkupValidator:
    """Validate simple bracket-style markup like `[tag]` and `[/tag]`.

    Method `validate(text)` returns `True` when all tags are properly
    opened and closed with correct nesting. On failure it raises
    `rich.errors.MarkupError` with an explanatory message.
    """

    def validate(self, text: str) -> bool:
        """Return True if the markup tags in `text` are well-formed.

        Rules:
        - Opening tag: `[tag]` or `[tag attr=...]` pushes `tag` onto a stack.
        - Closing tag: `[/tag]` pops and must match last opened tag.
        - Nameless closing `[/]` pops the top of the stack.
        - Tag name is taken as the first token of the bracket content.
        - On any unmatched, missing, or malformed brackets/tags a
          `MarkupError` is raised describing the problem.
        """
        stack: List[str] = []
        i = 0
        n = len(text)

        def _is_escaped(s: str, idx: int) -> bool:
            """Return True if character at idx is escaped by an odd number of backslashes."""
            # count consecutive backslashes immediately before idx
            bs = 0
            j = idx - 1
            while j >= 0 and s[j] == "\\":
                bs += 1
                j -= 1
            return (bs % 2) == 1

        while i < n:
            ch = text[i]
            if ch == "[":
                # if this '[' is escaped (preceded by an odd number of backslashes),
                # treat it as literal text and ignore as a tag start
                if _is_escaped(text, i):
                    i += 1
                    continue
                
                # otherwise it starts a tag
                # find closing bracket
                j = text.find("]", i + 1)
                if j == -1:
                    raise MarkupError("unclosed '[': missing ']' for an opening bracket")

                content = text[i + 1 : j].strip()
                if not content:
                    # empty brackets `[]` are invalid
                    raise MarkupError("empty tag '[]' is invalid")

                # determine name (handle closing tags) using regex
                is_closing = content.startswith("/")

                if is_closing:
                    # content after the slash (may be empty for nameless close)
                    name_part = content[1:].lstrip()
                    if not name_part:
                        # nameless closing tag '[/]' pops the top of the stack
                        if not stack:
                            raise MarkupError("nameless closing tag '[/]' with no open tags to close")
                        stack.pop()
                    else:
                        m = _TAG_NAME_RE.match(name_part)
                        if not m:
                            raise MarkupError(f"invalid closing tag '[/{name_part}]'")
                        name = m.group(1)
                        if not stack:
                            raise MarkupError(f"closing tag '[/{name}]' with no matching opening tag")
                        last = stack.pop()
                        if last != name:
                            raise MarkupError(f"mismatched closing tag '[/{name}]', expected '[/{last}]'")
                else:
                    # opening tag: use only the first token as the tag name
                    m = _TAG_NAME_RE.match(content)
                    if not m:
                        raise MarkupError(f"invalid opening tag '[{content}]'")
                    name = m.group(1)
                    stack.append(name)

                i = j + 1
            else:
                i += 1

        if stack:
            # unclosed tags remain on the stack
            last = stack[-1]
            raise MarkupError(f"unclosed tag '[{last}]'")
        return True
