from rich.console import Console
from rich.panel import Panel

console = Console(width=16)

console.print(Panel("""这是对亚洲语言支持的测试。面对模棱两可的想法，拒绝猜测的诱惑。""", expand=False))

console.print(Panel(""":pile_of_poo:""", expand=False))

console.print(Panel(""":pile_of_poo::vampire::thumbs_up: """ * 5))
print("x" * 15)
