import json
import io
from time import time
from rich.console import Console
from rich.pretty import Pretty


console = Console(file=io.StringIO(), color_system="truecolor", width=100)

with open("cats.json") as fh:
    cats = json.load(fh)


start = time()
pretty = Pretty(cats)
console.print(pretty, overflow="ignore", crop=False)
taken = (time() - start) * 1000


print(console.file.getvalue())
print(f"{taken:.1f}")
