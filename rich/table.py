from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Iterable, List, NamedTuple, Optional, Tuple, Union

from . import box, errors
from ._loop import loop_first_last, loop_last
from ._ratio import ratio_distribute, ratio_reduce
from .jupyter import JupyterMixin
from .measure import Measurement
from .padding import Padding, PaddingDimensions
from .protocol import is_renderable
from .segment import Segment
from .style import Style, StyleType
from .styled import Styled
from .text import Text, TextType

if TYPE_CHECKING:
    from .console import (
        Console,
        ConsoleOptions,
        JustifyMethod,
        OverflowMethod,
        RenderableType,
        RenderResult,
    )


@dataclass
class Column:
    """Defines a column in a table."""

    index: int
    """Index of column."""

    header: "RenderableType" = ""
    """RenderableType: Renderable for the header (typically a string)"""

    footer: "RenderableType" = ""
    """RenderableType: Renderable for the footer (typically a string)"""

    header_style: StyleType = "table.header"
    """StyleType: The style of the header."""

    footer_style: StyleType = "table.footer"
    """StyleType: The style of the footer."""

    style: StyleType = "none"
    """StyleType: The style of the column."""

    justify: "JustifyMethod" = "left"
    """str: How to justify text within the column ("left", "center", "right", or "full")"""

    overflow: "OverflowMethod" = "ellipsis"

    width: Optional[int] = None
    """Optional[int]: Width of the column, or ``None`` (default) to auto calculate width."""

    ratio: Optional[int] = None
    """Optional[int]: Ratio to use when calculating column width, or ``None`` (default) to adapt to column contents."""

    no_wrap: bool = False
    """bool: Prevent wrapping of text within the column. Defaults to ``False``."""

    _cells: List["RenderableType"] = field(default_factory=list)

    @property
    def cells(self) -> Iterable["RenderableType"]:
        """Get all cells in the column, not including header."""
        yield from self._cells

    @property
    def flexible(self) -> bool:
        """Check if this column is flexible."""
        return self.ratio is not None


class _Cell(NamedTuple):
    """A single cell in a table."""

    style: StyleType
    """Style to apply to cell."""
    renderable: "RenderableType"
    """Cell renderable."""


