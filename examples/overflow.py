from typing import List
from rich.console import Console, OverflowMethod
from rich.text import Text

console = Console()
supercali = "supercalifragilisticexpialidocious"

overflow_methods: List[OverflowMethod] = ["fold", "crop", "ellipsis"]
for overflow in overflow_methods:
    console.rule(overflow)
    console.print(supercali, overflow=overflow, width=10)
