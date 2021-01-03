from typing import Iterable, List, NamedTuple, Tuple

from .console import Console, ConsoleOptions, RenderResult, RenderableType
from ._loop import loop_first, loop_last
from .segment import Segment
from .style import Style, StyleType


class Tree:
    def __init__(
        self, renderable: RenderableType, line_style: StyleType = "tree.line"
    ) -> None:
        self.renderable = renderable
        self.line_style = line_style
        self.children: List[Tree] = []

    def add(self, renderable: RenderableType, line_style: StyleType = None) -> "Tree":
        node = Tree(
            renderable, line_style=self.line_style if line_style is None else line_style
        )
        self.children.append(node)
        return node

    def __rich_console__(
        self, console: "Console", options: "ConsoleOptions"
    ) -> "RenderResult":

        stack: List[Iterable[Tuple[bool, Tree]]] = []
        pop = stack.pop
        push = stack.append
        new_line = Segment.line()

        line_style = console.get_style(self.line_style)
        SPACE, CONTINUE, FORK, END = [
            Segment("    ", line_style),
            Segment("│   ", line_style),
            Segment("├── ", line_style),
            Segment("└── ", line_style),
        ]
        levels: List[Segment] = [SPACE]
        push(loop_last([self]))

        while stack:
            stack_node = pop()
            try:
                last, node = next(stack_node)
            except StopIteration:
                levels.pop()
                if levels:
                    levels[-1] = FORK
                continue
            push(stack_node)
            if last:
                levels[-1] = END.with_style(levels[-1].style)
            line_style = console.get_style(node.line_style)

            lines_length = sum(level.cell_length for level in levels[1:])
            renderable_lines = console.render_lines(
                node.renderable,
                options.update(width=options.max_width - lines_length),
            )

            prefix = levels[1:]
            for first, line in loop_first(renderable_lines):
                yield from prefix
                yield from line
                yield new_line
                if first:
                    prefix = levels[1:-1] + [
                        SPACE if last else CONTINUE.with_style(line_style)
                    ]

            if node.children:
                levels[-1] = SPACE if last else CONTINUE
                levels.append(
                    END.with_style(line_style)
                    if len(node.children) == 1
                    else FORK.with_style(line_style)
                )
                push(loop_last(node.children))


# if __name__ == "__main__":
#     from rich import print
#     from rich.console import Console
#     from rich.panel import Panel

#     tree = Tree("Root")
#     foo_node = tree.add("Foo")
#     foo_node.add("1")
#     two_node = foo_node.add("2", line_style="red")
#     two_node.add(Panel("hello"))
#     two_node.add("[bold magenta]World!").add("foo").add("bar")
#     foo_node.add("3")
#     tree.add("bar")
#     tree.add("baz")

#     console = Console()
#     console.print(tree, width=40)
#     console.print(two_node)

if __name__ == "__main__":

    from rich.console import RenderGroup
    from rich.markdown import Markdown
    from rich.panel import Panel
    from rich.syntax import Syntax
    from rich.table import Table

    table = Table(row_styles=["", "dim"])

    table.add_column("Released", style="cyan", no_wrap=True)
    table.add_column("Title", style="magenta")
    table.add_column("Box Office", justify="right", style="green")

    table.add_row("Dec 20, 2019", "Star Wars: The Rise of Skywalker", "$952,110,690")
    table.add_row("May 25, 2018", "Solo: A Star Wars Story", "$393,151,347")
    table.add_row("Dec 15, 2017", "Star Wars Ep. V111: The Last Jedi", "$1,332,539,889")
    table.add_row("Dec 16, 2016", "Rogue One: A Star Wars Story", "$1,332,439,889")

    code = """\
class Segment(NamedTuple):
    text: str = ""    
    style: Optional[Style] = None    
    is_control: bool = False    
"""
    syntax = Syntax(code, "python", theme="monokai", line_numbers=True)

    markdown = Markdown(
        """\
## Header 2
> Hello, World!
> 
> Markdown _all_ the things
"""
    )

    root = Tree(":open_file_folder: The Root node", line_style="cyan")

    node = root.add(":file_folder: Renderables")
    simple_node = node.add(":file_folder: [bold red]Atomic", line_style="green")
    simple_node.add(RenderGroup("📄 Syntax", syntax))
    simple_node.add(RenderGroup("📄 Markdown", markdown))

    containers_node = node.add(":file_folder: [bold red]Containers", line_style="blue")
    panel = Panel.fit("Just a panel", border_style="red")
    containers_node.add(RenderGroup("📄 Panels", panel))

    containers_node.add(RenderGroup("📄 [b magenta]Table", table))

    console = Console()
    console.print(root)