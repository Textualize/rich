from dataclasses import dataclass, field
from itertools import chain
from typing import (
    Iterable,
    List,
    NamedTuple,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
    TYPE_CHECKING,
    Union,
)
from typing_extensions import Literal

from . import box

if TYPE_CHECKING:
    from .console import (
        Console,
        ConsoleOptions,
        ConsoleRenderable,
        JustifyValues,
        RenderableType,
        RenderResult,
    )
from . import errors
from .padding import Padding, PaddingDimensions
from .segment import Segment
from .style import Style
from .text import Text
from ._render_width import RenderWidth
from ._tools import iter_first_last, iter_first, iter_last, ratio_divide


T = TypeVar("T")


def _pick_first(values: Iterable[Optional[T]], final: T) -> T:
    """Pick first non-None value."""
    for value in values:
        if value is not None:
            return value
    return final


@dataclass
class Column:
    """Defines a column in a table."""

    header: Union[str, "ConsoleRenderable"] = ""
    footer: Union[str, "ConsoleRenderable"] = ""
    header_style: Union[str, Style] = "table.header"
    footer_style: Union[str, Style] = "table.footer"
    style: Union[str, Style] = "none"
    justify: "JustifyValues" = "left"
    width: Optional[int] = None
    ratio: Optional[int] = None
    _cells: List["ConsoleRenderable"] = field(default_factory=list)

    @property
    def cells(self) -> Iterable["ConsoleRenderable"]:
        """Get all cells in the column, not including header."""
        yield from self._cells

    @property
    def flexible(self) -> bool:
        """Check if this column is flexible."""
        return self.ratio is not None

    @property
    def header_renderable(self) -> "ConsoleRenderable":
        return (
            Text.from_markup(self.header, style=self.header_style or "")
            if isinstance(self.header, str)
            else self.header
        )

    @property
    def footer_renderable(self) -> "ConsoleRenderable":
        return (
            Text.from_markup(self.footer, style=self.footer_style or "")
            if isinstance(self.footer, str)
            else self.footer
        )


class _Cell(NamedTuple):

    style: Union[str, Style]
    renderable: "ConsoleRenderable"


