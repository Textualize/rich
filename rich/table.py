from dataclasses import dataclass, field, replace
from __future__ import annotations  # 关键：延迟类型评估
from rich.console import Console, ConsoleOptions, RenderResult  # 确保类型导入

class Table(JupyterMixin):
    def _render(
        self,
        console: Console,  # 明确类型
        options: ConsoleOptions,  # 明确类型
        widths: List[int]
    ) -> RenderResult:  # 明确返回值类型
        # ... 其余代码保持不变 ...

        from typing import (
        TYPE_CHECKING,
        Dict,
        Iterable,
        List,
        NamedTuple,
        Optional,
        Sequence,
        Tuple,
        Union,
        )

# [导入分析]
# 引入了大量内部辅助模块：
# - _ratio: 处理列宽比例分配（如 1:2:1）。
# - _pick: 辅助函数。
# - _loop: 循环辅助（如第一个、最后一个元素的判断）。
from . import box, errors
from ._loop import loop_first_last, loop_last
from ._pick import pick_bool
from ._ratio import ratio_distribute, ratio_reduce
from .align import VerticalAlignMethod
from .jupyter import JupyterMixin
from .measure import Measurement
from .padding import Padding, PaddingDimensions
from .protocol import is_renderable
from .segment import Segment
from .style import Style, StyleType
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
    """[数据类：列配置]
    
    定义表格中某一列的属性和行为。
    它不存储实际的数据内容（单元格内容存储在 Table 中），而是存储如何显示这一列的规则。
    """

    header: "RenderableType" = ""
    """RenderableType: 列头内容（通常是字符串）"""

    footer: "RenderableType" = ""
    """RenderableType: 列脚内容"""

    header_style: StyleType = ""
    """StyleType: 列头的样式"""

    footer_style: StyleType = ""
    """StyleType: 列脚的样式"""

    style: StyleType = ""
    """StyleType: 列单元格的默认样式"""

    justify: "JustifyMethod" = "left"
    """str: 文本对齐方式 ("left", "center", "right", or "full")"""

    vertical: "VerticalAlignMethod" = "top"
    """str: 垂直对齐方式 ("top", "middle", or "bottom")"""

    overflow: "OverflowMethod" = "ellipsis"
    """str: 文本溢出处理方式 (默认为省略号)"""

    width: Optional[int] = None
    """Optional[int]: 列的固定宽度，None 表示自动计算"""

    min_width: Optional[int] = None
    """Optional[int]: 列的最小宽度"""

    max_width: Optional[int] = None
    """Optional[int]: 列的最大宽度"""

    ratio: Optional[int] = None
    """Optional[int]: 
    [关键属性：比例宽度]
    当 Table.expand=True 时，列宽按比例分配。
    例如：ratio=1 和 ratio=2 的两列，后者宽度是前者的两倍。
    """
    no_wrap: bool = False
    """bool: 是否禁用自动换行"""

    highlight: bool = False
    """bool: 是否对该列内容进行语法高亮"""

    _index: int = 0
    """Index of column."""

    # [数据结构设计]
    # 使用 default_factory=list 确保每个 Column 实例都有自己独立的列表，避免共享。
    _cells: List["RenderableType"] = field(default_factory=list)

    def copy(self) -> "Column":
        """[原型模式：复制列配置]
        
        使用 dataclasses.replace 创建一个副本。
        注意：这里显式将 _cells 设置为空列表 []，意味着复制的是“配置”而非“数据”。
        """
        return replace(self, _cells=[])

    @property
    def cells(self) -> Iterable["RenderableType"]:
        """[属性：获取单元格内容]
        
        这是一个生成器属性，方便遍历该列的所有单元格（不包括表头和表脚）。
        """
        yield from self._cells

    @property
    def flexible(self) -> bool:
        """[属性：判断是否为弹性列]
        
        如果定义了 ratio，说明该列宽度是动态的，可以伸缩。
        这对于自动布局算法至关重要。
        """
        return self.ratio is not None


@dataclass
class Row:
    """[数据类：行配置]
    
    存储行的元数据，不存储具体单元格数据（单元格数据存储在 Column 中，通过索引对应）。
    """

    style: Optional[StyleType] = None
    """Style to apply to row."""

    end_section: bool = False
    """[布局控制：分段标记]
    如果为 True，表示这是一个逻辑段落的结束，通常会在该行下方强制绘制一条分割线。
    """


