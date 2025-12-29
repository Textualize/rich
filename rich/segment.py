from enum import IntEnum
from functools import lru_cache
from itertools import filterfalse
from logging import getLogger
from operator import attrgetter
from typing import (
    TYPE_CHECKING,
    Dict,
    Iterable,
    List,
    NamedTuple,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
)

# [导入分析]
# - `IntEnum`: 用于定义控制码的类型枚举。
# - `lru_cache`: 用于缓存计算结果，提高性能（如 _split_cells）。
# - `filterfalse`: 用于过滤非控制码的 Segment。
# - `getLogger`: 记录日志。
# - `attrgetter`: 用于快速获取对象属性（如 is_control）。
# - `typing`: 标准类型提示模块。
from .cells import (
    _is_single_cell_widths,
    cached_cell_len,
    cell_len,
    get_character_cell_size,
    set_cell_size,
)
# [导入分析]
# - `cells`: 处理字符单元格宽度（如全角字符）的模块。
from .repr import Result, rich_repr
# [导入分析]
# - `repr`: 用于实现 `__rich_repr__` 方法，支持 `rich.print` 的自定义表示。
from .style import Style
# [导入分析]
# - `style`: 样式对象。

if TYPE_CHECKING:
    from .console import Console, ConsoleOptions, RenderResult
# [导入分析]
# - `TYPE_CHECKING`: 在类型检查时导入，避免运行时依赖。

log = getLogger("rich")


class ControlType(IntEnum):
    """[枚举：控制码类型]
    
    定义了非打印的控制码，这些通常对应 ANSI 转义序列。
    例如：响铃 (BELL)、清屏 (CLEAR)、移动光标 (CURSOR_MOVE_TO) 等。
    """
    BELL = 1
    CARRIAGE_RETURN = 2
    HOME = 3
    CLEAR = 4
    SHOW_CURSOR = 5
    HIDE_CURSOR = 6
    ENABLE_ALT_SCREEN = 7
    DISABLE_ALT_SCREEN = 8
    CURSOR_UP = 9
    CURSOR_DOWN = 10
    CURSOR_FORWARD = 11
    CURSOR_BACKWARD = 12
    CURSOR_MOVE_TO_COLUMN = 13
    CURSOR_MOVE_TO = 14
    ERASE_IN_LINE = 15
    SET_WINDOW_TITLE = 16


ControlCode = Union[
    Tuple[ControlType],
    Tuple[ControlType, Union[int, str]],
    Tuple[ControlType, int, int],
]
# [类型别名]
# 定义了控制码的多种可能形式：
# 1. (ControlType,)
# 2. (ControlType, int) 或 (ControlType, str)
# 3. (ControlType, int, int)


