from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

console = Console(width=16)

console.print(Panel("""这是对亚洲语言支持的测试。面对模棱两可的想法，拒绝猜测的诱惑。""", expand=False))

console.print(Panel(""":pile_of_poo:""", expand=False))

console.print(Panel(""":pile_of_poo::vampire::thumbs_up: """ * 5))
print("x" * 15)

console = Console()
table = Table()
table.add_column("这是对亚洲语言支持的测试。", justify="right")
console.print(table)
table.add_column("拒绝猜测的诱惑。")
console.print(table)
table.add_row("拒绝猜测的诱惑")
console.print(table)
