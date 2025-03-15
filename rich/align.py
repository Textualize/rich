import sys
from itertools import chain
from typing import TYPE_CHECKING, Iterable, Optional

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

from .constrain import Constrain
from .jupyter import JupyterMixin
from .measure import Measurement
from .segment import Segment
from .style import StyleType

if TYPE_CHECKING:
    from .console import Console, ConsoleOptions, RenderableType, RenderResult

AlignMethod = Literal["left", "center", "right"]
VerticalAlignMethod = Literal["top", "middle", "bottom"]

class Align(JupyterMixin):
    def __init__(
        self,
        renderable: "RenderableType",
        align: AlignMethod = "left",
        style: Optional[StyleType] = None,
        *,
        vertical: Optional[VerticalAlignMethod] = None,
        pad: bool = True,
        width: Optional[int] = None,
        height: Optional[int] = None,
    ) -> None:
        if align not in ("left", "center", "right"):
            raise ValueError(f'invalid align value: {align!r}')
        if vertical is not None and vertical not in ("top", "middle", "bottom"):
            raise ValueError(f'invalid vertical value: {vertical!r}')
        self.renderable = renderable
        self.align = align
        self.style = style
        self.vertical = vertical
        self.pad = pad
        self.width = width
        self.height = height

    def __repr__(self) -> str:
        return f"Align({self.renderable!r}, {self.align!r})"

    @classmethod
    def left(cls, renderable: "RenderableType", style: Optional[StyleType] = None, **kwargs) -> "Align":
        return cls(renderable, "left", style=style, **kwargs)

    @classmethod
    def center(cls, renderable: "RenderableType", style: Optional[StyleType] = None, **kwargs) -> "Align":
        return cls(renderable, "center", style=style, **kwargs)

    @classmethod
    def right(cls, renderable: "RenderableType", style: Optional[StyleType] = None, **kwargs) -> "Align":
        return cls(renderable, "right", style=style, **kwargs)

    def __rich_console__(self, console: "Console", options: "ConsoleOptions") -> "RenderResult":
        width = console.measure(self.renderable, options=options).maximum
        rendered = console.render(Constrain(self.renderable, min(width, self.width) if self.width else width), options.update(height=None))
        lines = list(Segment.split_lines(rendered))
        width, height = Segment.get_shape(lines)
        lines = Segment.set_shape(lines, width, height)
        new_line = Segment.line()
        excess_space = options.max_width - width
        style = console.get_style(self.style) if self.style else None

        def generate_segments() -> Iterable[Segment]:
            if excess_space <= 0:
                yield from chain.from_iterable(lines)
                yield new_line
            elif self.align == "left":
                pad = Segment(" " * excess_space, style) if self.pad else None
                for line in lines:
                    yield from line
                    if pad: yield pad
                    yield new_line
            elif self.align == "center":
                left = excess_space // 2
                pad = Segment(" " * left, style)
                pad_right = Segment(" " * (excess_space - left), style) if self.pad else None
                for line in lines:
                    if left: yield pad
                    yield from line
                    if pad_right: yield pad_right
                    yield new_line
            elif self.align == "right":
                pad = Segment(" " * excess_space, style)
                for line in lines:
                    yield pad
                    yield from line
                    yield new_line

        blank_line = Segment(f"{' ' * (self.width or options.max_width)}\n", style) if self.pad else Segment("\n")

        def blank_lines(count: int) -> Iterable[Segment]:
            for _ in range(count): yield blank_line

        vertical_height = self.height or options.height
        if self.vertical and vertical_height:
            top_space = (vertical_height - height) // 2 if self.vertical == "middle" else (vertical_height - height if self.vertical == "bottom" else 0)
            bottom_space = vertical_height - top_space - height
            iter_segments = chain(blank_lines(top_space), generate_segments(), blank_lines(bottom_space))
        else:
            iter_segments = generate_segments()

        if self.style:
            iter_segments = Segment.apply_style(iter_segments, console.get_style(self.style))
        yield from iter_segments

    def __rich_measure__(self, console: "Console", options: "ConsoleOptions") -> Measurement:
        return Measurement.get(console, options, self.renderable)

class VerticalCenter(JupyterMixin):
    def __init__(self, renderable: "RenderableType", style: Optional[StyleType] = None) -> None:
        self.renderable = renderable
        self.style = style

    def __repr__(self) -> str:
        return f"VerticalCenter({self.renderable!r})"

    def __rich_console__(self, console: "Console", options: "ConsoleOptions") -> "RenderResult":
        style = console.get_style(self.style) if self.style else None
        lines = console.render_lines(self.renderable, options.update(height=None), pad=False)
        width, _height = Segment.get_shape(lines)
        new_line = Segment.line()
        height = options.height or options.size.height
        top_space = (height - len(lines)) // 2
        bottom_space = height - top_space - len(lines)
        blank_line = Segment(f"{' ' * width}", style)

        def blank_lines(count: int) -> Iterable[Segment]:
            for _ in range(count):
                yield blank_line
                yield new_line

        if top_space > 0: yield from blank_lines(top_space)
        for line in lines:
            yield from line
            yield new_line
        if bottom_space > 0: yield from blank_lines(bottom_space)

    def __rich_measure__(self, console: "Console", options: "ConsoleOptions") -> Measurement:
        return Measurement.get(console, options, self.renderable)

if __name__ == "__main__":
    from rich.console import Console, Group
    from rich.highlighter import ReprHighlighter
    from rich.panel import Panel

    highlighter = ReprHighlighter()
    console = Console()

    panel = Panel(
        Group(
            Align.left(highlighter("align='left'")),
            Align.center(highlighter("align='center'")),
            Align.right(highlighter("align='right'")),
        ),
        width=60,
        style="on dark_blue",
        title="Align",
    )

    console.print(Align.center(panel, vertical="middle", style="on red", height=console.height))