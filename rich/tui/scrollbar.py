from typing import List, Optional

from rich.segment import Segment
from rich.style import Style


def render_bar(
    height: int = 25,
    size: float = 100,
    window_size: float = 25,
    position: float = 0,
    bar_style: Optional[Style] = None,
    back_style: Optional[Style] = None,
    ascii_only: bool = False,
    vertical: bool = True,
) -> List[Segment]:
    if vertical:
        if ascii_only:
            solid = "|"
            half_start = "|"
            half_end = "|"
        else:
            solid = "┃"
            half_start = "╻"
            half_end = "╹"
    else:
        if ascii_only:
            solid = "-"
            half_start = "-"
            half_end = "-"
        else:
            solid = "━"
            half_start = "╺"
            half_end = "╸"

    _bar_style = bar_style or Style.parse("bright_magenta")
    _back_style = back_style or Style.parse("#555555")

    _Segment = Segment

    start_bar_segment = _Segment(half_start, _bar_style)
    end_bar_segment = _Segment(half_end, _bar_style)
    bar_segment = _Segment(solid, _bar_style)

    start_back_segment = _Segment(half_end, _back_style)
    end_back_segment = _Segment(half_end, _back_style)
    back_segment = _Segment(solid, _back_style)

    segments = [back_segment] * height

    step_size = size / height

    start = position / step_size
    end = (position + window_size) / step_size

    start_index = int(start)
    end_index = int(end)
    bar_height = (end_index - start_index) + 1

    segments[start_index:end_index] = [bar_segment] * bar_height

    sub_position = start % 1.0
    if sub_position >= 0.5:
        segments[start_index] = start_bar_segment
    elif start_index:
        segments[start_index - 1] = end_back_segment

    sub_position = end % 1.0
    if sub_position < 0.5:
        segments[end_index] = end_bar_segment
    elif end_index + 1 < len(segments):
        segments[end_index + 1] = start_back_segment

    return segments


if __name__ == "__main__":
    from rich.console import Console
    from rich.segment import Segments

    console = Console()

    bar = render_bar(height=20, position=10, vertical=False, ascii_only=False)

    console.print(Segments(bar, new_lines=False))
