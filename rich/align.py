from typing import Iterable, TYPE_CHECKING

from typing_extensions import Literal
from .constrain import Constrain
from .jupyter import JupyterMixin
from .measure import Measurement
from .segment import Segment
from .style import StyleType


if TYPE_CHECKING:
    from .console import Console, ConsoleOptions, RenderResult, RenderableType

AlignValues = Literal["left", "center", "right"]
AlignMethod = AlignValues  # TODO: deprecate AlignValues


class Align(JupyterMixin):
    """Align a renderable by adding spaces if necessary.

    Args:
        renderable (RenderableType): A console renderable.
        align (AlignMethod): One of "left", "center", or "right""
        style (StyleType, optional): An optional style to apply to the background.
        pad (bool, optional): Pad the right with spaces. Defaults to True.
        width (int, optional): Restrict contents to given width, or None to use default width. Defaults to None.

    Raises:
        ValueError: if ``align`` is not one of the expected values.
    """

    def __init__(
        self,
        renderable: "RenderableType",
        align: AlignMethod,
        style: StyleType = None,
        *,
        pad: bool = True,
        width: int = None,
    ) -> None:
        if align not in ("left", "center", "right"):
            raise ValueError(
                f'invalid value for align, expected "left", "center", "right" (not {align!r})'
            )
        self.renderable = renderable
        self.align = align
        self.style = style
        self.pad = pad
        self.width = width

    def __repr__(self) -> str:
        return f"Align({self.renderable!r}, {self.align!r})"

    @classmethod
    def left(
        cls,
        renderable: "RenderableType",
        style: StyleType = None,
        *,
        pad: bool = True,
        width: int = None,
    ) -> "Align":
        """Align a renderable to the left."""
        return cls(renderable, "left", style=style, pad=pad, width=width)

    @classmethod
    def center(
        cls,
        renderable: "RenderableType",
        style: StyleType = None,
        *,
        pad: bool = True,
        width: int = None,
    ) -> "Align":
        """Align a renderable to the center."""
        return cls(renderable, "center", style=style, pad=pad, width=width)

    @classmethod
    def right(
        cls,
        renderable: "RenderableType",
        style: StyleType = None,
        *,
        pad: bool = True,
        width: int = None,
    ) -> "Align":
        """Align a renderable to the right."""
        return cls(renderable, "right", style=style, pad=pad, width=width)

    def __rich_console__(
        self, console: "Console", options: "ConsoleOptions"
    ) -> "RenderResult":

        align = self.align

        width = Measurement.get(console, self.renderable).maximum

        rendered = console.render(
            Constrain(
                self.renderable, width if self.width is None else min(width, self.width)
            ),
            options,
        )
        lines = list(Segment.split_lines(rendered))
        width, height = Segment.get_shape(lines)
        lines = Segment.set_shape(lines, width, height)
        new_line = Segment.line()
        excess_space = options.max_width - width
        style = console.get_style(self.style) if self.style is not None else None

        def generate_segments() -> Iterable[Segment]:
            if excess_space <= 0:
                # Exact fit
                for line in lines:
                    yield from line
                    yield new_line

            elif align == "left":
                # Pad on the right
                pad = Segment(" " * excess_space, style) if self.pad else None
                for line in lines:
                    yield from line
                    if pad:
                        yield pad
                    yield new_line

            elif align == "center":
                # Pad left and right
                left = excess_space // 2
                pad = Segment(" " * left, style)
                pad_right = (
                    Segment(" " * (excess_space - left), style) if self.pad else None
                )
                for line in lines:
                    if left:
                        yield pad
                    yield from line
                    if pad_right:
                        yield pad_right
                    yield new_line

            elif align == "right":
                # Padding on left
                pad = Segment(" " * excess_space, style)
                for line in lines:
                    yield pad
                    yield from line
                    yield new_line

        iter_segments = generate_segments()
        if self.style is not None:
            style = console.get_style(self.style)
            iter_segments = Segment.apply_style(iter_segments, style)
        return iter_segments

    def __rich_measure__(self, console: "Console", max_width: int) -> Measurement:
        measurement = Measurement.get(console, self.renderable, max_width)
        return measurement


class VerticalCenter(JupyterMixin):
    """Vertically aligns a renderable.

    Args:
        renderable (RenderableType): A renderable object.
    """

    def __init__(
        self,
        renderable: "RenderableType",
        style: StyleType = None,
    ) -> None:
        self.renderable = renderable
        self.style = style

    def __repr__(self) -> str:
        return f"VerticalCenter({self.renderable!r})"

    def __rich_console__(
        self, console: "Console", options: "ConsoleOptions"
    ) -> "RenderResult":
        style = console.get_style(self.style) if self.style is not None else None
        lines = console.render_lines(self.renderable, options, pad=False)
        width, _height = Segment.get_shape(lines)
        new_line = Segment.line()
        height = console.size.height
        top_space = (height - len(lines)) // 2
        bottom_space = height - top_space - len(lines)
        blank_line = Segment(f"{' ' * width}", style)

        def blank_lines(count) -> Iterable[Segment]:
            for _ in range(count):
                yield blank_line
                yield new_line

        if top_space > 0:
            yield from blank_lines(top_space)
        for line in lines:
            yield from line
            yield new_line
        if bottom_space > 0:
            yield from blank_lines(bottom_space)

    def __rich_measure__(self, console: "Console", max_width: int) -> Measurement:
        measurement = Measurement.get(console, self.renderable, max_width)
        return measurement


if __name__ == "__main__":  # pragma: no cover
    from rich.console import Console, RenderGroup
    from rich.highlighter import ReprHighlighter
    from rich.panel import Panel

    highlighter = ReprHighlighter()
    console = Console()

    panel = Align.center(
        Panel(
            RenderGroup(
                Align(highlighter("align='left'"), "left"),
                Align(highlighter("align='center'"), "center"),
                Align(highlighter("align='right'"), "right"),
            ),
            width=60,
            style="on dark_blue",
            title="VerticalCenter",
        ),
        style="on red",
    )
    console.print(VerticalCenter(panel, style="on red"))
