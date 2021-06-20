"""

Use Bar to renderer a sort-of circle.

"""
import math

from rich.align import Align
from rich.bar import Bar
from rich.color import Color
from rich import print


SIZE = 40

for row in range(SIZE):
    y = (row / (SIZE - 1)) * 2 - 1
    x = math.sqrt(1 - y * y)
    color = Color.from_rgb((1 + y) * 127.5, 0, (1 + y) * 127.5)
    bar = Bar(2, width=SIZE * 2, begin=1 - x, end=1 + x, color=color)
    print(Align.center(bar))