@rich_repr()
class Segment(NamedTuple):
    """[核心数据结构：文本片段]
    
    Rich 中最基本的数据单元。它封装了文本、样式和可能的控制码。
    所有渲染操作最终都会生成一个 Segment 流，然后由 Console 转换为终端可识别的字符串。
    
    Args:
        text (str): 文本内容。
        style (Style, optional): 应用于文本的样式。
        control (Sequence[ControlCode], optional): 控制码序列。
    """

    text: str
    style: Optional[Style] = None
    control: Optional[Sequence[ControlCode]] = None

    @property
    def cell_length(self) -> int:
        """[属性：单元格长度]
        
        计算文本在终端中占用的字符单元格数。
        对于控制码，长度为 0。
        """
        text, _style, control = self
        return 0 if control else cell_len(text)

    def __rich_repr__(self) -> Result:
        """[协议：富表示]
        
        定义了如何被 `rich.print` 渲染。
        """
        yield self.text
        if self.control is None:
            if self.style is not None:
                yield self.style
        else:
            yield self.style
            yield self.control

    def __bool__(self) -> bool:
        """[布尔值转换]
        
        判断 Segment 是否包含文本内容。
        """
        return bool(self.text)

    @property
    def is_control(self) -> bool:
        """[属性：是否为控制码]
        
        判断 Segment 是否包含控制码。
        """
        return self.control is not None

    @classmethod
    @lru_cache(1024 * 16)
    def _split_cells(cls, segment: "Segment", cut: int) -> Tuple["Segment", "Segment"]:
        """[核心算法：单元格分割]
        
        在指定的单元格位置分割 Segment。
        处理了全角字符（2单元格宽）的复杂情况，确保分割后宽度正确。
        
        Args:
            segment (Segment): 要分割的 Segment。
            cut (int): 分割点（单元格位置）。
            
        Returns:
            Tuple[Segment, Segment]: 分割后的两个 Segment。
        """
        text, style, control = segment
        _Segment = Segment
        cell_length = segment.cell_length
        if cut >= cell_length:
            return segment, _Segment("", style, control)

        cell_size = get_character_cell_size

        pos = int((cut / cell_length) * len(text))

        while True:
            before = text[:pos]
            cell_pos = cell_len(before)
            out_by = cell_pos - cut
            if not out_by:
                return (
                    _Segment(before, style, control),
                    _Segment(text[pos:], style, control),
                )
            if out_by == -1 and cell_size(text[pos]) == 2:
                return (
                    _Segment(text[:pos] + " ", style, control),
                    _Segment(" " + text[pos + 1 :], style, control),
                )
            if out_by == +1 and cell_size(text[pos - 1]) == 2:
                return (
                    _Segment(text[: pos - 1] + " ", style, control),
                    _Segment(" " + text[pos:], style, control),
                )
            if cell_pos < cut:
                pos += 1
            else:
                pos -= 1

    def split_cells(self, cut: int) -> Tuple["Segment", "Segment"]:
        """[方法：分割单元格]
        
        在指定位置分割 Segment。
        如果分割点在双宽字符中间，会用两个空格替换，保持总宽度。
        
        Args:
            cut (int): 分割点。
            
        Returns:
            Tuple[Segment, Segment]: 分割后的两个 Segment。
        """
        text, style, control = self
        assert cut >= 0

        if _is_single_cell_widths(text):
            # [优化：快速路径]
            # 如果文本中所有字符都是单宽，直接按字符索引分割。
            if cut >= len(text):
                return self, Segment("", style, control)
            return (
                Segment(text[:cut], style, control),
                Segment(text[cut:], style, control),
            )

        return self._split_cells(self, cut)

    @classmethod
    def line(cls) -> "Segment":
        """[工厂方法：新行片段]
        
        创建一个表示换行符的 Segment。
        """
        return cls("\n")

    @classmethod
    def apply_style(
        cls,
        segments: Iterable["Segment"],
        style: Optional[Style] = None,
        post_style: Optional[Style] = None,
    ) -> Iterable["Segment"]:
        """[工具方法：应用样式]
        
        将样式应用到 Segment 流。
        样式是叠加的：`style + segment.style + post_style`。
        
        Args:
            segments (Iterable[Segment]): 要处理的 Segment 流。
            style (Style, optional): 基础样式。
            post_style (Style, optional): 叠加在 segment.style 之上的样式。
            
        Returns:
            Iterable[Segment]: 处理后的 Segment 流。
        """
        result_segments = segments
        if style:
            apply = style.__add__
            result_segments = (
                cls(text, None if control else apply(_style), control)
                for text, _style, control in result_segments
            )
        if post_style:
            result_segments = (
                cls(
                    text,
                    (
                        None
                        if control
                        else (_style + post_style if _style else post_style)
                    ),
                    control,
                )
                for text, _style, control in result_segments
            )
        return result_segments

    @classmethod
    def filter_control(
        cls, segments: Iterable["Segment"], is_control: bool = False
    ) -> Iterable["Segment"]:
        """[工具方法：过滤控制码]
        
        根据是否包含控制码来过滤 Segment。
        
        Args:
            segments (Iterable[Segment]): 要过滤的 Segment 流。
            is_control (bool, optional): True 过滤出控制码，False 过滤出非控制码。
            
        Returns:
            Iterable[Segment]: 过滤后的 Segment 流。
        """
        if is_control:
            return filter(attrgetter("control"), segments)
        else:
            return filterfalse(attrgetter("control"), segments)

    @classmethod
    def split_lines(cls, segments: Iterable["Segment"]) -> Iterable[List["Segment"]]:
        """[工具方法：分割行]
        
        将包含换行符的 Segment 流分割成多行。
        
        Args:
            segments (Iterable[Segment]): 可能包含换行符的 Segment 流。
            
        Yields:
            Iterable[List[Segment]]: 每一行的 Segment 列表。
        """
        line: List[Segment] = []
        append = line.append

        for segment in segments:
            if "\n" in segment.text and not segment.control:
                text, style, _ = segment
                while text:
                    _text, new_line, text = text.partition("\n")
                    if _text:
                        append(cls(_text, style))
                    if new_line:
                        yield line
                        line = []
                        append = line.append
            else:
                append(segment)
        if line:
            yield line

    @classmethod
    def split_and_crop_lines(
        cls,
        segments: Iterable["Segment"],
        length: int,
        style: Optional[Style] = None,
        pad: bool = True,
        include_new_lines: bool = True,
    ) -> Iterable[List["Segment"]]:
        """[工具方法：分割并裁剪行]
        
        将 Segment 流分割成行，并裁剪超出指定长度的行。
        
        Args:
            segments (Iterable[Segment]): 要处理的 Segment 流。
            length (int): 目标行长度。
            style (Style, optional): 填充用的样式。
            pad (bool): 是否用空格填充短行。
            
        Returns:
            Iterable[List[Segment]]: 处理后的行列表。
        """
        line: List[Segment] = []
        append = line.append

        adjust_line_length = cls.adjust_line_length
        new_line_segment = cls("\n")

        for segment in segments:
            if "\n" in segment.text and not segment.control:
                text, segment_style, _ = segment
                while text:
                    _text, new_line, text = text.partition("\n")
                    if _text:
                        append(cls(_text, segment_style))
                    if new_line:
                        cropped_line = adjust_line_length(
                            line, length, style=style, pad=pad
                        )
                        if include_new_lines:
                            cropped_line.append(new_line_segment)
                        yield cropped_line
                        line.clear()
            else:
                append(segment)
        if line:
            yield adjust_line_length(line, length, style=style, pad=pad)

    @classmethod
    def adjust_line_length(
        cls,
        line: List["Segment"],
        length: int,
        style: Optional[Style] = None,
        pad: bool = True,
    ) -> List["Segment"]:
        """[工具方法：调整行长度]
        
        裁剪超出长度的行，或用空格填充不足的行。
        
        Args:
            line (List[Segment]): 单行 Segment 列表。
            length (int): 目标长度。
            style (Style, optional): 填充用的样式。
            pad (bool): 是否填充。
            
        Returns:
            List[Segment]: 调整后的行。
        """
        line_length = sum(segment.cell_length for segment in line)
        new_line: List[Segment]

        if line_length < length:
            if pad:
                new_line = line + [cls(" " * (length - line_length), style)]
            else:
                new_line = line[:]
        elif line_length > length:
            new_line = []
            append = new_line.append
            line_length = 0
            for segment in line:
                segment_length = segment.cell_length
                if line_length + segment_length < length or segment.control:
                    append(segment)
                    line_length += segment_length
                else:
                    text, segment_style, _ = segment
                    text = set_cell_size(text, length - line_length)
                    append(cls(text, segment_style))
                    break
        else:
            new_line = line[:]
        return new_line

    @classmethod
    def get_line_length(cls, line: List["Segment"]) -> int:
        """[工具方法：获取行长度]
        
        计算一行 Segment 的总单元格长度（不含控制码）。
        
        Args:
            line (List[Segment]): 单行 Segment 列表。
            
        Returns:
            int: 总长度。
        """
        _cell_len = cell_len
        return sum(_cell_len(text) for text, style, control in line if not control)

    @classmethod
    def get_shape(cls, lines: List[List["Segment"]]) -> Tuple[int, int]:
        """[工具方法：获取形状]
        
        计算一个 Segment 二维列表（多行）的包围矩形尺寸（宽度和高度）。
        
        Args:
            lines (List[List[Segment]]): 多行 Segment 列表。
            
        Returns:
            Tuple[int, int]: (宽度, 高度)。
        """
        get_line_length = cls.get_line_length
        max_width = max(get_line_length(line) for line in lines) if lines else 0
        return (max_width, len(lines))

    @classmethod
    def set_shape(
        cls,
        lines: List[List["Segment"]],
        width: int,
        height: Optional[int] = None,
        style: Optional[Style] = None,
        new_lines: bool = False,
    ) -> List[List["Segment"]]:
        """[工具方法：设置形状]
        
        将一个 Segment 二维列表调整为指定的宽度和高度。
        
        Args:
            lines (List[List[Segment]]): 多行 Segment 列表。
            width (int): 目标宽度。
            height (int, optional): 目标高度，None 表示不改变。
            style (Style, optional): 填充用的样式。
            new_lines (bool): 填充行是否包含换行符。
            
        Returns:
            List[List[Segment]]: 调整后的 Segment 二维列表。
        """
        _height = height or len(lines)

        blank = (
            [cls(" " * width + "\n", style)] if new_lines else [cls(" " * width, style)]
        )

        adjust_line_length = cls.adjust_line_length
        shaped_lines = lines[:_height]
        shaped_lines[:] = [
            adjust_line_length(line, width, style=style) for line in lines
        ]
        if len(shaped_lines) < _height:
            shaped_lines.extend([blank] * (_height - len(shaped_lines)))
        return shaped_lines

    @classmethod
    def align_top(
        cls: Type["Segment"],
        lines: List[List["Segment"]],
        width: int,
        height: int,
        style: Style,
        new_lines: bool = False,
    ) -> List[List["Segment"]]:
        """[布局工具：顶部对齐]
        
        将多行 Segment 列表在指定高度内顶部对齐。
        如果行数不足，在底部填充空白行。
        
        Args:
            lines (List[List[Segment]]): 要对齐的多行 Segment 列表。
            width (int): 填充行的宽度。
            height (int): 目标高度。
            style (Style): 填充行的样式。
            new_lines (bool): 填充行是否包含换行符。
            
        Returns:
            List[List["Segment"]]: 对齐后的 Segment 二维列表。
        """
        extra_lines = height - len(lines)
        if not extra_lines:
            return lines[:]
        lines = lines[:height]
        blank = cls(" " * width + "\n", style) if new_lines else cls(" " * width, style)
        lines = lines + [[blank]] * extra_lines
        return lines

    @classmethod
    def align_bottom(
        cls: Type["Segment"],
        lines: List[List["Segment"]],
        width: int,
        height: int,
        style: Style,
        new_lines: bool = False,
    ) -> List[List["Segment"]]:
        """[布局工具：底部对齐]
        
        将多行 Segment 列表在指定高度内底部对齐。
        如果行数不足，在顶部填充空白行。
        
        Args:
            lines (List[List["Segment"]]): 要对齐的多行 Segment 列表。
            width (int): 填充行的宽度。
            height (int): 目标高度。
            style (Style): 填充行的样式。
            new_lines (bool): 填充行是否包含换行符。
            
        Returns:
            List[List["Segment"]]: 对齐后的 Segment 二维列表。
        """
        extra_lines = height - len(lines)
        if not extra_lines:
            return lines[:]
        lines = lines[:height]
        blank = cls(" " * width + "\n", style) if new_lines else cls(" " * width, style)
        lines = [[blank]] * extra_lines + lines
        return lines

    @classmethod
    def align_middle(
        cls: Type["Segment"],
        lines: List[List["Segment"]],
        width: int,
        height: int,
        style: Style,
        new_lines: bool = False,
    ) -> List[List["Segment"]]:
        """[布局工具：居中对齐]
        
        将多行 Segment 列表在指定高度内居中对齐。
        如果行数不足，在顶部和底部平均填充空白行。
        
        Args:
            lines (List[List["Segment"]]): 要对齐的多行 Segment 列表。
            width (int): 填充行的宽度。
            height (int): 目标高度。
            style (Style): 填充行的样式。
            new_lines (bool): 填充行是否包含换行符。
            
        Returns:
            List[List["Segment"]]: 对齐后的 Segment 二维列表。
        """
        extra_lines = height - len(lines)
        if not extra_lines:
            return lines[:]
        lines = lines[:height]
        blank = cls(" " * width + "\n", style) if new_lines else cls(" " * width, style)
        top_lines = extra_lines // 2
        bottom_lines = extra_lines - top_lines
        lines = [[blank]] * top_lines + lines + [[blank]] * bottom_lines
        return lines

    @classmethod
    def simplify(cls, segments: Iterable["Segment"]) -> Iterable["Segment"]:
        """[优化工具：简化 Segment 流]
        
        合并连续且样式相同的 Segment。
        这可以减少 Segment 的数量，提高渲染效率。
        
        Args:
            segments (Iterable["Segment"]): 要简化的 Segment 流。
            
        Returns:
            Iterable["Segment"]: 简化后的 Segment 流。
        """
        iter_segments = iter(segments)
        try:
            last_segment = next(iter_segments)
        except StopIteration:
            return

        _Segment = Segment
        for segment in iter_segments:
            if last_segment.style == segment.style and not segment.control:
                last_segment = _Segment(
                    last_segment.text + segment.text, last_segment.style
                )
            else:
                yield last_segment
                last_segment = segment
        yield last_segment

    @classmethod
    def strip_links(cls, segments: Iterable["Segment"]) -> Iterable["Segment"]:
        """[过滤工具：移除链接]
        
        从 Segment 流中移除所有链接（URL）。
        
        Args:
            segments (Iterable["Segment"]): 要处理的 Segment 流。
            
        Yields:
            "Segment": 移除链接后的 Segment。
        """
        for segment in segments:
            if segment.control or segment.style is None:
                yield segment
            else:
                text, style, _control = segment
                yield cls(text, style.update_link(None) if style else None)

    @classmethod
    def strip_styles(cls, segments: Iterable["Segment"]) -> Iterable["Segment"]:
        """[过滤工具：移除样式]
        
        从 Segment 流中移除所有样式信息。
        
        Args:
            segments (Iterable["Segment"]): 要处理的 Segment 流。
            
        Yields:
            "Segment": 样式为 None 的 Segment。
        """
        for text, _style, control in segments:
            yield cls(text, None, control)

    @classmethod
    def remove_color(cls, segments: Iterable["Segment"]) -> Iterable["Segment"]:
        """[过滤工具：移除颜色]
        
        从 Segment 流中移除所有颜色信息，但保留其他样式（如粗体、下划线）。
        
        Args:
            segments (Iterable["Segment"]): 要处理的 Segment 流。
            
        Yields:
            "Segment": 无颜色的 Segment。
        """

        cache: Dict[Style, Style] = {}
        for text, style, control in segments:
            if style:
                colorless_style = cache.get(style)
                if colorless_style is None:
                    colorless_style = style.without_color
                    cache[style] = colorless_style
                yield cls(text, colorless_style, control)
            else:
                yield cls(text, None, control)

    @classmethod
    def divide(
        cls, segments: Iterable["Segment"], cuts: Iterable[int]
    ) -> Iterable[List["Segment"]]:
        """[分割工具：按位置分割]
        
        在指定的单元格位置分割 Segment 流，返回多个 Segment 列表。
        
        Args:
            segments (Iterable["Segment"]): 要分割的 Segment 流。
            cuts (Iterable[int]): 分割点列表。
            
        Yields:
            Iterable[List["Segment"]]: 分割后的 Segment 列表。
        """
        split_segments: List["Segment"] = []
        add_segment = split_segments.append

        iter_cuts = iter(cuts)

        while True:
            cut = next(iter_cuts, -1)
            if cut == -1:
                return
            if cut != 0:
                break
            yield []
        pos = 0

        segments_clear = split_segments.clear
        segments_copy = split_segments.copy

        _cell_len = cached_cell_len
        for segment in segments:
            text, _style, control = segment
            while text:
                end_pos = pos if control else pos + _cell_len(text)
                if end_pos < cut:
                    add_segment(segment)
                    pos = end_pos
                    break

                if end_pos == cut:
                    add_segment(segment)
                    yield segments_copy()
                    segments_clear()
                    pos = end_pos

                    cut = next(iter_cuts, -1)
                    if cut == -1:
                        if split_segments:
                            yield segments_copy()
                        return

                    break

                else:
                    before, segment = segment.split_cells(cut - pos)
                    text, _style, control = segment
                    add_segment(before)
                    yield segments_copy()
                    segments_clear()
                    pos = cut

                cut = next(iter_cuts, -1)
                if cut == -1:
                    if split_segments:
                        yield segments_copy()
                    return

        yield segments_copy()


