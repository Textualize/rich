from __future__ import annotations

from typing import Tuple

from .console import Console, ConsoleOptions, ConsoleRenderable, RenderResult
from .text import Text
from .styled_text import StyledText

BOX = """\
┌─┐
│ │
└─┘
"""


class Panel:
    def __init__(self, *contents: ConsoleRenderable) -> None:
        self.contents: Tuple[ConsoleRenderable, ...] = contents

    def __console__(self, console: Console, options: ConsoleOptions) -> RenderResult:

        width = options.max_width
        contents_width = width - 2

        child_options = options.copy()
        child_options.max_width = contents_width

        lines = console.render_lines(self.contents, child_options)
        # contents = list(console.render_all(self.contents, child_options))
        # lines = Text.reformat(contents_width, contents)

        box = BOX
        top_left = box[0]
        top = box[1]
        top_right = box[2]
        left = box[4]
        right = box[6]
        bottom_left = box[8]
        bottom = box[9]
        bottom_right = box[10]

        line_start = StyledText(left)
        line_end = StyledText(f"{right}\n")

        yield StyledText(f"{top_left}{top * contents_width}{top_right}\n")
        for line in lines:
            yield line_start
            yield from line
            yield line_end
        yield StyledText(f"{bottom_left}{bottom * contents_width}{bottom_right}\n")
