"""

This example demonstrates how to write a custom highlighter.

"""

# Note: You Must Install Rich First

# All Imports:
from random import randint
from rich import print
from rich.highlighter import Highlighter

# Creating The Rainbow Highlighter Class:
class RainbowHighlighter(Highlighter):

    # Defining The Highlight Function:
    def highlight(self, text):

        # Chooses A Random Colour For Each Letter In The String:
        for index in range(len(text)):
            text.stylize(f"color({randint(16, 255)})", index, index + 1)

# Calling The Rainbow Highlighter Class:
rainbow = RainbowHighlighter()

# Printing The Text That Has To Be Rainbow Highlighted:
print(rainbow("I must not fear. Fear is the mind-killer."))