class Segments:
    """[简单渲染器：Segment 流包装器]
    
    一个简单的渲染器，用于在 `__rich_console__` 方法之外打印 Segment 流。
    它将一个 Segment 流包装成一个可渲染对象。
    """

    def __init__(self, segments: Iterable[Segment], new_lines: bool = False) -> None:
        self.segments = list(segments)
        self.new_lines = new_lines

    def __rich_console__(
        self, console: "Console", options: "ConsoleOptions"
    ) -> "RenderResult":
        if self.new_lines:
            line = Segment.line()
            for segment in self.segments:
                yield segment
                yield line
        else:
            yield from self.segments


class SegmentLines:
    """[简单渲染器：多行 Segment 包装器]
    
    一个简单的渲染器，用于处理多行 Segment 列表。
    它将一个二维的 Segment 列表（多行）包装成一个可渲染对象。
    这在渲染过程中可能作为中间步骤使用。
    """

    def __init__(self, lines: Iterable[List[Segment]], new_lines: bool = False) -> None:
        """[构造函数]
        
        Args:
            lines (Iterable[List[Segment]]): 多行 Segment 列表。
            new_lines (bool, optional): 是否在每行后插入换行符。Defaults to False.
        """
        self.lines = list(lines)
        self.new_lines = new_lines

    def __rich_console__(
        self, console: "Console", options: "ConsoleOptions"
    ) -> "RenderResult":
        """[渲染协议：核心方法]
        
        当 `rich.print` 或 `console.print` 遇到这个对象时，会调用此方法。
        
        Args:
            console (Console): 当前的 Console 实例。
            options (ConsoleOptions): 渲染选项。
            
        Yields:
            RenderResult: 生成的 Segment 流。
        """
        if self.new_lines:
            new_line = Segment.line()
            for line in self.lines:
                yield from line # 逐个生成该行的 Segment
                yield new_line # 生成换行符
        else:
            for line in self.lines:
                yield from line # 逐个生成该行的 Segment


