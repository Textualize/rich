"""
Randomly Prints Names in random Colors to Show examples of how to use randbow text in an Text Generator.
"""
from random import randint

from rich import print
from rich.highlighter import Highlighter


class RainbowHighlighter(Highlighter):
    def highlight(self, text):
        for index in range(len(text)):
            text.stylize(f"color({randint(16, 255)})", index, index + 1)


i = [
    "Harland Feeley",
    "Rebbecca Lovins",
    "Josephina Lippincott",
    "Eboni Huwe",
    "Allyson Trombley",
    "Jordan Brisbin",
    "Chloe Goll",
    "Rodney Augustin",
    "Noemi Cusumano",
    "Agustina Buttner",
]

rainbow = RainbowHighlighter()

for x in i:
    print(rainbow(x) + "\n")
