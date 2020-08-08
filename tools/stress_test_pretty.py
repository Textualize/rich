from rich.console import Console
from rich.pretty import Pretty

DATA = {
    "foo": [1, 2, 3, (1, 2, 3), {4, 5, 6, (7, 8, 9)}, "Hello, World"],
    "bar": [None, False, True],
}

console = Console()
for w in range(100):
    console.print(DATA, width=w)

