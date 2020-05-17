from rich.console import Console
from rich.align import Align
from rich.table import Table
from rich.text import Text
from rich.pretty import Pretty

table = Table("Foo", "Bar")
table.add_row("1", "2")

c = Console()
c.log(locals(), justify="right")
c.print(locals(), justify="right")
c.log(Text("Hello"), justify="right")
