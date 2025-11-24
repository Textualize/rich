"""Bar chart renderable for Rich."""

from collections.abc import Mapping, Sequence
from typing import Dict, List, Optional, Tuple, Union

from .bar import END_BLOCK_ELEMENTS, FULL_BLOCK
from .console import Console, ConsoleOptions, RenderResult
from .jupyter import JupyterMixin
from .measure import Measurement
from .segment import Segment
from .style import Style, StyleType

DEFAULT_COLORS = [
    "blue",
    "green",
    "yellow",
    "magenta",
    "cyan",
    "red",
    "bright_blue",
    "bright_green",
]


class BarChart(JupyterMixin):
    """Render a flexible bar chart in the terminal.

    Args:
        data (Union[Dict[str, float], List[Tuple[str, float]], Sequence[float]]):
            Data to display. Can be:
            - Dict mapping labels to values
            - Dict mapping labels to dicts of grouped values
            - List of (label, value) tuples
            - Sequence of values (labels will be auto-generated)
        width (int, optional): Width of the chart, or None for maximum width. Defaults to None.
        max_value (float, optional): Maximum value for scaling. If None, uses max value from data. Defaults to None.
        show_values (bool, optional): Show values on bars (horizontal only). Defaults to True.
        bar_width (int, optional): Width of each bar in characters. Defaults to 1.
        orientation (str, optional): Either ``"horizontal"`` or ``"vertical"``. Defaults to ``"horizontal"``.
        chart_height (int, optional): Height (in rows) of a vertical chart. Defaults to 10 if not given.
        group_labels (Sequence[str], optional): Optional ordering of grouped series labels.
        group_styles (Sequence[StyleType], optional): Styles for grouped series (cycled if fewer than groups).
        group_gap (int, optional): Number of spaces between grouped bars. Defaults to 1.
        style (StyleType, optional): Default style for bars. Defaults to None.
        bar_styles (Sequence[StyleType], optional): Styles for each single bar (cycled). Defaults to None.
        label_style (StyleType, optional): Style for labels. Defaults to None.
        value_style (StyleType, optional): Style for values. Defaults to None.
    """

    def __init__(
        self,
        data: Union["Dict[str, float]", List[Tuple[str, float]], Sequence[float]],
        *,
        width: Optional[int] = None,
        max_value: Optional[float] = None,
        show_values: bool = True,
        bar_width: int = 1,
        orientation: str = "horizontal",
        chart_height: Optional[int] = None,
        group_labels: Optional[Sequence[str]] = None,
        group_styles: Optional[Sequence[StyleType]] = None,
        group_gap: int = 1,
        style: Optional[StyleType] = None,
        bar_styles: Optional[Sequence[StyleType]] = None,
        label_style: Optional[StyleType] = None,
        value_style: Optional[StyleType] = None,
    ):
        items = self._coerce_items(data)
        if not items:
            raise ValueError("Data cannot be empty")

        self.width = width
        self.show_values = show_values
        self.bar_width = max(1, bar_width)
        self.orientation = orientation
        self.chart_height = chart_height
        self.style = style
        self.bar_styles = list(bar_styles) if bar_styles else None
        self.label_style = label_style
        self.value_style = value_style

        self.group_gap = max(0, group_gap)
        self._explicit_group_labels = list(group_labels) if group_labels else None
        self.group_styles = list(group_styles) if group_styles else None

        self.grouped = False
        self.group_labels: List[str] = []
        self.simple_rows: List[Tuple[str, float]] = []
        self.group_rows: List[Tuple[str, List[float]]] = []

        self._normalize_items(items)
        self._set_max_value(max_value)

    # --------------------------------------------------------------------- #
    # Initialization helpers
    # --------------------------------------------------------------------- #

    def _coerce_items(
        self,
        data: Union["Dict[str, float]", List[Tuple[str, float]], Sequence[float]],
    ) -> List[Tuple[Union[str, int], Union[float, Mapping[str, float]]]]:
        if isinstance(data, Mapping):
            return list(data.items())
        if isinstance(data, Sequence):
            if not data:
                return []
            first = data[0]
            if isinstance(first, tuple) and len(first) == 2:
                return list(data)  # type: ignore[list-item]
            return [(index, value) for index, value in enumerate(data)]
        raise TypeError("BarChart data must be a mapping or sequence")

    def _normalize_items(
        self,
        items: List[Tuple[Union[str, int], Union[float, Mapping[str, float]]]],
    ) -> None:
        first_value = items[0][1]
        if isinstance(first_value, Mapping):
            self.grouped = True
            self._normalize_grouped_items(items)  # type: ignore[arg-type]
        else:
            self.simple_rows = [
                (str(label), float(value)) for label, value in items  # type: ignore[arg-type]
            ]

    def _normalize_grouped_items(
        self,
        items: List[Tuple[Union[str, int], Mapping[str, float]]],
    ) -> None:
        groups: List[str] = []
        seen = set()
        if self._explicit_group_labels:
            groups.extend(str(name) for name in self._explicit_group_labels)
            seen.update(groups)

        normalized_rows: List[Tuple[str, Dict[str, float]]] = []
        for label, mapping in items:
            label_str = str(label)
            row_dict: Dict[str, float] = {}
            for key, value in mapping.items():
                key_str = str(key)
                row_dict[key_str] = float(value)
                if not self._explicit_group_labels and key_str not in seen:
                    groups.append(key_str)
                    seen.add(key_str)
            normalized_rows.append((label_str, row_dict))

        if not groups:
            raise ValueError("Grouped data requires at least one series")

        self.group_labels = groups
        for label, mapping in normalized_rows:
            row_values = [mapping.get(group, 0.0) for group in self.group_labels]
            self.group_rows.append((label, row_values))

    def _set_max_value(self, max_value: Optional[float]) -> None:
        values: List[float]
        if self.grouped:
            values = [
                value
                for _, row in self.group_rows
                for value in row
            ]
        else:
            values = [value for _, value in self.simple_rows]

        if not values:
            values = [0.0]

        computed_max = max(values)
        if computed_max <= 0:
            computed_max = 1.0

        self.max_value = max_value if max_value is not None else computed_max
        if self.max_value <= 0:
            self.max_value = 1.0

    # --------------------------------------------------------------------- #
    # Rendering helpers
    # --------------------------------------------------------------------- #

    def _get_label_style(self) -> Optional[Style]:
        return Style.parse(str(self.label_style)) if self.label_style else None

    def _get_value_style(self) -> Optional[Style]:
        return Style.parse(str(self.value_style)) if self.value_style else None

    def _get_bar_style(self, index: int) -> Style:
        if self.bar_styles:
            raw_style = self.bar_styles[index % len(self.bar_styles)]
        elif self.style:
            raw_style = self.style
        else:
            raw_style = DEFAULT_COLORS[index % len(DEFAULT_COLORS)]
        return Style.parse(str(raw_style))

    def _get_group_style(self, index: int) -> Style:
        if self.group_styles:
            raw_style = self.group_styles[index % len(self.group_styles)]
        elif self.bar_styles:
            raw_style = self.bar_styles[index % len(self.bar_styles)]
        elif self.style:
            raw_style = self.style
        else:
            raw_style = DEFAULT_COLORS[index % len(DEFAULT_COLORS)]
        return Style.parse(str(raw_style))

    def _bar_length(self, value: float, bar_area_width: int) -> int:
        if self.max_value <= 0:
            return 0
        return int((value / self.max_value) * bar_area_width)

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        if self.orientation == "vertical":
            yield from self._render_vertical(console, options)
        else:
            yield from self._render_horizontal(console, options)

    # ------------------------------------------------------------------ #
    # Horizontal rendering
    # ------------------------------------------------------------------ #

    def _render_horizontal(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        if self.grouped:
            yield from self._render_horizontal_grouped(console, options)
            return

        available_width = min(
            self.width if self.width is not None else options.max_width,
            options.max_width,
        )

        max_label_len = max(len(label) for label, _ in self.simple_rows)
        label_width = max_label_len + 2

        bar_area_width = available_width - label_width
        if self.show_values:
            bar_area_width -= 12
        if bar_area_width < 1:
            bar_area_width = 1

        label_style = self._get_label_style()
        value_style = self._get_value_style()

        for idx, (label, value) in enumerate(self.simple_rows):
            bar_style = self._get_bar_style(idx)
            bar_length = self._bar_length(value, bar_area_width)
            bar_text = self._make_horizontal_bar(bar_length)
            value_text = ""
            if self.show_values:
                value_text = f" {value:.2f}"

            label_padding = " " * (label_width - len(label) - 1)
            line_segments: List[Segment] = [
                Segment(label_padding),
                Segment(label, label_style),
                Segment(" "),
                Segment(bar_text, bar_style),
            ]
            if value_text:
                line_segments.append(Segment(value_text, value_style))
            line_segments.append(Segment.line())
            yield from line_segments

    def _render_horizontal_grouped(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        available_width = min(
            self.width if self.width is not None else options.max_width,
            options.max_width,
        )

        max_category_len = max(len(label) for label, _ in self.group_rows)
        label_width = max_category_len + 1
        max_group_len = max(len(name) for name in self.group_labels)
        group_width = max_group_len + 1

        bar_area_width = available_width - label_width - group_width - 2
        if self.show_values:
            bar_area_width -= 12
        if bar_area_width < 1:
            bar_area_width = 1

        label_style = self._get_label_style()
        value_style = self._get_value_style()

        for label, values in self.group_rows:
            for group_index, value in enumerate(values):
                bar_length = self._bar_length(value, bar_area_width)
                bar_style = self._get_group_style(group_index)

                category_column = label if group_index == 0 else ""
                category_column = category_column.ljust(label_width)
                group_name = self.group_labels[group_index]
                group_column = group_name.ljust(group_width)

                line_segments: List[Segment] = [
                    Segment(category_column, label_style if category_column.strip() else None),
                    Segment(" "),
                    Segment(group_column, label_style),
                    Segment(" "),
                    Segment(self._make_horizontal_bar(bar_length), bar_style),
                ]
                if self.show_values:
                    line_segments.append(Segment(f" {value:.2f}", value_style))
                line_segments.append(Segment.line())
                yield from line_segments

            # Blank line between categories for readability
            yield Segment.line()

        yield from self._render_group_legend()

    def _make_horizontal_bar(self, bar_length: int) -> str:
        full_blocks = bar_length // self.bar_width
        remainder = bar_length % self.bar_width
        bar_chars = FULL_BLOCK * full_blocks
        if remainder > 0 and remainder < len(END_BLOCK_ELEMENTS):
            bar_chars += END_BLOCK_ELEMENTS[remainder]
        return bar_chars or ""

    # ------------------------------------------------------------------ #
    # Vertical rendering
    # ------------------------------------------------------------------ #

    def _render_vertical(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        if self.grouped:
            yield from self._render_vertical_grouped(console, options)
            return

        chart_height = self._get_chart_height(options)
        label_style = self._get_label_style()

        bar_heights = [
            self._bar_length(value, chart_height) for _, value in self.simple_rows
        ]
        bar_styles = [self._get_bar_style(idx) for idx in range(len(bar_heights))]

        gap = 1
        for row in range(chart_height, 0, -1):
            segments: List[Segment] = []
            for idx, height in enumerate(bar_heights):
                if height >= row:
                    segments.append(Segment(FULL_BLOCK * self.bar_width, bar_styles[idx]))
                else:
                    segments.append(Segment(" " * self.bar_width))
                if idx != len(bar_heights) - 1:
                    segments.append(Segment(" " * gap))
            segments.append(Segment.line())
            yield from segments

        label_segments: List[Segment] = []
        for idx, (label, _value) in enumerate(self.simple_rows):
            label_str = self._fit_label(label)
            label_segments.append(Segment(label_str, label_style))
            if idx != len(self.simple_rows) - 1:
                label_segments.append(Segment(" " * gap))
        label_segments.append(Segment.line())
        yield from label_segments

    def _render_vertical_grouped(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        chart_height = self._get_chart_height(options)
        label_style = self._get_label_style()

        group_count = len(self.group_labels)
        group_gap = self.group_gap
        category_gap = group_gap + 1

        heights: List[List[int]] = []
        for label, values in self.group_rows:
            heights.append(
                [self._bar_length(value, chart_height) for value in values]
            )

        for row in range(chart_height, 0, -1):
            segments: List[Segment] = []
            for cat_idx, category_heights in enumerate(heights):
                for group_index, bar_height in enumerate(category_heights):
                    if bar_height >= row:
                        style = self._get_group_style(group_index)
                        segments.append(Segment(FULL_BLOCK * self.bar_width, style))
                    else:
                        segments.append(Segment(" " * self.bar_width))
                    if group_index != group_count - 1:
                        segments.append(Segment(" " * group_gap))
                if cat_idx != len(heights) - 1:
                    segments.append(Segment(" " * category_gap))
            segments.append(Segment.line())
            yield from segments

        category_width = group_count * self.bar_width + (group_count - 1) * group_gap
        label_segments: List[Segment] = []
        for cat_idx, (label, _values) in enumerate(self.group_rows):
            label_text = self._center_text(label, category_width)
            label_segments.append(Segment(label_text, label_style))
            if cat_idx != len(self.group_rows) - 1:
                label_segments.append(Segment(" " * category_gap))
        label_segments.append(Segment.line())
        yield from label_segments

        yield from self._render_group_legend()

    def _render_group_legend(self) -> RenderResult:
        if not self.grouped or not self.group_labels:
            return
        segments: List[Segment] = []
        for idx, group in enumerate(self.group_labels):
            style = self._get_group_style(idx)
            segments.append(Segment(FULL_BLOCK * self.bar_width, style))
            segments.append(Segment(f" {group}  "))
        segments.append(Segment.line())
        yield from segments

    # ------------------------------------------------------------------ #
    # Utilities
    # ------------------------------------------------------------------ #

    def _get_chart_height(self, options: ConsoleOptions) -> int:
        default_height = 10
        max_height = options.height if options.height is not None else options.size.height
        chart_height = self.chart_height or min(default_height, max_height)
        return max(1, chart_height)

    def _fit_label(self, label: str) -> str:
        if len(label) > self.bar_width:
            return label[: self.bar_width]
        return label.ljust(self.bar_width)

    def _center_text(self, text: str, width: int) -> str:
        if width <= len(text):
            return text[:width]
        padding = width - len(text)
        left = padding // 2
        right = padding - left
        return f"{' ' * left}{text}{' ' * right}"

    def __rich_measure__(
        self, console: Console, options: ConsoleOptions
    ) -> Measurement:
        if self.width is not None:
            return Measurement(self.width, self.width)
        return Measurement(20, options.max_width)

 