from .align import Align
from .console import Console, ConsoleOptions, RenderResult, RenderableType
from .highlighter import ReprHighlighter
from .panel import Panel
from .pretty import Pretty
from ._ratio import ratio_resolve
from .segment import Segment
from .style import StyleType


from typing import List, Optional, TYPE_CHECKING
from typing_extensions import Literal

Direction = Literal["horizontal", "vertical"]


if TYPE_CHECKING:
    from rich.tree import Tree


class Placeholder:
    highlighter = ReprHighlighter()

    def __init__(self, layout: "Layout", style: StyleType = "") -> None:
        self.layout = layout
        self.style = style

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        width = options.max_width
        height = options.height
        layout = self.layout

        layout_info = {
            "size": layout.size,
            "minimum_size": layout.minimum_size,
            "ratio": layout.ratio,
            "name": layout.name,
        }

        title = (
            f"{layout.name!r} ({width} x {height})"
            if layout.name
            else f"({width} x {height})"
        )
        yield Panel(
            Align.center(Pretty(layout_info), vertical="middle"),
            style=self.style,
            title=self.highlighter(title),
            border_style="blue",
        )


class Layout:
    """A renderable to divide a fixed height in to rows or columns.

    Args:
        renderable (RenderableType, optional): Renderable content, or None for placeholder. Defaults to None.
        size (int, optional): Optional fixed size of layout. Defaults to None.
        minimum_size (int, optional): Minimum size of layout. Defaults to 1.
        ratio (int, optional): Optional ratio for flexible layout. Defaults to 1.
        name (str, optional): Optional identifier for Layout. Defaults to None.
        visible (bool, optional): Visibility of layout. Defaults to True.
    """

    def __init__(
        self,
        renderable: RenderableType = None,
        *,
        direction: str = "vertical",
        size: int = None,
        minimum_size: int = 1,
        ratio: int = 1,
        name: str = None,
        visible: bool = True,
    ) -> None:
        self._renderable = renderable or Placeholder(self)
        self.direction = direction
        self.size = size
        self.minimum_size = minimum_size
        self.ratio = ratio
        self.name = name
        self.visible = visible
        self._children: List[Layout] = []

    def __repr__(self) -> str:
        return f"Layout(size={self.size!r}, minimum_size={self.size!r}, ratio={self.ratio!r}, name={self.name!r}, visible={self.visible!r})"

    @property
    def renderable(self) -> RenderableType:
        """Layout renderable."""
        return self if self._children else self._renderable

    # @renderable.setter
    # def renderable(self, renderable: RenderableType) -> None:
    #     self._renderable = renderable

    @property
    def children(self) -> List["Layout"]:
        """Gets (visible) layout children."""
        return [child for child in self._children if child.visible]

    def get(self, name) -> Optional["Layout"]:
        """Get a named layout."""
        if self.name == name:
            return self
        else:
            for child in self._children:
                named_layout = child.get(name)
                if named_layout is not None:
                    return named_layout
        return None

    def __getitem__(self, name) -> "Layout":
        layout = self.get(name)
        if layout is None:
            raise KeyError(f"No layout with name {name!r}")
        return layout

    @property
    def tree(self) -> "Tree":
        from rich.tree import Tree

        def summary(layout):
            name = repr(layout.name) + " " if layout.name else ""
            if layout.size:
                return f"{name}(size={layout.size})"
            else:
                return f"{name}(ratio={layout.ratio})"

        layout = self
        tree = Tree(summary(layout), highlight=True)

        def recurse(tree, layout):
            for child in layout.children:
                recurse(tree.add(summary(child)), child)

        recurse(tree, self)
        return tree

    def split(
        self,
        renderable: RenderableType = None,
        *,
        size: int = None,
        minimum_size: int = 1,
        ratio: int = 1,
        name: str = None,
        visible: bool = True,
        direction: Direction = "vertical",
    ):
        layout = Layout(
            renderable,
            size=size,
            minimum_size=minimum_size,
            ratio=ratio,
            name=name,
            visible=visible,
            direction=direction,
        )
        self._children.append(layout)
        return layout

    def update(self, renderable: RenderableType) -> None:
        """Update renderable.

        Args:
            renderable (RenderableType): New renderable object.
        """
        self._renderable = renderable

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        if not self.children:
            yield self._renderable or ""
        elif self.direction == "vertical":
            yield from self._render_vertical(console, options)
        elif self.direction == "horizontal":
            yield from self._render_horizontal(console, options)

    def _render_horizontal(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        render_widths = ratio_resolve(options.max_width, self.children)
        renders = [
            console.render_lines(child.renderable, options.update(width=render_width))
            for child, render_width in zip(self.children, render_widths)
        ]
        new_line = Segment.line()
        for lines in zip(*renders):
            for line in lines:
                yield from line
            yield new_line

    def _render_vertical(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        render_heights = ratio_resolve(options.height or console.height, self.children)
        renders = [
            console.render_lines(child.renderable, options.update(height=render_height))
            for child, render_height in zip(self.children, render_heights)
        ]
        new_line = Segment.line()
        for render in renders:
            for line in render:
                yield from line
                yield new_line


if __name__ == "__main__":  # type: ignore
    from rich.console import Console
    from rich.panel import Panel

    console = Console()
    layout = Layout()

    header = layout.split(name="header", size=3)
    body = layout.split(ratio=1, direction="horizontal")
    footer = layout.split(size=10, name="footer")

    side = body.split(name="side")
    body.split(name="body", ratio=2)

    side.split()
    side.split()

    console.print(layout)

    # from rich.live import Live
    # from time import sleep

    # with Live(layout, screen=True, refresh_per_second=2):
    #     try:
    #         while 1:
    #             sleep(1)
    #     except KeyboardInterrupt:
    #         pass