class Table(JupyterMixin):
    """A console renderable to draw a table.
    
    Args:
        *headers (Union[Column, str]): Column headers, either as a string, or :class:`~rich.table.Column` instance.
        title (Union[str, Text], optional): The title of the table rendered at the top. Defaults to None.
        caption (Union[str, Text], optional): The table caption rendered below. Defaults to None.
        width (int, optional): The width in characters of the table, or ``None`` to automatically fit. Defaults to None.
        box (box.Box, optional): One of the constants in box.py used to draw the edges (see :ref:`appendix_box`). Defaults to box.HEAVY_HEAD.
        safe_box (Optional[bool], optional): Disable box characters that don't display on windows legacy terminal with *raster* fonts. Defaults to True.
        padding (PaddingDimensions, optional): Padding for cells (top, right, bottom, left). Defaults to (0, 1).
        collapse_padding (bool, optional): Enable collapsing of padding around cells. Defaults to False.
        pad_edge (bool, optional): Enable padding of edge cells. Defaults to True.
        expand (bool, optional): Expand the table to fit the available space if ``True``, otherwise the table width will be auto-calculated. Defaults to False.
        show_header (bool, optional): Show a header row. Defaults to True.
        show_footer (bool, optional): Show a footer row. Defaults to False.
        show_edge (bool, optional): Draw a box around the outside of the table. Defaults to True.
        show_lines (bool, optional): Draw lines between every row. Defaults to False.
        leading (bool, optional): Number of blank lines between rows (precludes ``show_lines``). Defaults to 0.
        style (Union[str, Style], optional): Default style for the table. Defaults to "none".
        row_styles (List[Union, str], optional): Optional list of row styles, if more that one style is give then the styles will alternate. Defaults to None.
        header_style (Union[str, Style], optional): Style of the header. Defaults to None.
        footer_style (Union[str, Style], optional): Style of the footer. Defaults to None.
        border_style (Union[str, Style], optional): Style of the border. Defaults to None.
        title_style (Union[str, Style], optional): Style of the title. Defaults to None.
        caption_style (Union[str, Style], optional): Style of the caption. Defaults to None.
    """

    columns: List[Column]

    def __init__(
        self,
        *headers: Union[Column, str],
        title: TextType = None,
        caption: TextType = None,
        width: int = None,
        box: Optional[box.Box] = box.HEAVY_HEAD,
        safe_box: Optional[bool] = None,
        padding: PaddingDimensions = (0, 1),
        collapse_padding: bool = False,
        pad_edge: bool = True,
        expand: bool = False,
        show_header: bool = True,
        show_footer: bool = False,
        show_edge: bool = True,
        show_lines: bool = False,
        leading: int = 0,
        style: StyleType = "none",
        row_styles: Iterable[StyleType] = None,
        header_style: StyleType = None,
        footer_style: StyleType = None,
        border_style: StyleType = None,
        title_style: StyleType = None,
        caption_style: StyleType = None,
    ) -> None:

        self.columns = [
            (Column(index, header) if isinstance(header, str) else header)
            for index, header in enumerate(headers)
        ]
        self.title = title
        self.caption = caption
        self.width = width
        self.box = box
        self.safe_box = safe_box
        self._padding = Padding.unpack(padding)
        self.pad_edge = pad_edge
        self._expand = expand
        self.show_header = show_header
        self.show_footer = show_footer
        self.show_edge = show_edge
        self.show_lines = show_lines
        self.leading = leading
        self.collapse_padding = collapse_padding
        self.style = style
        self.header_style = header_style
        self.footer_style = footer_style
        self.border_style = border_style
        self.title_style = title_style
        self.caption_style = title_style
        self._row_count = 0
        self.row_styles = list(row_styles or [])

    @classmethod
    def grid(
        cls,
        padding: PaddingDimensions = 0,
        collapse_padding: bool = True,
        pad_edge: bool = False,
        expand: bool = False,
    ) -> "Table":
        """Get a table with no lines, headers, or footer.

        Args:
            padding (PaddingDimensions, optional): Get padding around cells. Defaults to 0.
            collapse_padding (bool, optional): Enable collapsing of padding around cells. Defaults to True.
            pad_edge (bool, optional): Enable padding around edges of table. Defaults to False.
            expand (bool, optional): Expand the table to fit the available space if ``True``, otherwise the table width will be auto-calculated. Defaults to False.
        
        Returns:
            Table: A table instance.
        """
        return cls(
            box=None,
            padding=padding,
            collapse_padding=collapse_padding,
            show_header=False,
            show_footer=False,
            show_edge=False,
            pad_edge=pad_edge,
            expand=expand,
        )

    @property
    def expand(self) -> int:
        """Setting a non-None self.width implies expand."""
        return self._expand or self.width is not None

    @expand.setter
    def expand(self, expand: bool) -> None:
        """Set expand."""
        self._expand = expand

    @property
    def _extra_width(self) -> int:
        """Get extra width to add to cell content."""
        width = 0
        if self.box and self.show_edge:
            width += 2
        if self.box:
            width += len(self.columns) - 1
        return width

    @property
    def row_count(self) -> int:
        """Get the current number of rows."""
        return self._row_count

    def get_row_style(self, index: int) -> StyleType:
        """Get the current row style."""
        if self.row_styles:
            return self.row_styles[index % len(self.row_styles)]
        return Style()

    def __rich_measure__(self, console: "Console", max_width: int) -> Measurement:
        if self.width is not None:
            max_width = self.width

        if self.box:
            max_width -= len(self.columns) - 1
            if self.show_edge:
                max_width -= 2

        extra_width = self._extra_width
        _measure_column = self._measure_column

        measurements = [
            _measure_column(console, column, max_width) for column in self.columns
        ]
        minimum_width = (
            sum(measurement.minimum for measurement in measurements) + extra_width
        )
        maximum_width = (
            sum(measurement.maximum for measurement in measurements) + extra_width
            if (self.width is None)
            else self.width
        )
        return Measurement(minimum_width, maximum_width)

    @property
    def padding(self) -> Tuple[int, int, int, int]:
        """Get cell padding."""
        return self._padding

    @padding.setter
    def padding(self, padding: PaddingDimensions) -> "Table":
        """Set cell padding."""
        self._padding = Padding.unpack(padding)
        return self

    def add_column(
        self,
        header: "RenderableType" = "",
        footer: "RenderableType" = "",
        *,
        header_style: StyleType = None,
        footer_style: StyleType = None,
        style: StyleType = None,
        justify: "JustifyMethod" = "left",
        overflow: "OverflowMethod" = "ellipsis",
        width: int = None,
        ratio: int = None,
        no_wrap: bool = False,
    ) -> None:
        """Add a column to the table.
        
        Args:
            header (RenderableType, optional): Text or renderable for the header.
                Defaults to "".
            footer (RenderableType, optional): Text or renderable for the footer.
                Defaults to "".
            header_style (Union[str, Style], optional): Style for the header. Defaults to "none".
            footer_style (Union[str, Style], optional): Style for the header. Defaults to "none".
            style (Union[str, Style], optional): Style for the column cells. Defaults to "none".
            justify (JustifyMethod, optional): Alignment for cells. Defaults to "left".
            width (int, optional): A minimum width in characters. Defaults to None.
            ratio (int, optional): Flexible ratio for the column (requires ``Table.expand`` or ``Table.width``). Defaults to None.
            no_wrap (bool, optional): Set to ``True`` to disable wrapping of this column.
        """

        column = Column(
            index=len(self.columns),
            header=header,
            footer=footer,
            header_style=Style.pick_first(
                header_style, self.header_style, "table.header"
            ),
            footer_style=Style.pick_first(
                footer_style, self.footer_style, "table.footer"
            ),
            style=Style.pick_first(style, self.style, "table.cell"),
            justify=justify,
            overflow=overflow,
            width=width,
            ratio=ratio,
            no_wrap=no_wrap,
        )
        self.columns.append(column)

    def add_row(
        self, *renderables: Optional["RenderableType"], style: StyleType = None
    ) -> None:
        """Add a row of renderables.
        
        Args:
            *renderables (None or renderable): Each cell in a row must be a renderable object (including str),
                or ``None`` for a blank cell.
            style (StyleType, optional): An optional style to apply to the entire row. Defaults to None.

        Raises:
            errors.NotRenderableError: If you add something that can't be rendered.
        """

        def add_cell(column: Column, renderable: "RenderableType") -> None:
            column._cells.append(
                renderable if style is None else Styled(renderable, style)
            )

        cell_renderables: List[Optional["RenderableType"]] = list(renderables)

        columns = self.columns
        if len(cell_renderables) < len(columns):
            cell_renderables = [
                *cell_renderables,
                *[None] * (len(columns) - len(cell_renderables)),
            ]
        for index, renderable in enumerate(cell_renderables):
            if index == len(columns):
                column = Column(index)
                for _ in range(self._row_count):
                    add_cell(column, Text(""))
                self.columns.append(column)
            else:
                column = columns[index]
            if renderable is None:
                add_cell(column, "")
            elif is_renderable(renderable):
                add_cell(column, renderable)
            else:
                raise errors.NotRenderableError(
                    f"unable to render {type(renderable).__name__}; a string or other renderable object is required"
                )
        self._row_count += 1

    def __rich_console__(
        self, console: "Console", options: "ConsoleOptions"
    ) -> "RenderResult":

        max_width = options.max_width
        if self.width is not None:
            max_width = self.width
        if self.box:
            max_width -= len(self.columns) - 1
            if self.show_edge:
                max_width -= 2
        widths = self._calculate_column_widths(console, max_width)
        table_width = sum(widths) + self._extra_width

        render_options = options.update(width=table_width)

        def render_annotation(text: TextType, style: StyleType) -> "RenderResult":
            render_text = (
                console.render_str(text, style=style) if isinstance(text, str) else text
            )
            return console.render(
                render_text, options=render_options.update(justify="center")
            )

        if self.title:
            yield from render_annotation(
                self.title, style=Style.pick_first(self.title_style, "table.title")
            )
        yield from self._render(console, render_options, widths)
        if self.caption:
            yield from render_annotation(
                self.caption,
                style=Style.pick_first(self.caption_style, "table.caption"),
            )

    def _calculate_column_widths(self, console: "Console", max_width: int) -> List[int]:
        """Calculate the widths of each column, including padding, not including borders."""
        columns = self.columns
        width_ranges = [
            self._measure_column(console, column, max_width) for column in columns
        ]
        widths = [_range.maximum or 1 for _range in width_ranges]
        get_padding_width = self._get_padding_width

        if self.expand:
            ratios = [col.ratio or 0 for col in columns if col.flexible]
            if any(ratios):
                fixed_widths = [
                    0 if column.flexible else _range.maximum
                    for _range, column in zip(width_ranges, columns)
                ]
                flex_minimum = [
                    (column.width or 1) + get_padding_width(column.index)
                    for column in columns
                    if column.flexible
                ]
                flexible_width = max_width - sum(fixed_widths)
                flex_widths = ratio_distribute(flexible_width, ratios, flex_minimum)
                iter_flex_widths = iter(flex_widths)
                for index, column in enumerate(columns):
                    if column.flexible:
                        widths[index] = fixed_widths[index] + next(iter_flex_widths)
        table_width = sum(widths)

        if table_width > max_width:
            widths = self._collapse_widths(
                widths, [not column.no_wrap for column in columns], max_width
            )
            table_width = sum(widths)

            # last resort, reduce columns evenly
            if table_width > max_width:
                excess_width = table_width - max_width
                widths = ratio_reduce(excess_width, [1] * len(widths), widths, widths)
                table_width = sum(widths)

            width_ranges = [
                self._measure_column(console, column, width)
                for width, column in zip(widths, columns)
            ]
            widths = [_range.maximum or 1 for _range in width_ranges]

        if table_width < max_width and self.expand:
            pad_widths = ratio_distribute(max_width - table_width, widths)
            widths = [_width + pad for _width, pad in zip(widths, pad_widths)]

        return widths

    @classmethod
    def _collapse_widths(
        cls, widths: List[int], wrapable: List[bool], max_width: int
    ) -> List[int]:
        """Reduce widths so that the total is under max_width.

        Args:
            widths (List[int]): List of widths.
            wrapable (List[bool]): List of booleans that indicate if a column may shrink.
            max_width (int): Maximum width to reduce to.

        Returns:
            List[int]: A new list of widths.
        """
        total_width = sum(widths)
        excess_width = total_width - max_width
        if any(wrapable):
            while total_width and excess_width > 0:
                max_column = max(
                    width for width, allow_wrap in zip(widths, wrapable) if allow_wrap
                )
                try:
                    second_max_column = max(
                        width if allow_wrap and width != max_column else 0
                        for width, allow_wrap in zip(widths, wrapable)
                    )
                except ValueError:
                    second_max_column = 0
                column_difference = max_column - second_max_column
                ratios = [
                    (1 if (width == max_column and allow_wrap) else 0)
                    for width, allow_wrap in zip(widths, wrapable)
                ]
                if not any(ratios) or not column_difference:
                    break
                max_reduce = [min(excess_width, column_difference)] * len(widths)
                widths = ratio_reduce(excess_width, ratios, max_reduce, widths)

                total_width = sum(widths)
                excess_width = total_width - max_width
        return widths

    def _get_cells(self, column_index: int, column: Column) -> Iterable[_Cell]:
        """Get all the cells with padding and optional header."""

        collapse_padding = self.collapse_padding
        pad_edge = self.pad_edge
        padding = self.padding
        any_padding = any(padding)

        first_column = column_index == 0
        last_column = column_index == len(self.columns) - 1

        def add_padding(
            renderable: "RenderableType", first_row: bool, last_row: bool
        ) -> "RenderableType":
            if not any_padding:
                return renderable
            top, right, bottom, left = padding

            if collapse_padding:
                if not first_column:
                    left = max(0, left - right)
                if not last_row:
                    bottom = max(0, top - bottom)

            if not pad_edge:
                if first_column:
                    left = 0
                if last_column:
                    right = 0
                if first_row:
                    top = 0
                if last_row:
                    bottom = 0
            _padding = Padding(renderable, (top, right, bottom, left))
            return _padding

        raw_cells: List[Tuple[StyleType, "RenderableType"]] = []
        _append = raw_cells.append
        if self.show_header:
            _append((column.header_style, column.header))
        for cell in column.cells:
            _append((column.style, cell))
        if self.show_footer:
            _append((column.footer_style, column.footer))
        for first, last, (style, renderable) in loop_first_last(raw_cells):
            yield _Cell(style, add_padding(renderable, first, last))

    def _get_padding_width(self, column_index: int) -> int:
        """Get extra width from padding."""
        _, pad_right, _, pad_left = self.padding
        if self.collapse_padding:
            if column_index > 0:
                pad_left = max(0, pad_left - pad_right)
        return pad_left + pad_right

    def _measure_column(
        self, console: "Console", column: Column, max_width: int
    ) -> Measurement:
        """Get the minimum and maximum width of the column."""

        padding_width = self._get_padding_width(column.index)

        if column.width is not None:
            # Fixed width column
            return Measurement(
                column.width + padding_width, column.width + padding_width
            )
        # Flexible column, we need to measure contents
        min_widths: List[int] = []
        max_widths: List[int] = []
        append_min = min_widths.append
        append_max = max_widths.append
        get_render_width = Measurement.get
        for cell in self._get_cells(column.index, column):
            _min, _max = get_render_width(console, cell.renderable, max_width)
            append_min(_min)
            append_max(_max)

        return Measurement(
            max(min_widths) if min_widths else 1,
            max(max_widths) if max_widths else max_width,
        )

    def _render(
        self, console: "Console", options: "ConsoleOptions", widths: List[int]
    ) -> "RenderResult":
        table_style = console.get_style(self.style or "")

        border_style = table_style + console.get_style(self.border_style or "")
        rows: List[Tuple[_Cell, ...]] = list(
            zip(
                *(
                    self._get_cells(column_index, column)
                    for column_index, column in enumerate(self.columns)
                )
            )
        )
        safe_box: bool = console.safe_box if self.safe_box is None else self.safe_box  # type: ignore
        _box = (
            box.get_safe_box(self.box, console.legacy_windows) if safe_box else self.box
        )

        # _box = self.box
        new_line = Segment.line()

        columns = self.columns
        show_header = self.show_header
        show_footer = self.show_footer
        show_edge = self.show_edge
        show_lines = self.show_lines
        leading = self.leading

        _Segment = Segment
        if _box:
            box_segments = [
                (
                    _Segment(_box.head_left, border_style),
                    _Segment(_box.head_right, border_style),
                    _Segment(_box.head_vertical, border_style),
                ),
                (
                    _Segment(_box.foot_left, border_style),
                    _Segment(_box.foot_right, border_style),
                    _Segment(_box.foot_vertical, border_style),
                ),
                (
                    _Segment(_box.mid_left, border_style),
                    _Segment(_box.mid_right, border_style),
                    _Segment(_box.mid_vertical, border_style),
                ),
            ]
            if show_edge:
                yield _Segment(_box.get_top(widths), border_style)
                yield new_line
        else:
            box_segments = []

        get_row_style = self.get_row_style
        get_style = console.get_style

        for index, (first, last, row) in enumerate(loop_first_last(rows)):
            header_row = first and show_header
            footer_row = last and show_footer
            max_height = 1
            cells: List[List[List[Segment]]] = []
            if header_row or footer_row:
                row_style = Style()
            else:
                row_style = get_style(
                    get_row_style(index - 1 if show_header else index)
                )
            for width, cell, column in zip(widths, row, columns):
                render_options = options.update(
                    width=width,
                    justify=column.justify,
                    no_wrap=column.no_wrap,
                    overflow=column.overflow,
                )
                cell_style = table_style + row_style + get_style(cell.style)
                lines = console.render_lines(
                    cell.renderable, render_options, style=cell_style
                )
                max_height = max(max_height, len(lines))
                cells.append(lines)

            cells[:] = [
                _Segment.set_shape(_cell, width, max_height, style=table_style)
                for width, _cell in zip(widths, cells)
            ]

            if _box:
                if last and show_footer:
                    yield _Segment(
                        _box.get_row(widths, "foot", edge=show_edge), border_style
                    )
                    yield new_line
                if first:
                    left, right, divider = box_segments[0]
                elif last:
                    left, right, divider = box_segments[2]
                else:
                    left, right, divider = box_segments[1]

                for line_no in range(max_height):
                    if show_edge:
                        yield left
                    for last_cell, rendered_cell in loop_last(cells):
                        yield from rendered_cell[line_no]
                        if not last_cell:
                            yield divider
                    if show_edge:
                        yield right
                    yield new_line
            else:
                for line_no in range(max_height):
                    for rendered_cell in cells:
                        yield from rendered_cell[line_no]
                    yield new_line
            if _box and first and show_header:
                yield Segment(
                    _box.get_row(widths, "head", edge=show_edge), border_style
                )
                yield new_line
            if _box and (show_lines or leading):
                if (
                    not last
                    and not (show_footer and index >= len(rows) - 2)
                    and not (show_header and header_row)
                ):
                    if leading:
                        for _ in range(leading):
                            yield _Segment(
                                _box.get_row(widths, "mid", edge=show_edge),
                                border_style,
                            )
                    else:
                        yield _Segment(
                            _box.get_row(widths, "row", edge=show_edge), border_style
                        )
                    yield new_line

        if _box and show_edge:
            yield _Segment(_box.get_bottom(widths), border_style)
            yield new_line


if __name__ == "__main__":  # pragma: no cover
    from .console import Console

    c = Console()
    table = Table(
        show_lines=False,
        row_styles=["red", "green"],
        expand=False,
        show_header=True,
        show_footer=False,
        show_edge=True,
    )
    table.add_column("foo", no_wrap=True, footer="BAR")
    table.add_column("bar")
    table.add_column("baz")
    table.add_row("Magnet", "foo" * 20, "bar" * 10, "egg" * 15)

    for width in range(170, 1, -1):
        print(" " * width + "<|")
        c = Console(width=width)
        c.print(table)

    c.print("Some more words", width=4, overflow="ellipsis")