class _Cell(NamedTuple):
    """[数据结构：单元格定义]
    
    使用 NamedTuple 定义不可变的单元格。
    它将内容和样式封装在一起，作为渲染的最小单元。
    """
    style: StyleType
    """Style to apply to cell."""
    renderable: "RenderableType"
    """Cell renderable."""
    vertical: VerticalAlignMethod
    """Cell vertical alignment."""


class Table(JupyterMixin):
    """[核心类：表格]
    
    Rich 中最复杂且功能最强大的组件之一。
    支持：自动宽度计算、比例分配、嵌套渲染、丰富的边框样式。
    """

    columns: List[Column]
    rows: List[Row]

    def __init__(
        self,
        *headers: Union[Column, str],
        title: Optional[TextType] = None,
        caption: Optional[TextType] = None,
        width: Optional[int] = None,
        min_width: Optional[int] = None,
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
        row_styles: Optional[Iterable[StyleType]] = None,
        header_style: Optional[StyleType] = "table.header",
        footer_style: Optional[StyleType] = "table.footer",
        border_style: Optional[StyleType] = None,
        title_style: Optional[StyleType] = None,
        caption_style: Optional[StyleType] = None,
        title_justify: "JustifyMethod" = "center",
        caption_justify: "JustifyMethod" = "center",
        highlight: bool = False,
    ) -> None:
        # [状态初始化]
        self.columns: List[Column] = []
        self.rows: List[Row] = []
        
        # [属性映射]
        self.title = title
        self.caption = caption
        self.width = width
        self.min_width = min_width
        self.box = box
        self.safe_box = safe_box
        
        # [内部状态处理]
        # 使用 Padding.unpack 将各种格式的 padding 参数（整数或元组）标准化为。
        self._padding = Padding.unpack(padding)
        self.pad_edge = pad_edge
        self._expand = expand
        
        # [显示开关]
        self.show_header = show_header
        self.show_footer = show_footer
        self.show_edge = show_edge
        self.show_lines = show_lines
        self.leading = leading
        self.collapse_padding = collapse_padding
        
        # [样式配置]
        self.style = style
        self.header_style = header_style or ""
        self.footer_style = footer_style or ""
        self.border_style = border_style
        self.title_style = title_style
        self.caption_style = caption_style
        self.title_justify: "JustifyMethod" = title_justify
        self.caption_justify: "JustifyMethod" = caption_justify
        self.highlight = highlight
        
        # [行样式列表]
        # 支持传入多个样式，实现斑马纹效果（隔行变色）。
        self.row_styles: Sequence[StyleType] = list(row_styles or [])
        
        # [初始化列]
        append_column = self.columns.append
        for header in headers:
            if isinstance(header, str):
                # 如果传入的是字符串，自动创建一个以该字符串为头的 Column
                self.add_column(header=header)
            else:
                # 如果传入的是 Column 对象，直接添加并设置索引
                header._index = len(self.columns)
                append_column(header)

    @classmethod
    def grid(
        cls,
        *headers: Union[Column, str],
        padding: PaddingDimensions = 0,
        collapse_padding: bool = True,
        pad_edge: bool = False,
        expand: bool = False,
    ) -> "Table":
        """[工厂方法：网格表格]
        
        创建一个没有边框、没有表头的极简表格。
        常用于对齐多列文本，而不是展示数据表。
        """
        return cls(
            *headers,
            box=None, # 关键：无边框
            padding=padding,
            collapse_padding=collapse_padding,
            show_header=False, # 关键：无表头
            show_footer=False,
            show_edge=False,
            pad_edge=pad_edge,
            expand=expand,
        )

    @property
    def expand(self) -> bool:
        """[属性：展开逻辑]
        
        判定表格是否需要扩展到最大可用宽度。
        如果显式设置了 width，也等同于 expand。
        """
        return self._expand or self.width is not None

    @expand.setter
    def expand(self, expand: bool) -> None:
        self._expand = expand

    @property
    def _extra_width(self) -> int:
        """[布局计算：额外宽度开销]
        
        计算非内容区域占用的字符数（边框线、边缘）。
        
        公式：
        1. 如果有边缘 且显示边缘：+2 (左边框 + 右边框)
        2. 如果有边框：+ (列数 - 1) (列之间的竖线)
        """
        width = 0
        if self.box and self.show_edge:
            width += 2
        if self.box:
            width += len(self.columns) - 1
        return width

    @property
    def row_count(self) -> int:
        """Get the current number of rows."""
        return len(self.rows)

    def get_row_style(self, console: "Console", index: int) -> StyleType:
        """[样式计算：获取行样式]
        
        计算某一行的最终样式。
        逻辑：
        基础样式 (null) + 循环样式 + 行特定样式
        """
        style = Style.null()
        if self.row_styles:
            # 使用取模运算 (%) 实现样式的循环应用
            style += console.get_style(self.row_styles[index % len(self.row_styles)])
        row_style = self.rows[index].style
        if row_style is not None:
            style += console.get_style(row_style)
        return style

    def __rich_measure__(
        self, console: "Console", options: "ConsoleOptions"
    ) -> Measurement:
        """[渲染协议：尺寸测量]
        
        这是布局算法的核心入口。
        它计算表格渲染所需的“最小宽度”和“最大宽度”。
        
        流程：
        1. 确定最大可用宽度。
        2. 减去边框开销 (_extra_width)。
        3. 调用 _calculate_column_widths 分配各列宽度。
        4. 测量每一列的内容，求和得到总尺寸。
        """
        max_width = options.max_width
        if self.width is not None:
            max_width = self.width
        if max_width < 0:
            return Measurement(0, 0)

        extra_width = self._extra_width
        # [核心算法]：计算列宽分配
        max_width = sum(
            self._calculate_column_widths(
                console, options.update_width(max_width - extra_width)
            )
        )
        _measure_column = self._measure_column

        # 测量每一列
        measurements = [
            _measure_column(console, options.update_width(max_width), column)
            for column in self.columns
        ]
        
        # 计算总的最小和最大宽度，并加回边框开销
        minimum_width = (
            sum(measurement.minimum for measurement in measurements) + extra_width
        )
        maximum_width = (
            sum(measurement.maximum for measurement in measurements) + extra_width
            if (self.width is None)
            else self.width
        )
        measurement = Measurement(minimum_width, maximum_width)
        measurement = measurement.clamp(self.min_width)
        return measurement

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
        header_style: Optional[StyleType] = None,
        highlight: Optional[bool] = None,
        footer_style: Optional[StyleType] = None,
        style: Optional[StyleType] = None,
        justify: "JustifyMethod" = "left",
        vertical: "VerticalAlignMethod" = "top",
        overflow: "OverflowMethod" = "ellipsis",
        width: Optional[int] = None,
        min_width: Optional[int] = None,
        max_width: Optional[int] = None,
        ratio: Optional[int] = None,
        no_wrap: bool = False,
    ) -> None:
        """[建造者模式：添加列]
        
        动态地向表格添加新列。
        这是一个流式接口，可以在循环中调用以构建表头。
        """
        column = Column(
            _index=len(self.columns),
            header=header,
            footer=footer,
            header_style=header_style or "",
            # 逻辑或：如果未指定，则继承 Table 的全局设置
            highlight=highlight if highlight is not None else self.highlight,
            footer_style=footer_style or "",
            style=style or "",
            justify=justify,
            vertical=vertical,
            overflow=overflow,
            width=width,
            min_width=min_width,
            max_width=max_width,
            ratio=ratio,
            no_wrap=no_wrap,
        )
        self.columns.append(column)


        def add_row(
        self,
        *renderables: Optional["RenderableType"],
        style: Optional[StyleType] = None,
        end_section: bool = False,
    ) -> None:
        #[数据操作：添加行]
        
       # 向表格添加一行数据。
        
        #智能特性：
        #1. 自动填充：如果传入的数据少于列数，自动用 None (空单元格) 填充。
        #2. 自动扩列：如果传入的数据多于列数，自动创建新的 Column 对象来容纳数据。
        #3. 类型校验：确保数据是可渲染的 (Renderable)。
       

            def add_cell(column: Column, renderable: "RenderableType") -> None:
                column._cells.append(renderable)

        cell_renderables: List[Optional["RenderableType"]] = list(renderables)

        columns = self.columns
        # [逻辑 1：数据不足时填充 None]
        if len(cell_renderables) < len(columns):
            cell_renderables = [
                *cell_renderables,
                *[None] * (len(columns) - len(cell_renderables)),
            ]
        for index, renderable in enumerate(cell_renderables):
            if index == len(columns):
                # [逻辑 2：数据溢出时创建新列]
                column = Column(_index=index, highlight=self.highlight)
                # 为之前没有该列的行补上空数据，保持表格矩形结构
                for _ in self.rows:
                    add_cell(column, Text(""))
                self.columns.append(column)
            else:
                column = columns[index]
            
            # [逻辑 3：数据处理]
            if renderable is None:
                add_cell(column, "")
            elif is_renderable(renderable):
                add_cell(column, renderable)
            else:
                raise errors.NotRenderableError(
                    f"unable to render {type(renderable).__name__}; a string or other renderable object is required"
                )
        # 创建行对象
        self.rows.append(Row(style=style, end_section=end_section))

    def add_section(self) -> None:
        """[辅助功能：添加分段]
        
        在当前行之后标记一个“段”结束。
        渲染时，这通常意味着在当前行下方画一条明显的分割线。
        """
        if self.rows:
            self.rows[-1].end_section = True

    def __rich_console__(
        self, console: "Console", options: "ConsoleOptions"
    ) -> "RenderResult":
        """[渲染协议：入口点]
        
        这是 Rich 渲染引擎调用的主方法。
        流程：
        1. 计算最终列宽。
        2. 渲染标题（如果有）。
        3. 调用核心渲染方法 _render。
        4. 渲染说明文字（如果有）。
        """
        if not self.columns:
            yield Segment("\n")
            return

        max_width = options.max_width
        if self.width is not None:
            max_width = self.width

        extra_width = self._extra_width
        # [关键步骤：调用布局算法计算各列宽度]
        widths = self._calculate_column_widths(
            console, options.update_width(max_width - extra_width)
        )
        table_width = sum(widths) + extra_width

        # 准备渲染选项，限制宽度为计算出的表格总宽
        render_options = options.update(
            width=table_width, highlight=self.highlight, height=None
        )

        # [辅助函数：渲染注解（标题/说明）]
        def render_annotation(
            text: TextType, style: StyleType, justify: "JustifyMethod" = "center"
        ) -> "RenderResult":
            render_text = (
                console.render_str(text, style=style, highlight=False)
                if isinstance(text, str)
                else text
            )
            return console.render(
                render_text, options=render_options.update(justify=justify)
            )

        if self.title:
            yield from render_annotation(
                self.title,
                style=Style.pick_first(self.title_style, "table.title"),
                justify=self.title_justify,
            )
        # [核心渲染：实际表格内容]
        yield from self._render(console, render_options, widths)
        if self.caption:
            yield from render_annotation(
                self.caption,
                style=Style.pick_first(self.caption_style, "table.caption"),
                justify=self.caption_justify,
            )

    def _calculate_column_widths(
        self, console: "Console", options: "ConsoleOptions"
    ) -> List[int]:
        """[核心算法：列宽计算]
        
        这是 Rich 表格布局引擎的心脏。它要解决一个约束满足问题：
        在满足 min_width/max_width/ratio 的前提下，分配 max_width。
        
        策略顺序：
        1. 测量内容，获得自然宽度。
        2. 如果 expand=True，按 ratio 分配剩余空间。
        3. 如果总宽 > max_width，进行压缩 (_collapse_widths)。
        4. 如果压缩后仍超宽，强制平均缩减（最后手段）。
        5. 如果总宽 < max_width 且 expand=True，填充剩余空间。
        """
        max_width = options.max_width
        columns = self.columns
        # 1. [测量阶段] 获取每列的最小和最大内容宽度
        width_ranges = [
            self._measure_column(console, options, column) for column in columns
        ]
        # 默认使用最大内容宽度作为起始宽度
        widths = [_range.maximum or 1 for _range in width_ranges]
        get_padding_width = self._get_padding_width
        extra_width = self._extra_width
        
        # 2. [扩展阶段：处理比例]
        if self.expand:
            # 收集所有可伸缩列的比例
            ratios = [col.ratio or 0 for col in columns if col.flexible]
            if any(ratios):
                # 固定宽度列取最大值，伸缩列先不算
                fixed_widths = [
                    0 if column.flexible else _range.maximum
                    for _range, column in zip(width_ranges, columns)
                ]
                # 计算伸缩列的最小宽（防止被压扁）
                flex_minimum = [
                    (column.width or 1) + get_padding_width(column._index)
                    for column in columns
                    if column.flexible
                ]
                flexible_width = max_width - sum(fixed_widths)
                # 使用 ratio_distribute 算法分配剩余空间
                flex_widths = ratio_distribute(flexible_width, ratios, flex_minimum)
                iter_flex_widths = iter(flex_widths)
                for index, column in enumerate(columns):
                    if column.flexible:
                        widths[index] = fixed_widths[index] + next(iter_flex_widths)
        table_width = sum(widths)

        # 3. [收缩阶段：如果超出最大宽度]
        if table_width > max_width:
            # 先尝试通过压缩允许换行的列来适应
            widths = self._collapse_widths(
                widths,
                [(column.width is None and not column.no_wrap) for column in columns],
                max_width,
            )
            table_width = sum(widths)
            # 如果还是太宽，最后手段：按比例强制缩减所有列
            if table_width > max_width:
                excess_width = table_width - max_width
                widths = ratio_reduce(excess_width, [1] * len(widths), widths, widths)
                table_width = sum(widths)

            # 重新测量，确保压缩后的宽度不小于内容的最小宽度
            width_ranges = [
                self._measure_column(console, options.update_width(width), column)
                for width, column in zip(widths, columns)
            ]
            widths = [_range.maximum or 0 for _range in width_ranges]

        # 4. [填充阶段：如果小于最大宽度且允许扩展]
        if (table_width < max_width and self.expand) or (
            self.min_width is not None and table_width < (self.min_width - extra_width)
        ):
            _max_width = (
                max_width
                if self.min_width is None
                else min(self.min_width - extra_width, max_width)
            )
            # 将剩余空间按当前宽度比例分配给各列
            pad_widths = ratio_distribute(_max_width - table_width, widths)
            widths = [_width + pad for _width, pad in zip(widths, pad_widths)]

        return widths

    @classmethod
    def _collapse_widths(
        cls, widths: List[int], wrapable: List[bool], max_width: int
    ) -> List[int]:
        """[算法辅助：宽度压缩]
        
        尝试减少列宽以适应 max_width。
        策略：优先减少“最宽”且“允许换行”的列。
        
        这是一个迭代过程：
        1. 找到当前最大的列宽。
        2. 将其缩减到第二大的列宽（这样能保持相对比例，不会出现某列极窄的情况）。
        3. 重复直到总宽满足要求。
        """
        total_width = sum(widths)
        excess_width = total_width - max_width
        if any(wrapable):
            while total_width and excess_width > 0:
                # 找到允许换行的列中的最大宽度
                max_column = max(
                    width for width, allow_wrap in zip(widths, wrapable) if allow_wrap
                )
                # 找到允许换行的列中的第二大宽度
                second_max_column = max(
                    width if allow_wrap and width != max_column else 0
                    for width, allow_wrap in zip(widths, wrapable)
                )
                column_difference = max_column - second_max_column
                # 只有最大宽度的列有比例（权重），其他为 0
                ratios = [
                    (1 if (width == max_column and allow_wrap) else 0)
                    for width, allow_wrap in zip(widths, wrapable)
                ]
                if not any(ratios) or not column_difference:
                    break
                # 计算这次迭代能缩减多少
                max_reduce = [min(excess_width, column_difference)] * len(widths)
                widths = ratio_reduce(excess_width, ratios, max_reduce, widths)

                total_width = sum(widths)
                excess_width = total_width - max_width
        return widths

    def _get_cells(
        self, console: "Console", column_index: int, column: Column
    ) -> Iterable[_Cell]:
        """[数据获取：获取列的所有单元格]
        
        返回一个生成器，按顺序产生该列的：表头 -> 数据行 -> 表脚。
        同时处理复杂的 Padding 逻辑。
        """

        collapse_padding = self.collapse_padding
        pad_edge = self.pad_edge
        padding = self.padding
        any_padding = any(padding)

        first_column = column_index == 0
        last_column = column_index == len(self.columns) - 1

        # [性能优化：Padding 缓存]
        # 由于单元格的 padding 取决于它是否在边缘，共有 4 种组合 (首/中/尾)。
        # 缓存计算结果避免重复计算。
        _padding_cache: Dict[Tuple[bool, bool], Tuple[int, int, int, int]] = {}

        def get_padding(first_row: bool, last_row: bool) -> Tuple[int, int, int, int]:
            cached = _padding_cache.get((first_row, last_row))
            if cached:
                return cached
            top, right, bottom, left = padding

            # [逻辑：Padding 折叠]
            # 如果开启折叠，相邻单元格的共享边距会合并。
            # 例如：左边距 1 + 右边距 1，折叠后只需要 1。
            if collapse_padding:
                if not first_column:
                    left = max(0, left - right)
                if not last_row:
                    bottom = max(0, top - bottom)

            # [逻辑：边缘 Padding]
            if not pad_edge:
                if first_column:
                    left = 0
                if last_column:
                    right = 0
                if first_row:
                    top = 0
                if last_row:
                    bottom = 0
            _padding = (top, right, bottom, left)
            _padding_cache[(first_row, last_row)] = _padding
            return _padding

        # [构建原始单元格列表]
        raw_cells: List[Tuple[StyleType, "RenderableType"]] = []
        _append = raw_cells.append
        get_style = console.get_style
        if self.show_header:
            # 样式叠加：表头样式 + 列表头样式
            header_style = get_style(self.header_style or "") + get_style(
                column.header_style
            )
            _append((header_style, column.header))
        # 添加该列的所有数据行
        cell_style = get_style(column.style or "")
        for cell in column.cells:
            _append((cell_style, cell))
        if self.show_footer:
            footer_style = get_style(self.footer_style or "") + get_style(
                column.footer_style
            )
            _append((footer_style, column.footer))

        if any_padding:
            # 如果有 padding，将内容包裹在 Padding 对象中
            _Padding = Padding
            for first, last, (style, renderable) in loop_first_last(raw_cells):
                yield _Cell(
                    style,
                    _Padding(renderable, get_padding(first, last)),
                    # 优先使用渲染对象自带的垂直对齐，否则使用列的设置
                    getattr(renderable, "vertical", None) or column.vertical,
                )
        else:
            # 无 padding 直接返回
            for style, renderable in raw_cells:
                yield _Cell(
                    style,
                    renderable,
                    getattr(renderable, "vertical", None) or column.vertical,
                )

    def _get_padding_width(self, int) -> int:
        """[计算辅助：Padding 宽度开销]
        
        计算某一列的 padding 在水平方向上占用的总宽度。
        如果开启了 collapse_padding，则要减去重叠部分。
        """
        _, pad_right, _, pad_left = self.padding
        if self.collapse_padding:
            if column_index > 0:
                # 非首列：左 padding 可能会被上一列的右 padding 抵消
                pad_left = max(0, pad_left - pad_right)
        return pad_left + pad_right

    def _measure_column(
        self,
        console: "Console",
        options: "ConsoleOptions",
        column: Column,
    ) -> Measurement:
        """[布局测量：列宽测量]
        
        测量一列中所有单元格（包括表头、表脚）的最小和最大宽度。
        
        返回的 Measurement 对象包含了该列在不换行/强制换行情况下的尺寸范围。
        """

        max_width = options.max_width
        if max_width < 1:
            return Measurement(0, 0)

        padding_width = self._get_padding_width(column._index)

        if column.width is not None:
            # 如果列指定了固定宽度，直接返回
            return Measurement(
                column.width + padding_width, column.width + padding_width
            ).with_maximum(max_width)
        
        # [动态宽度列]：需要遍历所有单元格进行测量
        min_widths: List[int] = []
        max_widths: List[int] = []
        append_min = min_widths.append
        append_max = max_widths.append
        get_render_width = Measurement.get
        
        # 测量该列的每个单元格
        for cell in self._get_cells(console, column._index, column):
            _min, _max = get_render_width(console, options, cell.renderable)
            append_min(_min)
            append_max(_max)

        # 聚合：取所有单元格中最宽的最小宽度，和最宽的最大宽度
        measurement = Measurement(
            max(min_widths) if min_widths else 1,
            max(max_widths) if max_widths else max_width,
        ).with_maximum(max_width)
        
        # 限制：应用用户设置的 min_width / max_width 约束
        measurement = measurement.clamp(
            None if column.min_width is None else column.min_width + padding_width,
            None if column.max_width is None else column.max_width + padding_width,
        )
        return measurement

        def _render(
        self, console: "Console", options: "ConsoleOptions", widths: List[int]
    ) -> "RenderResult":
        #[核心渲染引擎：绘制表格]
        
        #这是 Table 类最复杂的方法。它将逻辑上的行列数据转换为最终显示的 Segment 流。
        
        #主要流程：
        #1. 转置数据（列转行）。
        #2. 渲染每个单元格为 Segment 列表。
        #3. 计算行高（处理多行单元格）。
        #4. 垂直对齐单元格内容。
        #5. 逐行输出，拼接边框和内容。

        # 1. [样式准备]
        # 合并表格全局样式和边框样式
            table_style = console.get_style(self.style or "")

        border_style = table_style + console.get_style(self.border_style or "")
        
        # 2. [数据转置：关键步骤]
        # _get_cells 返回的是每一列的数据（列式存储）。
        # 使用 zip(*...) 将其“转置”为每一行的数据（行式存储），方便逐行绘制。
        # row_cells 是一个 List[Tuple[_Cell, ...]]，每个 Tuple 代表一行。
        _column_cells = (
            self._get_cells(console, column_index, column)
            for column_index, column in enumerate(self.columns)
        )
        row_cells: List[Tuple[_Cell, ...]] = list(zip(*_column_cells))
        
        # 3. [边框准备]
        # substitute: 处理旧版 Windows 终端字符兼容性问题（替换不支持的字符）。
        # get_plain_headed_box: 如果不显示表头，将表头专用的粗边框转为普通边框。
        _box = (
            self.box.substitute(
                options, safe=pick_bool(self.safe_box, console.safe_box)
            )
            if self.box
            else None
        )
        _box = _box.get_plain_headed_box() if _box and not self.show_header else _box

        new_line = Segment.line()

        columns = self.columns
        show_header = self.show_header
        show_footer = self.show_footer
        show_edge = self.show_edge
        show_lines = self.show_lines
        leading = self.leading

        _Segment = Segment
        
        # 4. [预加载边框 Segment]
        # 为了性能，预先创建好不同位置的边框字符 Segment。
        if _box:
            box_segments = [
                # Header 部分边框（左、右、中）
                (
                    _Segment(_box.head_left, border_style),
                    _Segment(_box.head_right, border_style),
                    _Segment(_box.head_vertical, border_style),
                ),
                # Body 部分边框
                (
                    _Segment(_box.mid_left, border_style),
                    _Segment(_box.mid_right, border_style),
                    _Segment(_box.mid_vertical, border_style),
                ),
                # Footer 部分边框
                (
                    _Segment(_box.foot_left, border_style),
                    _Segment(_box.foot_right, border_style),
                    _Segment(_box.foot_vertical, border_style),
                ),
            ]
            # [绘制顶边框]
            if show_edge:
                yield _Segment(_box.get_top(widths), border_style)
                yield new_line
        else:
            box_segments = []

        get_row_style = self.get_row_style
        get_style = console.get_style

        # 5. [逐行渲染循环]
        for index, (first, last, row_cell) in enumerate(loop_first_last(row_cells)):
            # 判断当前行是表头、表脚还是数据行
            header_row = first and show_header
            footer_row = last and show_footer
            
            # 获取对应的 Row 元数据（用于获取行样式、段结束标记等）
            # 注意：如果是表头或表脚，Row 列表中可能没有对应的对象（逻辑上）
            row = (
                self.rows[index - show_header]
                if (not header_row and not footer_row)
                else None
            )
            
            max_height = 1
            cells: List[List[List[Segment]]] = []
            
            # 确定当前行的样式
            if header_row or footer_row:
                row_style = Style.null()
            else:
                row_style = get_style(
                    get_row_style(console, index - 1 if show_header else index)
                )
            
            # [步骤 A：渲染单元格内容]
            # 将每个单元格的 renderable 渲染为 List[List[Segment]] (即多行文本)
            for width, cell, column in zip(widths, row_cell, columns):
                render_options = options.update(
                    width=width,
                    justify=column.justify,
                    no_wrap=column.no_wrap,
                    overflow=column.overflow,
                    height=None,
                    highlight=column.highlight,
                )
                lines = console.render_lines(
                    cell.renderable,
                    render_options,
                    style=get_style(cell.style) + row_style,
                )
                # 记录该行中最大的高度（行高由最高的单元格决定）
                max_height = max(max_height, len(lines))
                cells.append(lines)

            row_height = max(len(cell) for cell in cells)

            # [辅助函数：单元格垂直对齐]
            def align_cell(
                cell: List[List[Segment]],
                vertical: "VerticalAlignMethod",
                width: int,
                style: Style,
            ) -> List[List[Segment]]:
                # 表头底部对齐，表脚顶部对齐，默认遵循配置
                if header_row:
                    vertical = "bottom"
                elif footer_row:
                    vertical = "top"

                if vertical == "top":
                    return _Segment.align_top(cell, width, row_height, style)
                elif vertical == "middle":
                    return _Segment.align_middle(cell, width, row_height, style)
                return _Segment.align_bottom(cell, width, row_height, style)

            # [步骤 B：形状调整与对齐]
            # 1. 调用 align_cell 填充高度。
            # 2. 调用 set_shape 填充宽度（使所有单元格都是标准的 width x row_height 矩形）。
            cells[:] = [
                _Segment.set_shape(
                    align_cell(
                        cell,
                        _cell.vertical,
                        width,
                        get_style(_cell.style) + row_style,
                    ),
                    width,
                    max_height,
                )
                for width, _cell, cell, column in zip(widths, row_cell, cells, columns)
            ]

            # [步骤 C：绘制边框和内容]
            if _box:
                # 如果有页脚，先画页脚的上边框
                if last and show_footer:
                    yield _Segment(
                        _box.get_row(widths, "foot", edge=show_edge), border_style
                    )
                    yield new_line
                
                # 根据当前行位置（首/中/尾）选择边框样式
                left, right, _divider = box_segments[0 if first else (2 if last else 1)]

                # [分隔符样式处理]
                # 如果分隔符是空格，则继承行的背景色，这样看起来像连通的背景。
                divider = (
                    _divider
                    if _divider.text.strip()
                    else _Segment(
                        _divider.text, row_style.background_style + _divider.style
                    )
                )
                
                # 逐行输出 Segment
                for line_no in range(max_height):
                    if show_edge:
                        yield left # 左边框
                    for last_cell, rendered_cell in loop_last(cells):
                        yield from rendered_cell[line_no] # 单元格内容
                        if not last_cell:
                            yield divider # 列分隔符
                    if show_edge:
                        yield right # 右边框
                    yield new_line
            
            # [无框模式]
            else:
                for line_no in range(max_height):
                    for rendered_cell in cells:
                        yield from rendered_cell[line_no]
                    yield new_line
            
            # 如果有表头，画表头的下边框
            if _box and first and show_header:
                yield _Segment(
                    _box.get_row(widths, "head", edge=show_edge), border_style
                )
                yield new_line
                
            # [步骤 D：行后处理]
            # 检查是否需要绘制分段线（show_lines, leading, end_section）
            end_section = row and row.end_section
            if _box and (show_lines or leading or end_section):
                if (
                    not last
                    and not (show_footer and index >= len(row_cells) - 2)
                    and not (show_header and header_row)
                ):
                    if leading:
                        # 绘制空行
                        yield _Segment(
                            _box.get_row(widths, "mid", edge=show_edge) * leading,
                            border_style,
                        )
                    else:
                        # 绘制实线
                        yield _Segment(
                            _box.get_row(widths, "row", edge=show_edge), border_style
                        )
                    yield new_line

        # [绘制底边框]
        if _box and show_edge:
            yield _Segment(_box.get_bottom(widths), border_style)
            yield new_line