class Table:
    columns: List[Column]

    def __init__(
        self,
        *headers: Union[Column, str],
        title: str = None,
        footer: str = None,
        width: int = None,
        box: Optional[box.Box] = box.DOUBLE_EDGE,
        padding: PaddingDimensions = (0, 1),
        pad_edge: bool = True,
        expand: bool = False,
        show_header: bool = True,
        show_footer: bool = False,
        show_edge: bool = True,
        style: Union[str, Style] = "none",
        header_style: Union[str, Style] = None,
        footer_style: Union[str, Style] = None,
        border_style: Union[str, Style] = None,
        title_style: Union[str, Style] = None,
    ) -> None:
        self.columns = [
            (Column(header) if isinstance(header, str) else header)
            for header in headers
        ]
        self.title = title
        self.width = width
        self.box = box
        self._padding = Padding.unpack(padding)
        self.pad_edge = pad_edge
        self.expand = expand
        self.show_header = show_header
        self.show_footer = show_footer
        self.show_edge = show_edge
        self.style = style
        self.header_style = header_style
        self.footer_style = footer_style
        self.border_style = border_style
        self.title_style = title_style
        self._row_count = 0

    @property
    def padding(self) -> Tuple[int, int, int, int]:
        return self._padding

    @padding.setter
    def padding(self, padding: PaddingDimensions) -> "Table":
        self._padding = Padding.unpack(padding)
        return self

    def add_column(
        self,
        header: Union[str, "ConsoleRenderable"] = "",
        footer: Union[str, "ConsoleRenderable"] = "",
        header_style: Union[str, Style] = None,
        footer_style: Union[str, Style] = None,
        style: Union[str, Style] = None,
        justify: "JustifyValues" = "left",
        width: int = None,
        ratio: int = None,
    ):
        """Add a column to the table.
        
        Args:
            header (Union[str, ConsoleRenderable], optional): Text or renderable for the header.
                Defaults to "".
            footer (Union[str, ConsoleRenderable], optional): Text or renderable for the footer.
                Defaults to "".
            header_style (Union[str, Style], optional): Style for the header. Defaults to "none".
            footer_style (Union[str, Style], optional): Style for the header. Defaults to "none".
            style (Union[str, Style], optional): Style for the column cells. Defaults to "none".
            justify (JustifyValues, optional): Alignment for cells. Defaults to "left".
            width (int, optional): A minimum width in characters. Defaults to None.
            ratio (int, optional): Flexible ratio for the column. Defaults to None.
        """
        column = Column(
            header=header,
            footer=footer,
            header_style=_pick_first((header_style, self.header_style), "table.header"),
            footer_style=_pick_first((footer_style, self.footer_style), "table.footer"),
            style=_pick_first((style, self.style), "table.cell"),
            justify=justify,
            width=width,
            ratio=ratio,
        )
        self.columns.append(column)

    def add_row(self, *renderables: Optional[Union[str, "ConsoleRenderable"]]) -> None:
        from .console import ConsoleRenderable

        def add_cell(column: Column, renderable: ConsoleRenderable):
            column._cells.append(renderable)

        cell_renderables: List[Optional[Union[str, ConsoleRenderable]]] = list(
            renderables
        )

        columns = self.columns
        if len(cell_renderables) < len(columns):
            cell_renderables = [
                *cell_renderables,
                *[None] * (len(columns) - len(cell_renderables)),
            ]
        for index, renderable in enumerate(cell_renderables):
            if index == len(columns):
                column = Column()
                for _ in range(self._row_count):
                    add_cell(column, Text(""))
                self.columns.append(column)
            else:
                column = columns[index]
            if isinstance(renderable, ConsoleRenderable):
                add_cell(column, renderable)
            elif renderable is None:
                add_cell(column, Text(""))
            elif isinstance(renderable, str):
                add_cell(column, Text.from_markup(renderable))
            else:
                raise errors.NotRenderableError(
                    f"unable to render {renderable!r}; str or object with a __console__ method is required"
                )
        self._row_count += 1

    def __console__(
        self, console: "Console", options: "ConsoleOptions"
    ) -> "RenderResult":

        max_width = options.max_width
        if self.width is not None:
            max_width = min(self.width, max_width)

        if self.box:
            max_width -= len(self.columns)
            if self.show_edge:
                max_width -= 2
        widths = self._calculate_column_widths(max_width)
        table_width = sum(widths) + len(self.columns) + (2 if self.box else 0)
        if self.title:
            title_text = Text.from_markup(self.title, style=self.title_style or "")
            wrapped_title = title_text.wrap(table_width, "center")
            yield wrapped_title
        yield from self._render(console, options, widths)

    def _calculate_column_widths(self, max_width: int) -> List[int]:
        """Calculate the widths of each column."""
        columns = self.columns
        width_ranges = [
            self._measure_column(column_index, column, max_width)
            for column_index, column in enumerate(columns)
        ]

        widths = [_range.maximum or 1 for _range in width_ranges]
        padding_width = self.padding[1] + self.padding[3]
        if self.expand:
            ratios = [col.ratio or 0 for col in columns if col.flexible]
            if any(ratios):
                fixed_widths = [_range.maximum for _range in width_ranges]
                fixed_widths = [
                    _range.minimum if column.flexible else _range.maximum
                    for _range, column in zip(width_ranges, columns)
                ]
                flex_minimum = [
                    (column.width or 0) + padding_width
                    for column in columns
                    if column.flexible
                ]
                flexible_width = max_width - sum(fixed_widths)

                flex_widths = ratio_divide(flexible_width, ratios, flex_minimum)
                iter_flex_widths = iter(flex_widths)
                for index, column in enumerate(columns):
                    if column.flexible:
                        widths[index] = fixed_widths[index] + next(iter_flex_widths)
        table_width = sum(widths)

        if table_width > max_width:
            flex_widths = [_range.span for _range in width_ranges]
            if not any(flex_widths):
                flex_widths = [1] * len(flex_widths)
            excess_width = table_width - max_width
            widths = [
                width - excess_width
                for width, excess_width in zip(
                    widths, ratio_divide(excess_width, flex_widths)
                )
            ]
        elif table_width < max_width and self.expand:
            pad_widths = ratio_divide(max_width - table_width, widths)
            widths = [_width + pad for _width, pad in zip(widths, pad_widths)]

        return widths

    def _get_cells(self, column_index: int, column: Column) -> Iterable[_Cell]:
        """Get all the cells with padding and optional header."""

        padding = self.padding
        any_padding = any(padding)

        first = column_index == 0
        last = column_index == len(self.columns) - 1

        def add_padding(renderable: "ConsoleRenderable") -> "ConsoleRenderable":
            if not any_padding:
                return renderable
            top, right, bottom, left = padding
            if not self.pad_edge:
                if first:
                    left = 0
                if last:
                    right = 0
            return Padding(renderable, (top, right, bottom, left))

        if self.show_header:
            yield _Cell(column.header_style, add_padding(column.header_renderable))
        for cell in column.cells:
            yield _Cell(column.style, add_padding(cell))
        if self.show_footer:
            yield _Cell(column.footer_style, add_padding(column.footer_renderable))

    def _measure_column(
        self, column_index: int, column: Column, max_width: int
    ) -> RenderWidth:
        """Get the minimum and maximum width of the column."""
        padding_width = self.padding[1] + self.padding[3]
        if column.width is not None:
            # Fixed width column
            return RenderWidth(
                column.width + padding_width, column.width + padding_width
            )
        # Flexible column, we need to measure contents
        min_widths: List[int] = []
        max_widths: List[int] = []
        append_min = min_widths.append
        append_max = max_widths.append
        get_render_width = RenderWidth.get
        for cell in self._get_cells(column_index, column):
            _min, _max = get_render_width(cell.renderable, max_width)
            append_min(_min)
            append_max(_max)
        return RenderWidth(
            max(min_widths) if min_widths else 1,
            max(max_widths) if max_widths else max_width,
        )

    def _render(
        self, console: "Console", options: "ConsoleOptions", widths: List[int]
    ) -> "RenderResult":
        table_style = console.get_style(self.style or "")

        border_style = table_style + console.get_style(self.border_style or "")
        rows: Iterable[Tuple[_Cell, ...]] = zip(
            *(
                self._get_cells(column_index, column)
                for column_index, column in enumerate(self.columns)
            )
        )
        box = self.box
        new_line = Segment.line()

        columns = self.columns
        show_header = self.show_header
        show_footer = self.show_footer
        show_edge = self.show_edge

        if box and show_edge:
            yield Segment(box.get_top(widths), border_style)

        for first, last, row in iter_first_last(rows):
            max_height = 1
            cells: List[List[List[Segment]]] = []
            for width, cell, column in zip(widths, row, columns):
                render_options = options.update(width=width, justify=column.justify)
                cell_style = table_style + console.get_style(cell.style)
                lines = console.render_lines(
                    cell.renderable, render_options, style=cell_style
                )
                max_height = max(max_height, len(lines))
                cells.append(lines)

            cells[:] = [
                Segment.set_shape(_cell, width, max_height, style=table_style)
                for width, _cell in zip(widths, cells)
            ]

            if box:
                if last and show_footer:
                    yield Segment(
                        box.get_row(widths, "foot", edge=show_edge), border_style
                    )
                if first:
                    left = Segment(box.head_left, border_style)
                    right = Segment(box.head_right, border_style)
                    divider = Segment(box.head_vertical, border_style)
                elif last:
                    left = Segment(box.foot_left, border_style)
                    right = Segment(box.foot_right, border_style)
                    divider = Segment(box.foot_vertical, border_style)
                else:
                    left = Segment(box.mid_left, border_style)
                    right = Segment(box.mid_right, border_style)
                    divider = Segment(box.mid_vertical, border_style)

                for line_no in range(max_height):
                    if show_edge:
                        yield left
                    for last, rendered_cell in iter_last(cells):
                        yield from rendered_cell[line_no]
                        if not last:
                            yield divider
                    if show_edge:
                        yield right
                    yield new_line
            else:
                for line_no in range(max_height):
                    for rendered_cell in cells:
                        yield from rendered_cell[line_no]
                    yield new_line
            if box and first and show_header:
                yield Segment(box.get_row(widths, "head", edge=show_edge), border_style)

        if box and show_edge:
            yield Segment(box.get_bottom(widths), border_style)


if __name__ == "__main__":  # pragma: no cover

    from .console import Console
    from . import box

    c = Console()
    table = Table(
        Column(
            "Foo", footer=Text("Total", justify="right"), footer_style="bold", ratio=1
        ),
        Column("Bar", style="red", footer="123", ratio=1),
        box=box.SIMPLE,
        expand=True,
        show_footer=True,
        show_edge=True,
    )
    # table.columns[0].width = 50
    # table.columns[1].ratio = 1

    table.add_row("Hello, World! " * 8, "cake" * 10)
    from .markdown import Markdown

    table.add_row(Markdown("# This is *Markdown*!"), "More text", "Hello WOrld")
    table.columns[0].justify = "center"
    table.columns[1].justify = "right"

    c.print(table)
