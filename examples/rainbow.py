"""

This example demonstrates how to write a custom highlighter.

"""

from random import randint

from rich import print
from rich.highlighter import Highlighter


class RainbowHighlighter(Highlighter):
    def highlight(self, text):
        for index in range(len(text)):
            text.stylize(index, index + 1, str(randint(16, 255)))


rainbow = RainbowHighlighter()
print(rainbow("I must not fear. Fear is the mind-killer."))
