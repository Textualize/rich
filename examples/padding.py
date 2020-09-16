from rich import print
from rich.padding import Padding

test = Padding("Hello", (2, 4), style="on blue", expand=False)
print(test)
