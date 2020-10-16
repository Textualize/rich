"""

Use Bar to renderer a sort-of cirlce.

"""
import math

from rich.bar import Bar
from rich import print


SIZE = 40

for row in range(SIZE):
    y = (row / SIZE) * 2 - 1
    x = math.sqrt(1 - y * y)
    bar = Bar(1, width=SIZE * 2, begin=1 - x, end=x, color="red")
    print(bar)