if __name__ == "__main__":  # pragma: no cover
    # [模块测试与演示]
    # 这部分代码展示了 Table 类的各种用法和样式配置。
    from rich.console import Console
    from rich.highlighter import ReprHighlighter

    from ._timer import timer

    # [计时器上下文]：测量渲染耗时
    with timer("Table render"):
        table = Table(
            title="Star Wars Movies",
            caption="Rich example table",
            caption_justify="right",
        )

        # [添加列]
        table.add_column(
            "Released", header_style="bright_cyan", style="cyan", no_wrap=True
        )
        table.add_column("Title", style="magenta")
        table.add_column("Box Office", justify="right", style="green")

        # [添加行数据]
        table.add_row(
            "Dec 20, 2019",
            "Star Wars: The Rise of Skywalker",
            "$952,110,690",
        )
        table.add_row("May 25, 2018", "Solo: A Star Wars Story", "$393,151,347")
        table.add_row(
            "Dec 15, 2017",
            "Star Wars Ep. V111: The Last Jedi",
            "$1,332,539,889",
            style="on black",
            end_section=True, # 标记段落结束，会画线
        )
        table.add_row(
            "Dec 16, 2016",
            "Rogue One: A Star Wars Story",
            "$1,332,439,889",
        )

        def header(text: str) -> None:
            """[辅助函数]：打印带分割线的标题"""
            console.print()
            console.rule(highlight(text))
            console.print()

        console = Console()
        highlight = ReprHighlighter()
        
        # [演示 1：默认表格]
        header("Example Table")
        console.print(table, justify="center")

        # [演示 2：自动扩展模式]
        # 表格宽度填满控制台
        table.expand = True
        header("expand=True")
        console.print(table)

        # [演示 3：固定宽度]
        # 强制宽度为 50
        table.width = 50
        header("width=50")

        console.print(table, justify="center")

        # [演示 4：行交替样式]
        table.width = None
        table.expand = False
        table.row_styles = ["dim", "none"] # 偶数行变暗
        header("row_styles=['dim', 'none']")

        console.print(table, justify="center")

        # [演示 5：行间距]
        table.width = None
        table.expand = False
        table.row_styles = ["dim", "none"]
        table.leading = 1 # 行间距增加
        header("leading=1, row_styles=['dim', 'none']")
        console.print(table, justify="center")

        # [演示 6：显示所有网格线]
        table.width = None
        table.expand = False
        table.row_styles = ["dim", "none"]
        table.show_lines = True
        table.leading = 0
        header("show_lines=True, row_styles=['dim', 'none']")
        console.print(table, justify="center")