if __name__ == "__main__":  # pragma: no cover
    # [模块测试与演示]
    # 这部分代码展示了 Segment 的工作原理，是学习 Rich 内部机制的好例子。
    from rich.console import Console
    from rich.syntax import Syntax
    from rich.text import Text

    code = """from rich.console import Console
console = Console()
text = Text.from_markup("Hello, [bold magenta]World[/]!")
console.print(text)"""

    text = Text.from_markup("Hello, [bold magenta]World[/]!")

    console = Console()

    # [演示 1：标题]
    console.rule("rich.Segment")
    
    # [演示 2：介绍]
    console.print(
        "A Segment is the last step in the Rich render process before generating text with ANSI codes."
    )
    
    # [演示 3：展示代码]
    console.print("\nConsider the following code:\n")
    console.print(Syntax(code, "python", line_numbers=True))
    
    # [演示 4：渲染过程]
    console.print()
    console.print(
        "When you call [b]print()[/b], Rich [i]renders[/i] the object in to the following:\n"
    )
    # [关键步骤]：调用 console.render 获取 Segment 流
    fragments = list(console.render(text))
    console.print(fragments) # 直接打印 Segment 对象（会显示其文本内容）
    
    # [演示 5：最终输出]
    console.print()
    console.print("The Segments are then processed to produce the following output:\n")
    console.print(text) # 最终的、带有样式的输出
    
    # [总结]
    console.print(
        "\nYou will only need to know this if you are implementing your own Rich renderables."
    )
