import sys
from itertools import chain
from typing import TYPE_CHECKING, Iterable, Optional

if sys.version_info < (3, 8):
    from typing_extensions import Literal  # pragma: no cover
else:
    from typing import Literal

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
    """Align a renderable by adding spaces if necessary."""

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
        if align not in AlignMethod.__args__:
            raise ValueError(f"Invalid align value: {align!r}")
        if vertical and vertical not in VerticalAlignMethod.__args__:
            raise ValueError(f"Invalid vertical value: {vertical!r}")
        
        self.renderable, self.align, self.style = renderable, align, style
        self.vertical, self.pad, self.width, self.height = vertical, pad, width, height

    def __repr__(self) -> str:
        return f"Align({self.renderable!r}, {self.align!r})"

    @classmethod
    def create(cls, renderable: "RenderableType", align: AlignMethod, **kwargs) -> "Align":
        return cls(renderable, align, **kwargs)

    left = classmethod(lambda cls, r, **kw: cls.create(r, "left", **kw))
    center = classmethod(lambda cls, r, **kw: cls.create(r, "center", **kw))
    right = classmethod(lambda cls, r, **kw: cls.create(r, "right", **kw))

    def __rich_console__(self, console: "Console", options: "ConsoleOptions") -> "RenderResult":
        width = console.measure(self.renderable, options).maximum
        rendered = console.render(
            Constrain(self.renderable, min(width, self.width) if self.width else width),
            options.update(height=None),
        )
        lines = list(Segment.split_lines(rendered))
        width, height = Segment.get_shape(lines)
        lines = Segment.set_shape(lines, width, height)
        excess_space = options.max_width - width
        style = console.get_style(self.style) if self.style else None

        def generate_segments() -> Iterable[Segment]:
            if excess_space <= 0:
                yield from (seg for line in lines for seg in (*line, Segment.line()))
            else:
                pad = Segment(" " * excess_space, style) if self.pad else None
                left_pad = Segment(" " * (excess_space // 2), style) if self.align == "center" else None
                for line in lines:
                    if self.align == "right":
                        yield pad
                    if left_pad:
                        yield left_pad
                    yield from line
                    if self.align in {"left", "center"} and pad:
                        yield pad
                    yield Segment.line()

        blank_line = Segment(" " * (self.width or options.max_width), style) if self.pad else Segment("\n")
        blank_lines = lambda count: (blank_line for _ in range(count))

        if self.vertical and self.height:
            space = self.height - height
            top, bottom = (space // 2, space - space // 2) if self.vertical == "middle" else (space, 0) if self.vertical == "bottom" else (0, space)
            segments = chain(blank_lines(top), generate_segments(), blank_lines(bottom))
        else:
            segments = generate_segments()
        
        yield from Segment.apply_style(segments, style) if self.style else segments

    def __rich_measure__(self, console: "Console", options: "ConsoleOptions") -> Measurement:
        return Measurement.get(console, options, self.renderable)
