from typing import Iterable, List, NamedTuple, Tuple

from .console import Console, ConsoleOptions, RenderResult, RenderableType
from .jupyter import JupyterMixin
from ._loop import loop_first, loop_last
from .segment import Segment
from .style import Style, StyleStack, StyleType
from .styled import Styled


class Tree(JupyterMixin):
    def __init__(
        self,
        renderable: RenderableType,
        style: StyleType = "tree",
        guide_style: StyleType = "tree.line",
        expanded=True,
    ) -> None:
        """A renderable for a tree structure.

        Args:
            renderable (RenderableType): The renderable or text for the root node.
            style (StyleType, optional): Style of this tree. Defaults to "tree".
            guide_style (StyleType, optional): Style of the guide lines. Defaults to "tree.line".
            expanded (bool, optional): Also display children. Defaults to True.
        """

        self.renderable = renderable
        self.style = style
        self.guide_style = guide_style
        self.children: List[Tree] = []
        self.expanded = expanded

    def add(
        self,
        renderable: RenderableType,
        *,
        style: StyleType = None,
        guide_style: StyleType = None
    ) -> "Tree":
        node = Tree(
            renderable,
            style=self.style if style is None else style,
            guide_style=self.guide_style if guide_style is None else guide_style,
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

        get_style = console.get_style
        guide_style = get_style(self.guide_style)
        SPACE, CONTINUE, FORK, END = range(4)

        ASCII_GUIDES = ("    ", "|   ", "+-- ", "`-- ")
        TREE_GUIDES = [
            ("    ", "│   ", "├── ", "└── "),
            ("    ", "┃   ", "┣━━ ", "┗━━ "),
            ("    ", "║   ", "╠══ ", "╚══ "),
        ]
        _Segment = Segment

        def make_guide(index: int, style: Style = None) -> Segment:
            _style = guide_style if style is None else style
            if options.ascii_only:
                line = ASCII_GUIDES[index]
            else:
                guide = 1 if _style.bold else (2 if _style.underline2 else 0)
                line = TREE_GUIDES[guide][index]
            return _Segment(line, _style)

        levels: List[Segment] = [make_guide(CONTINUE)]
        push(loop_last([self]))

        guide_style_stack = StyleStack(get_style(self.guide_style))
        style_stack = StyleStack(get_style(self.style))

        while stack:
            stack_node = pop()
            try:
                last, node = next(stack_node)
            except StopIteration:
                levels.pop()
                if levels:
                    guide_style = levels[-1].style
                    levels[-1] = make_guide(FORK)
                    guide_style_stack.pop()
                    style_stack.pop()
                continue
            push(stack_node)
            if last:
                levels[-1] = make_guide(END, levels[-1].style)

            guide_style = guide_style_stack.current + get_style(node.guide_style)
            style = style_stack.current + get_style(node.style)

            renderable_lines = console.render_lines(
                Styled(node.renderable, style),
                options.update(
                    width=options.max_width
                    - sum(level.cell_length for level in levels[1:])
                ),
            )

            prefix = levels[1:]
            for first, line in loop_first(renderable_lines):
                if prefix:
                    yield from _Segment.apply_style(prefix, style.background_style)
                yield from line
                yield new_line
                if first and prefix:
                    prefix[-1] = make_guide(
                        SPACE if last else CONTINUE, prefix[-1].style
                    )

            if node.expanded and node.children:
                levels[-1] = make_guide(SPACE if last else CONTINUE, levels[-1].style)
                levels.append(make_guide(END if len(node.children) == 1 else FORK))
                style_stack.push(get_style(node.style))
                guide_style_stack.push(get_style(node.guide_style))
                push(loop_last(node.children))


# if __name__ == "__main__":
#     from rich import print
#     from rich.console import Console
#     from rich.panel import Panel

#     tree = Tree("Root")
#     foo_node = tree.add("Foo")
#     foo_node.add("1")
#     two_node = foo_node.add("2", guide_style="red")
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

    root = Tree(":open_file_folder: The Root node\n", guide_style="red")

    node = root.add(":file_folder: Renderables\n")
    simple_node = node.add(":file_folder: [bold red]Atomic\n", guide_style="uu green")
    simple_node.add(RenderGroup("📄 Syntax", syntax))
    simple_node.add(RenderGroup("📄 Markdown", markdown))

    containers_node = node.add(
        ":file_folder: [bold red]Containers", guide_style="bold magenta"
    )
    containers_node.expanded = True
    panel = Panel.fit("Just a panel", border_style="red")
    containers_node.add(RenderGroup("📄 Panels\n", panel))

    containers_node.add(RenderGroup("📄 [b magenta]Table", table))

    console = Console()
    console.print(root)