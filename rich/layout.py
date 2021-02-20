from .align import Align
from .console import Console, ConsoleOptions, RenderResult, RenderableType
from .highlighter import ReprHighlighter
from ._loop import loop_last
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


class _Placeholder:
    """An internal renderable used as a Layout placeholder."""

    highlighter = ReprHighlighter()

    def __init__(self, layout: "Layout", style: StyleType = "") -> None:
        self.layout = layout
        self.style = style

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        width = options.max_width
        height = options.height or options.size.height
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
        direction (str, optional): Direction of split, one of "vertical" or "horizontal". Defaults to "vertical".
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
        height: int = None,
    ) -> None:
        self._renderable = renderable or _Placeholder(self)
        self.direction = direction
        self.size = size
        self.minimum_size = minimum_size
        self.ratio = ratio
        self.name = name
        self.visible = visible
        self.height = height
        self._children: List[Layout] = []

    def __repr__(self) -> str:
        return f"Layout(size={self.size!r}, minimum_size={self.size!r}, ratio={self.ratio!r}, name={self.name!r}, visible={self.visible!r})"

    @property
    def renderable(self) -> RenderableType:
        """Layout renderable."""
        return self if self._children else self._renderable

    @property
    def children(self) -> List["Layout"]:
        """Gets (visible) layout children."""
        return [child for child in self._children if child.visible]

    def get(self, name: str) -> Optional["Layout"]:
        """Get a named layout, or None if it doesn't exist.

        Args:
            name (str): Name of layout.

        Returns:
            Optional[Layout]: Layout instance or None if no layout was found.
        """
        if self.name == name:
            return self
        else:
            for child in self._children:
                named_layout = child.get(name)
                if named_layout is not None:
                    return named_layout
        return None

    def __getitem__(self, name: str) -> "Layout":
        layout = self.get(name)
        if layout is None:
            raise KeyError(f"No layout with name {name!r}")
        return layout

    @property
    def tree(self) -> "Tree":
        """Get a tree renderable to show layout structure."""
        from rich.highlighter import ReprHighlighter
        from rich.text import Text
        from rich.tree import Tree

        highlighter = ReprHighlighter()

        def summary(layout) -> "Text":
            name = repr(layout.name) + " " if layout.name else ""
            direction = (
                ("➡" if layout.direction == "horizontal" else "⬇")
                if layout._children
                else "■"
            )
            if layout.size:
                _summary = highlighter(f"{direction} {name}(size={layout.size})")
            else:
                _summary = highlighter(f"{direction} {name}(ratio={layout.ratio})")
            _summary.stylize("" if layout.visible else "dim")
            return _summary

        layout = self
        tree = Tree(summary(layout), highlight=True)

        def recurse(tree, layout):
            for child in layout._children:
                recurse(tree.add(summary(child)), child)

        recurse(tree, self)
        return tree

    def split(self, *layouts, direction: Direction = None) -> None:
        """Split the layout in to multiple sub-layours.

        Args:
            *layouts (Layout): Positional arguments should be (sub) Layout instances.
            direction (Direction, optional): One of "horizontal" or "vertical" or None for no change. Defaults to None.
        """
        if direction is not None:
            self.direction = direction
        self._children.extend(layouts)

    def update(self, renderable: RenderableType) -> None:
        """Update renderable.

        Args:
            renderable (RenderableType): New renderable object.
        """
        self._renderable = renderable

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        render_options = options.update(
            height=options.height or self.height or options.size.height
        )
        if not self.children:
            for line in console.render_lines(
                self._renderable or "", render_options, new_lines=True
            ):
                yield from line

        elif self.direction == "vertical":
            yield from self._render_vertical(console, render_options)
        elif self.direction == "horizontal":
            yield from self._render_horizontal(console, render_options)

    def _render_horizontal(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        render_widths = ratio_resolve(options.max_width, self.children)
        renders = [
            console.render_lines(child, options.update(width=render_width))
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
            console.render_lines(
                child.renderable, options.update(height=render_height), new_lines=True
            )
            for child, render_height in zip(self.children, render_heights)
        ]
        for render in renders:
            for line in render:
                yield from line


if __name__ == "__main__":  # type: ignore
    from rich.console import Console
    from rich.panel import Panel

    console = Console()
    layout = Layout()

    layout.split(
        Layout(name="header", size=3),
        Layout(ratio=1, name="main"),
        Layout(size=10, name="footer"),
    )

    layout["main"].split(
        Layout(name="side"), Layout(name="body", ratio=2), direction="horizontal"
    )

    layout["side"].split(Layout(), Layout())

    console.print(layout)
