import io
import json
from time import time

from rich.console import Console
from rich.pretty import Pretty

console = Console(file=io.StringIO(), color_system="truecolor", width=100)

with open("cats.json") as fh:
    cats = json.load(fh)


console.begin_capture()
start = time()
pretty = Pretty(cats)
console.print(pretty, overflow="ignore", crop=False)
result = console.end_capture()
taken = (time() - start) * 1000
print(result)

print(console.file.getvalue())
print(f"{taken:.1f}")
