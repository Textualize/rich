# [导入分析]
# 该文件大量使用了 typing 模块（如 Protocol, Literal, TypeAlias 等），表明项目高度重视类型安全和静态检查。
# 这符合高质量开源项目的规范，有助于 IDE 提示和减少运行时错误。

import inspect
import os
import sys
import threading
import zlib
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from functools import wraps
from getpass import getpass
from html import escape
from inspect import isclass
from itertools import islice
from math import ceil
from time import monotonic
from types import FrameType, ModuleType, TracebackType
from typing import (
    IO,
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Literal,
    Mapping,
    NamedTuple,
    Optional,
    Protocol,
    TextIO,
    Tuple,
    Type,
    Union,
    cast,
    runtime_checkable,
)

from rich._null_file import NULL_FILE

from . import errors, themes
from ._emoji_replace import _emoji_replace
from ._export_format import CONSOLE_HTML_FORMAT, CONSOLE_SVG_FORMAT
from ._fileno import get_fileno
from ._log_render import FormatTimeCallable, LogRender
from .align import Align, AlignMethod
from .color import ColorSystem, blend_rgb
from .control import Control
from .emoji import EmojiVariant
from .highlighter import NullHighlighter, ReprHighlighter
from .markup import render as render_markup
from .measure import Measurement, measure_renderables
from .pager import Pager, SystemPager
from .pretty import Pretty, is_expandable
from .protocol import rich_cast
from .region import Region
from .scope import render_scope
from .screen import Screen
from .segment import Segment
from .style import Style, StyleType
from .styled import Styled
from .terminal_theme import DEFAULT_TERMINAL_THEME, SVG_EXPORT_THEME, TerminalTheme
from .text import Text, TextType
from .theme import Theme, ThemeStack

if TYPE_CHECKING:
    from ._windows import WindowsConsoleFeatures
    from .live import Live
    from .status import Status

# [常量定义]
# 定义了 Jupyter 环境下的默认尺寸，以及判断当前操作系统的标志。
JUPYTER_DEFAULT_COLUMNS = 115
JUPYTER_DEFAULT_LINES = 100
WINDOWS = sys.platform == "win32"

HighlighterType = Callable[[Union[str, "Text"]], "Text"]
# [类型别名优化]
# 使用 Literal 类型限制了参数只能取特定的字符串值，这在编译期就能防止拼写错误。
JustifyMethod = Literal["default", "left", "center", "right", "full"]
OverflowMethod = Literal["fold", "crop", "ellipsis", "ignore"]


class NoChange:
    """[标记类设计]
    这是一个特殊的哨兵类，用于区分“用户传入了 None”和“用户没有传入参数”的情况。
    在 ConsoleOptions.update 方法中作为默认值非常关键。
    """
    pass


NO_CHANGE = NoChange()

# [系统资源初始化]
# 获取标准输入、输出、错误的文件描述符。这是 Python 与操作系统底层交互的基础。
try:
    _STDIN_FILENO = sys.__stdin__.fileno()  # type: ignore[union-attr]
except Exception:
    _STDIN_FILENO = 0
try:
    _STDOUT_FILENO = sys.__stdout__.fileno()  # type: ignore[union-attr]
except Exception:
    _STDOUT_FILENO = 1
try:
    _STDERR_FILENO = sys.__stderr__.fileno()  # type: ignore[union-attr]
except Exception:
    _STDERR_FILENO = 2

_STD_STREAMS = (_STDIN_FILENO, _STDOUT_FILENO, _STDERR_FILENO)
_STD_STREAMS_OUTPUT = (_STDOUT_FILENO, _STDERR_FILENO)


# [策略数据映射]
# 定义了不同终端类型（TERM环境变量）对应的色彩支持能力。
# 这体现了策略模式的数据准备阶段。
_TERM_COLORS = {
    "kitty": ColorSystem.EIGHT_BIT,
    "256color": ColorSystem.EIGHT_BIT,
    "16color": ColorSystem.STANDARD,
}


class ConsoleDimensions(NamedTuple):
    """[数据结构分析]
    使用 NamedTuple 定义不可变的数据结构。
    优点：轻量、内存占用小、可以作为字典键、自带字段访问方式（.width）。
    用途：存储终端的宽和高。
    """
    width: int
    """The width of the console in 'cells'."""
    height: int
    """The height of the console in lines."""


@dataclass
class ConsoleOptions:
    """[核心配置类 - 设计模式：参数对象 / 不可变链式构建]
    
    该类封装了渲染过程中的所有上下文配置（尺寸、编码、对齐方式等）。
    
    关键设计点：
    1. 所有的 update 方法都返回一个新的 ConsoleOptions 实例（self.copy()）。
    2. 这意味着原配置对象不会被修改，保证了渲染过程中的线程安全和状态一致性。
    """

    size: ConsoleDimensions
    """Size of console."""
    legacy_windows: bool
    """legacy_windows: flag for legacy windows."""
    min_width: int
    """Minimum width of renderable."""
    max_width: int
    """Maximum width of renderable."""
    is_terminal: bool
    """True if the target is a terminal, otherwise False."""
    encoding: str
    """Encoding of terminal."""
    max_height: int
    """Height of container (starts as terminal)"""
    justify: Optional[JustifyMethod] = None
    """Justify value override for renderable."""
    overflow: Optional[OverflowMethod] = None
    """Overflow value override for renderable."""
    no_wrap: Optional[bool] = False
    """Disable wrapping for text."""
    highlight: Optional[bool] = None
    """Highlight override for render_str."""
    markup: Optional[bool] = None
    """Enable markup when rendering strings."""
    height: Optional[int] = None

    @property
    def ascii_only(self) -> bool:
        """[逻辑判断属性]
        根据编码快速判断是否只支持 ASCII 字符。
        如果不是以 'utf' 开头的编码，通常被视为不支持宽字符（如中文）。
        """
        return not self.encoding.startswith("utf")

    def copy(self) -> "ConsoleOptions":
        """[对象创建模式：原型模式]
        创建当前对象的浅拷贝。
        由于 dataclass 主要包含基本数据类型，浅拷贝足够。
        """
        options: ConsoleOptions = ConsoleOptions.__new__(ConsoleOptions)
        options.__dict__ = self.__dict__.copy()
        return options

    def update(
        self,
        *,
        width: Union[int, NoChange] = NO_CHANGE,
        min_width: Union[int, NoChange] = NO_CHANGE,
        max_width: Union[int, NoChange] = NO_CHANGE,
        justify: Union[Optional[JustifyMethod], NoChange] = NO_CHANGE,
        overflow: Union[Optional[OverflowMethod], NoChange] = NO_CHANGE,
        no_wrap: Union[Optional[bool], NoChange] = NO_CHANGE,
        highlight: Union[Optional[bool], NoChange] = NO_CHANGE,
        markup: Union[Optional[bool], NoChange] = NO_CHANGE,
        height: Union[Optional[int], NoChange] = NO_CHANGE,
    ) -> "ConsoleOptions":
        """[流式接口 / 链式调用]
        允许在不修改原对象的情况下更新配置。
        使用 NoChange 哨兵类作为默认值，解决了 None 无法作为“不修改”标识的问题。
        
        示例用法：
            new_options = options.update(width=80, justify="center")
        """
        options = self.copy()
        if not isinstance(width, NoChange):
            options.min_width = options.max_width = max(0, width)
        if not isinstance(min_width, NoChange):
            options.min_width = min_width
        if not isinstance(max_width, NoChange):
            options.max_width = max_width
        if not isinstance(justify, NoChange):
            options.justify = justify
        if not isinstance(overflow, NoChange):
            options.overflow = overflow
        if not isinstance(no_wrap, NoChange):
            options.no_wrap = no_wrap
        if not isinstance(highlight, NoChange):
            options.highlight = highlight
        if not isinstance(markup, NoChange):
            options.markup = markup
        if not isinstance(height, NoChange):
            if height is not None:
                options.max_height = height
            options.height = None if height is None else max(0, height)
        return options

    def update_width(self, width: int) -> "ConsoleOptions":
        """[便捷方法]
        封装了更新宽度的常用操作，减少代码重复。
        """
        options = self.copy()
        options.min_width = options.max_width = max(0, width)
        return options

    def update_height(self, height: int) -> "ConsoleOptions":
        """[便捷方法]"""
        options = self.copy()
        options.max_height = options.height = height
        return options

    def reset_height(self) -> "ConsoleOptions":
        """[状态重置]
        将高度重置为 None（通常意味着自动高度）。
        """
        options = self.copy()
        options.height = None
        return options

    def update_dimensions(self, width: int, height: int) -> "ConsoleOptions":
        """[便捷方法]"""
        options = self.copy()
        options.min_width = options.max_width = max(0, width)
        options.height = options.max_height = height
        return options


@runtime_checkable
class RichCast(Protocol):
    """[接口定义：Protocol（协议）]
    
    Python 的 Protocol 是静态鸭子类型。只要一个类实现了 __rich__ 方法，
    静态类型检查器（如 mypy）就会认为它是 RichCast 的子类。
    
    这是 Rich 库扩展性的核心：允许任何自定义对象通过实现 __rich__ 方法变成可渲染对象。
    """

    def __rich__(
        self,
    ) -> Union["ConsoleRenderable", "RichCast", str]:  # pragma: no cover
        ...


@runtime_checkable
class ConsoleRenderable(Protocol):
    """[核心渲染接口]
    所有需要在终端上渲染的复杂对象（表格、进度条等）都必须实现此接口。
    
    方法：
        __rich_console__: 传入 Console 实例和配置，返回渲染结果（Segment 流）。
    """

    def __rich_console__(
        self, console: "Console", options: "ConsoleOptions"
    ) -> "RenderResult":  # pragma: no cover
        ...


# A type that may be rendered by Console.
RenderableType = Union[ConsoleRenderable, RichCast, str]
"""[类型别名]
定义了所有可渲染类型的联合类型。
这使得 Console.print() 方法可以接受字符串、表格、或任何实现了协议的对象。
"""

# The result of calling a __rich_console__ method.
RenderResult = Iterable[Union[RenderableType, Segment]]
"""[生成器类型别名]
渲染结果通常是一个生成器，按需产生 Segment，避免内存中一次性构建巨大的字符串。"""

_null_highlighter = NullHighlighter()


class CaptureError(Exception):
    """[自定义异常]
    用于在 Capture 上下文管理器中发生错误时抛出。
    """
    pass


class NewLine:
    """[基础渲染组件]
    一个最简单的 Renderable，用于生成指定数量的换行符。
    体现了“万物皆可渲染”的设计思想。
    """

    def __init__(self, count: int = 1) -> None:
        self.count = count

    def __rich_console__(
        self, console: "Console", options: "ConsoleOptions"
    ) -> Iterable[Segment]:
        yield Segment("\n" * self.count)


class ScreenUpdate:
    """[底层控制渲染]
    用于直接在屏幕的指定 绘制一组行。
    这通常用于实现复杂的动画或局部刷新效果。
    """

    def __init__(self, lines: List[List[Segment]], x: int, y: int) -> None:
        self._lines = lines
        self.x = x
        self.y = y

    def __rich_console__(
        self, console: "Console", options: ConsoleOptions
    ) -> RenderResult:
        x = self.x
        move_to = Control.move_to
        # [算法逻辑]
        # 遍历所有行，先输出“移动光标”控制序列，再输出该行的内容。
        for offset, line in enumerate(self._lines, self.y):
            yield move_to(x, offset)
            yield from line


class Capture:
    """[上下文管理器：输出捕获]
    
    功能：拦截 Console 的输出，不打印到屏幕，而是保存为字符串。
    实现：
        __enter__: 开启捕获模式。
        __exit__: 结束捕获并获取结果。
    
    应用场景：单元测试、生成文本报告。
    """

    def __init__(self, console: "Console") -> None:
        self._console = console
        self._result: Optional[str] = None

    def __enter__(self) -> "Capture":
        self._console.begin_capture()
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        # 即使发生异常，也会尝试结束捕获并保存已输出的部分
        self._result = self._console.end_capture()

    def get(self) -> str:
        """Get the result of the capture."""
        if self._result is None:
            raise CaptureError(
                "Capture result is not available until context manager exits."
            )
        return self._result


class ThemeContext:
    """[上下文管理器：临时主题切换]
    
    允许在 `with` 块内临时应用一个新的主题，退出后自动恢复原主题。
    这是栈式管理的典型应用（ThemeStack）。
    """

    def __init__(self, console: "Console", theme: Theme, inherit: bool = True) -> None:
        self.console = console
        self.theme = theme
        self.inherit = inherit

    def __enter__(self) -> "ThemeContext":
        self.console.push_theme(self.theme)
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        self.console.pop_theme()


class PagerContext:
    """[上下文管理器：分页显示]
    
    当内容超过一屏时，调用系统的分页器（如 Linux 的 less 或 more）进行显示。
    
    逻辑：
        1. 进入时：开启缓冲。
        2. 退出时：将缓冲区内容转换为文本，传给 SystemPager。
    """

    def __init__(
        self,
        console: "Console",
        pager: Optional[Pager] = None,
        styles: bool = False,
        links: bool = False,
    ) -> None:
        self._console = console
        self.pager = SystemPager() if pager is None else pager
        self.styles = styles
        self.links = links

    def __enter__(self) -> "PagerContext":
        self._console._enter_buffer()
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        if exc_type is None:
            # [线程安全]
            # 使用锁确保在提取 buffer 时不会有其他线程干扰。
            with self._console._lock:
                buffer: List[Segment] = self._console._buffer[:]
                del self._console._buffer[:]
                segments: Iterable[Segment] = buffer
                if not self.styles:
                    segments = Segment.strip_styles(segments)
                elif not self.links:
                    segments = Segment.strip_links(segments)
                content = self._console._render_buffer(segments)
            self.pager.show(content)
        self._console._exit_buffer()


class ScreenContext:
    """[上下文管理器：备用屏幕]
    
    开启备用屏幕模式（类似 vim 或 top 的全屏模式）。
    
    原理：使用 ANSI 转义序列切换终端缓冲区。
    退出时必须恢复原状，否则用户的终端会“乱码”或看不到历史命令。
    """

    def __init__(
        self, console: "Console", hide_cursor: bool, style: StyleType = ""
    ) -> None:
        self.console = console
        self.hide_cursor = hide_cursor
        self.screen = Screen(style=style)
        self._changed = False

    def update(
        self, *renderables: RenderableType, style: Optional[StyleType] = None
    ) -> None:
        """Update the screen.

        Args:
            renderable (RenderableType, optional): Optional renderable to replace current renderable,
                or None for no change. Defaults to None.
            style: (Style, optional): Replacement style, or None for no change. Defaults to None.
        """
        if renderables:
            self.screen.renderable = (
                Group(*renderables) if len(renderables) > 1 else renderables[0]
            )
        if style is not None:
            self.screen.style = style
        self.console.print(self.screen, end="")

    def __enter__(self) -> "ScreenContext":
        self._changed = self.console.set_alt_screen(True)
        if self._changed and self.hide_cursor:
            self.console.show_cursor(False)
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        if self._changed:
            # [资源清理]
            # 无论是否发生异常，都要确保切回主屏幕并恢复光标。
            self.console.set_alt_screen(False)
            if self.hide_cursor:
                self.console.show_cursor(True)


class Group:
    """[设计模式：组合模式]
    
    将多个 Renderable 组合成一个大的 Renderable。
    这样，一个复杂的界面（包含表头、表格、进度条）可以被看作一个单一的对象进行渲染。
    """

    def __init__(self, *renderables: "RenderableType", fit: bool = True) -> None:
        self._renderables = renderables
        self.fit = fit
        self._render: Optional[List[RenderableType]] = None

    @property
    def renderables(self) -> List["RenderableType"]:
        if self._render is None:
            self._render = list(self._renderables)
        return self._render

    def __rich_measure__(
        self, console: "Console", options: "ConsoleOptions"
    ) -> "Measurement":
        """[尺寸测量协议]
        如果 fit=True，Group 的大小由内部元素的大小决定。
        如果 fit=False，Group 强行填满父容器提供的最大空间。
        """
        if self.fit:
            return measure_renderables(console, options, self.renderables)
        else:
            return Measurement(options.max_width, options.max_width)

    def __rich_console__(
        self, console: "Console", options: "ConsoleOptions"
    ) -> RenderResult:
        # [委托模式]
        # 简单地将渲染请求转发给内部的每一个 renderable。
        yield from self.renderables


def group(fit: bool = True) -> Callable[..., Callable[..., Group]]:
    """[装饰器工厂]
    
    这是一个高级装饰器，用于将一个生成 renderable 的函数转换为返回 Group 对象的函数。
    
    用途：简化代码，允许开发者写生成器函数来定义 UI 布局，而不需要手动构造 Group 对象。
    """
    def decorator(
        method: Callable[..., Iterable[RenderableType]],
    ) -> Callable[..., Group]:
        """Convert a method that returns an iterable of renderables in to a Group."""

        @wraps(method)
        def _replace(*args: Any, **kwargs: Any) -> Group:
            renderables = method(*args, **kwargs)
            return Group(*renderables, fit=fit)

        return _replace

    return decorator


def _is_jupyter() -> bool:  # pragma: no cover
    """[环境检测：运行环境识别]
    
    动态检测代码是否运行在 Jupyter Notebook 或 Google Colab 等环境中。
    
    实现原理：
    1. 尝试访问 `get_ipython` 这个全局变量（IPython 内核注入的）。
    2. 如果不存在，说明不是在 IPython 环境中运行。
    3. 如果存在，进一步检查 IPython Shell 的类名，区分是 Notebook 界面还是终端界面。
    """
    try:
        get_ipython  # type: ignore[name-defined]
    except NameError:
        return False
    ipython = get_ipython()  # type: ignore[name-defined]
    shell = ipython.__class__.__name__
    
    # [策略判断]
    # ZMQInteractiveShell 通常对应 Jupyter Notebook 或 Jupyter QtConsole。
    # google.colab 是 Colab 特有的判断。
    if (
        "google.colab" in str(ipython.__class__)
        or os.getenv("DATABRICKS_RUNTIME_VERSION")
        or shell == "ZMQInteractiveShell"
    ):
        return True  # Jupyter notebook or qtconsole
    elif shell == "TerminalInteractiveShell":
        return False  # Terminal running IPython
    else:
        return False  # Other type (?)


COLOR_SYSTEMS = {
    "standard": ColorSystem.STANDARD,
    "256": ColorSystem.EIGHT_BIT,
    "truecolor": ColorSystem.TRUECOLOR,
    "windows": ColorSystem.WINDOWS,
}

# [字典推导式]
# 反转 COLOR_SYSTEMS 字典，方便从枚举值反向查找字符串名称。
_COLOR_SYSTEMS_NAMES = {system: name for name, system in COLOR_SYSTEMS.items()}


@dataclass
class ConsoleThreadLocals(threading.local):
    """[设计模式：线程局部存储]
    
    继承自 `threading.local`，使得存储在其中的变量在每个线程中都有独立的副本。
    
    作用：
    Rich 的 Console 实例可能会在多线程环境中共享。
    如果不使用 TLS，多个线程同时调用 `print` 可能会互相干扰缓冲区或主题栈。
    通过 TLS，确保每个线程拥有独立的 `buffer`（输出缓冲）和 `theme_stack`（样式堆栈）。
    """

    theme_stack: ThemeStack
    # [默认工厂]
    # 使用 field(default_factory=list) 是为了避免所有线程共享同一个 list 对象。
    buffer: List[Segment] = field(default_factory=list)
    buffer_index: int = 0


class RenderHook(ABC):
    """[设计模式：观察者模式 / 钩子机制]
    
    定义了一个抽象接口，允许用户在渲染流程中插入自定义逻辑。
    
    应用场景：
    比如用户想要在每次渲染前统一修改某些内容，或者收集渲染统计信息，
    可以实现这个接口并注册到 Console 中。
    """

    @abstractmethod
    def process_renderables(
        self, renderables: List[ConsoleRenderable]
    ) -> List[ConsoleRenderable]:
        """Called with a list of objects to render.

        This method can return a new list of renderables, or modify and return the same list.

        Args:
            renderables (List[ConsoleRenderable]): A number of renderable objects.

        Returns:
            List[ConsoleRenderable]: A replacement list of renderables.
        """
        # [子类必须实现]
        pass


_windows_console_features: Optional["WindowsConsoleFeatures"] = None


def get_windows_console_features() -> "WindowsConsoleFeatures":  # pragma: no cover
    """[单例模式变种 / 延迟加载]
    
    使用模块级全局变量缓存 Windows 控制台特性。
    避免每次调用都去查询系统 API，提高性能。
    """
    global _windows_console_features
    if _windows_console_features is not None:
        return _windows_console_features
    from ._windows import get_windows_console_features

    _windows_console_features = get_windows_console_features()
    return _windows_console_features


def detect_legacy_windows() -> bool:
    """[环境检测：旧版 Windows 判断]
    
    判断是否运行在旧的 Windows 控制台（不支持 ANSI 转义序列）。
    旧版 Windows 需要特殊的 API 调用来设置颜色。
    """
    return WINDOWS and not get_windows_console_features().vt


class Console:
    """[核心类：Console]
    
    Rich 库的门面类，封装了所有终端交互的高级接口。
    
    设计特点：
    1. 参数高度可配置：支持自动检测或手动强制指定终端类型、颜色、尺寸等。
    2. 兼容性强：处理了 Windows、Jupyter、标准终端等多种环境差异。
    3. 依赖注入：允许注入文件对象、时间获取函数等，便于单元测试。
    """

    # [默认环境变量源]
    # 允许在测试时注入假的 _environ，实现环境隔离。
    _environ: Mapping[str, str] = os.environ

    def __init__(
        self,
        *,
        color_system: Optional[
            Literal["auto", "standard", "256", "truecolor", "windows"]
        ] = "auto",
        force_terminal: Optional[bool] = None,
        force_jupyter: Optional[bool] = None,
        force_interactive: Optional[bool] = None,
        soft_wrap: bool = False,
        theme: Optional[Theme] = None,
        stderr: bool = False,
        file: Optional[IO[str]] = None,
        quiet: bool = False,
        width: Optional[int] = None,
        height: Optional[int] = None,
        style: Optional[StyleType] = None,
        no_color: Optional[bool] = None,
        tab_size: int = 8,
        record: bool = False,
        markup: bool = True,
        emoji: bool = True,
        emoji_variant: Optional[EmojiVariant] = None,
        highlight: bool = True,
        log_time: bool = True,
        log_path: bool = True,
        log_time_format: Union[str, FormatTimeCallable] = "[%X]",
        highlighter: Optional["HighlighterType"] = ReprHighlighter(),
        legacy_windows: Optional[bool] = None,
        safe_box: bool = True,
        get_datetime: Optional[Callable[[], datetime]] = None,
        get_time: Optional[Callable[[], float]] = None,
        _environ: Optional[Mapping[str, str]] = None,
    ):
        # Copy of os.environ allows us to replace it for testing
        if _environ is not None:
            self._environ = _environ

        # [环境判断：Jupyter]
        # 如果没有强制指定，则自动检测。如果是 Jupyter，设置默认宽高。
        self.is_jupyter = _is_jupyter() if force_jupyter is None else force_jupyter
        if self.is_jupyter:
            if width is None:
                # [优先级：环境变量 > 代码常量]
                jupyter_columns = self._environ.get("JUPYTER_COLUMNS")
                if jupyter_columns is not None and jupyter_columns.isdigit():
                    width = int(jupyter_columns)
                else:
                    width = JUPYTER_DEFAULT_COLUMNS
            if height is None:
                jupyter_lines = self._environ.get("JUPYTER_LINES")
                if jupyter_lines is not None and jupyter_lines.isdigit():
                    height = int(jupyter_lines)
                else:
                    height = JUPYTER_DEFAULT_LINES

        self.tab_size = tab_size
        self.record = record
        self._markup = markup
        self._emoji = emoji
        self._emoji_variant: Optional[EmojiVariant] = emoji_variant
        self._highlight = highlight
        
        # [兼容性处理：Windows]
        # 自动检测是否为旧版 Windows，除非手动指定。
        self.legacy_windows: bool = (
            (detect_legacy_windows() and not self.is_jupyter)
            if legacy_windows is None
            else legacy_windows
        )

        if width is None:
            # [环境变量读取：COLUMNS]
            columns = self._environ.get("COLUMNS")
            if columns is not None and columns.isdigit():
                width = int(columns) - self.legacy_windows # 旧版 Windows 可能会导致边距问题
        if height is None:
            # [环境变量读取：LINES]
            lines = self._environ.get("LINES")
            if lines is not None and lines.isdigit():
                height = int(lines)

        self.soft_wrap = soft_wrap
        self._width = width
        self._height = height

        self._color_system: Optional[ColorSystem]

        self._force_terminal = None
        if force_terminal is not None:
            self._force_terminal = force_terminal

        self._file = file
        self.quiet = quiet
        self.stderr = stderr

        # [颜色系统初始化]
        if color_system is None:
            self._color_system = None
        elif color_system == "auto":
            self._color_system = self._detect_color_system()
        else:
            self._color_system = COLOR_SYSTEMS[color_system]

        # [并发控制]
        # 使用可重入锁 (RLock)，因为同一个线程可能会递归调用渲染方法。
        self._lock = threading.RLock()
        
        # [日志渲染器初始化]
        self._log_render = LogRender(
            show_time=log_time,
            show_path=log_path,
            time_format=log_time_format,
        )
        
        # [依赖注入：高亮器]
        # 允许自定义语法高亮逻辑。
        self.highlighter: HighlighterType = highlighter or _null_highlighter
        self.safe_box = safe_box
        
        # [依赖注入：时间获取函数]
        # 默认使用系统时间，但可以注入 Mock 时间用于测试。
        self.get_datetime = get_datetime or datetime.now
        self.get_time = get_time or monotonic
        
        self.style = style
        
        # [环境变量：NO_COLOR]
        # 遵循 NO_COLOR 标准 https://no-color.org/
        self.no_color = (
            no_color
            if no_color is not None
            else self._environ.get("NO_COLOR", "") != ""
        )
        
        # [交互模式判断]
        if force_interactive is None:
            tty_interactive = self._environ.get("TTY_INTERACTIVE", None)
            if tty_interactive is not None:
                if tty_interactive == "0":
                    force_interactive = False
                elif tty_interactive == "1":
                    force_interactive = True

        self.is_interactive = (
            (self.is_terminal and not self.is_dumb_terminal)
            if force_interactive is None
            else force_interactive
        )

        # [线程局部存储初始化]
        # 初始化每个线程独有的缓冲区和主题栈。
        self._record_buffer_lock = threading.RLock()
        self._thread_locals = ConsoleThreadLocals(
            theme_stack=ThemeStack(themes.DEFAULT if theme is None else theme)
        )
        self._record_buffer: List[Segment] = []
        self._render_hooks: List[RenderHook] = []
        self._live_stack: List[Live] = []
        self._is_alt_screen = False

    def __repr__(self) -> str:
        """[对象表示]
        提供简洁的对象描述，便于调试。
        """
        return f"<console width={self.width} {self._color_system!s}>"

    @property
    def file(self) -> IO[str]:
        """[属性：输出文件对象]
        
        逻辑：
        1. 如果显式指定了 file，使用它。
        2. 否则，根据 stderr 标志选择 sys.stderr 或 sys.stdout。
        3. 检查是否有 rich_proxied_file (用于代理输出，如捕获模式)。
        4. 最终兜底使用 NULL_FILE (丢弃所有输出)。
        """
        file = self._file or (sys.stderr if self.stderr else sys.stdout)
        file = getattr(file, "rich_proxied_file", file)
        if file is None:
            file = NULL_FILE
        return file

    @file.setter
    def file(self, new_file: IO[str]) -> None:
        """[属性设置器]
        允许动态修改输出目标。
        """
        self._file = new_file

    @property
    def _buffer(self) -> List[Segment]:
        """[属性：线程局部缓冲区]
        
        通过装饰器隐藏了线程局部变量的实现细节，
        外部使用时就像访问普通属性一样，但实际获取的是当前线程的 buffer。
        """
        return self._thread_locals.buffer

    @property
    def _buffer_index(self) -> int:
        """[属性：线程局部缓冲区索引]"""
        return self._thread_locals.buffer_index

    @_buffer_index.setter
    def _buffer_index(self, value: int) -> None:
        self._thread_locals.buffer_index = value

    @property
    def _theme_stack(self) -> ThemeStack:
        """[属性：线程局部主题栈]"""
        return self._thread_locals.theme_stack

    def _detect_color_system(self) -> Optional[ColorSystem]:
        """[算法：颜色系统探测]
        
        自动检测终端支持的颜色等级（标准16色、256色、真彩色）。
        
        检测优先级：
        1. Jupyter 环境 -> Truecolor
        2. 非终端或哑终端 -> None (无颜色)
        3. Windows -> 检查 API 支持 Truecolor 或 8-bit
        4. Linux/Mac -> 检查 COLORTERM 和 TERM 环境变量
        """
        if self.is_jupyter:
            return ColorSystem.TRUECOLOR
        if not self.is_terminal or self.is_dumb_terminal:
            return None
        if WINDOWS:  # pragma: no cover
            if self.legacy_windows:  # pragma: no cover
                return ColorSystem.WINDOWS
            windows_console_features = get_windows_console_features()
            return (
                ColorSystem.TRUECOLOR
                if windows_console_features.truecolor
                else ColorSystem.EIGHT_BIT
            )
        else:
            color_term = self._environ.get("COLORTERM", "").strip().lower()
            # COLORTERM=truecolor 或 24bit 是现代终端支持真彩色的标志
            if color_term in ("truecolor", "24bit"):
                return ColorSystem.TRUECOLOR
            term = self._environ.get("TERM", "").strip().lower()
            # 解析 TERM 变量，如 "xterm-256color"
            _term_name, _hyphen, colors = term.rpartition("-")
            color_system = _TERM_COLORS.get(colors, ColorSystem.STANDARD)
            return color_system

    def _enter_buffer(self) -> None:
        """[状态管理：进入缓冲模式]
        
        增加缓冲区索引。索引大于0意味着当前处于“捕获”或“分页”等不应立即输出的状态。
        """
        self._buffer_index += 1

    def _exit_buffer(self) -> None:
        """[状态管理：退出缓冲模式]
        
        减少索引，并触发缓冲区内容的检查和渲染。
        """
        self._buffer_index -= 1
        self._check_buffer()

    def set_live(self, live: "Live") -> bool:
        """[状态管理：设置 Live 显示]
        
        用于 Live 上下文管理器。实现了一个栈结构，支持 Live 嵌套（虽然通常不推荐）。
        
        Returns:
            Boolean: 如果是栈底（第一个 Live），返回 True，表示需要初始化。
        """
        with self._lock:
            self._live_stack.append(live)
            return len(self._live_stack) == 1

    def clear_live(self) -> None:
        """[状态管理：清除 Live 显示]"""
        with self._lock:
            self._live_stack.pop()

    def push_render_hook(self, hook: RenderHook) -> None:
        """[扩展点：注册渲染钩子]
        
        将自定义的渲染逻辑推入栈中。渲染时会依次调用栈中的钩子。
        """
        with self._lock:
            self._render_hooks.append(hook)

    def pop_render_hook(self) -> None:
        """[扩展点：移除渲染钩子]"""
        with self._lock:
            self._render_hooks.pop()

    def __enter__(self) -> "Console":
        """[上下文管理器协议]
        
        允许使用 `with Console() as console:` 语法。
        作用是开启缓冲模式，确保 `with` 块内的输出可以被捕获或统一处理。
        """
        self._enter_buffer()
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        """[上下文管理器协议]
        
        退出时结束缓冲模式，渲染内容。
        """
        self._exit_buffer()

    def begin_capture(self) -> None:
        """[功能：开始捕获]
        
        手动开启捕获模式，通常配合 `end_capture` 使用。
        """
        self._enter_buffer()

    def end_capture(self) -> str:
        """[功能：结束捕获并获取结果]
        
        Returns:
            str: 渲染后的字符串。
        """
        render_result = self._render_buffer(self._buffer)
        del self._buffer[:]
        self._exit_buffer()
        return render_result

    def push_theme(self, theme: Theme, *, inherit: bool = True) -> None:
        """[状态管理：压入主题]
        
        将新主题压入栈顶。后续的渲染将使用新主题的样式。
        
        Args:
            inherit: 如果为 True，新主题将继承旧主题的未定义样式；否则完全覆盖。
        """
        self._theme_stack.push_theme(theme, inherit=inherit)

    def pop_theme(self) -> None:
        """[状态管理：弹出主题]"""
        self._theme_stack.pop_theme()

    def use_theme(self, theme: Theme, *, inherit: bool = True) -> ThemeContext:
        """[设计模式：上下文管理器工厂]
        
        返回一个 ThemeContext 对象，支持 `with` 语法临时切换主题。
        这比手动调用 push/pop 更安全，因为它保证了 `__exit__` 时一定会 pop。
        
        示例：
            with console.use_theme(some_theme):
                console.print("Styled with some_theme")
            # 这里自动恢复原主题
        """
        return ThemeContext(self, theme, inherit)

    @property
    def color_system(self) -> Optional[str]:
        """[属性：颜色系统名称]
        
        将内部枚举值转换为外部可读的字符串。
        """
        if self._color_system is not None:
            return _COLOR_SYSTEMS_NAMES[self._color_system]
        else:
            return None

    @property
    def encoding(self) -> str:
        """[属性：编码格式]
        
        动态获取当前输出文件的编码，默认为 utf-8。
        """
        return (getattr(self.file, "encoding", "utf-8") or "utf-8").lower()


    @property
    def is_terminal(self) -> bool:
        """Check if the console is writing to a terminal.

        Returns:
            bool: True if the console writing to a device capable of
                understanding escape sequences, otherwise False.
        """
        # [优先级 1：开发者强制指定]
        # 如果在初始化时显式设置了 force_terminal，则直接使用，忽略所有检测。
        if self._force_terminal is not None:
            return self._force_terminal

        # [兼容性处理：Python IDLE]
        # IDLE 环境 stdin 模块名以 idlelib 开头。
        # 虽然 IDLE 有时会被误判为 TTY，但它不支持 ANSI 转义序列，必须强制返回 False。
        if hasattr(sys.stdin, "__module__") and sys.stdin.__module__.startswith(
            "idlelib"
        ):
            return False

        # [优先级 2：Jupyter 环境]
        # Jupyter 环境通常不是通过直接输出 ANSI 码渲染的（它有自己的渲染协议），所以返回 False。
        if self.is_jupyter:
            return False

        environ = self._environ

        # [环境变量检测：TTY_COMPATIBLE]
        # 允许用户通过环境变量显式告诉 Rich 当前是否兼容 TTY。
        tty_compatible = environ.get("TTY_COMPATIBLE", "")
        if tty_compatible == "0":
            return False
        if tty_compatible == "1":
            return True

        # [标准检测：FORCE_COLOR]
        # 遵循 force-color.org 标准。如果设置了该环境变量，通常意味着强制启用颜色。
        force_color = environ.get("FORCE_COLOR")
        if force_color is not None:
            return force_color != ""

        # [优先级 3：系统自动检测]
        # 调用文件对象的 isatty() 方法。这是判断输出是否指向终端（非文件/管道）的最标准方法。
        isatty: Optional[Callable[[], bool]] = getattr(self.file, "isatty", None)
        try:
            return False if isatty is None else isatty()
        except ValueError:
            # [异常处理]
            # 在某些边缘情况（如 pytest 结束时，文件描述符已关闭），isatty() 可能抛出 ValueError。
            # 此时视为非终端环境。
            return False

    @property
    def is_dumb_terminal(self) -> bool:
        """Detect dumb terminal.

        Returns:
            bool: True if writing to a dumb terminal, otherwise False.

        """
        # [环境变量检测：TERM]
        # 检查 TERM 环境变量是否为 "dumb" 或 "unknown"。
        # Dumb terminal 指的是那些不支持任何光标移动、颜色清除等高级功能的终端。
        _term = self._environ.get("TERM", "")
        is_dumb = _term.lower() in ("dumb", "unknown")
        return self.is_terminal and is_dumb

    @property
    def options(self) -> ConsoleOptions:
        """[属性：渲染配置快照]
        
        获取基于当前 Console 状态的渲染配置对象。
        该对象是不可变的（或者说是当前状态的快照），传递给渲染逻辑使用。
        """
        size = self.size
        return ConsoleOptions(
            max_height=size.height,
            size=size,
            legacy_windows=self.legacy_windows,
            min_width=1,
            max_width=size.width,
            encoding=self.encoding,
            is_terminal=self.is_terminal,
        )

    @property
    def size(self) -> ConsoleDimensions:
        """[核心算法：尺寸获取策略]
        
        智能获取终端的宽和高，具有多层回退机制。
        
        策略顺序：
        1. 显式设置 (_width, _height)
        2. 环境变量 (COLUMNS, LINES)
        3. 系统调用 (os.get_terminal_size)
        4. 硬编码默认值 (80x25)
        """

        # 1. 检查是否已显式设置尺寸
        if self._width is not None and self._height is not None:
            # [兼容性修正]
            # 旧版 Windows 可能在边缘绘制字符，所以宽度需要减去 1。
            return ConsoleDimensions(self._width - self.legacy_windows, self._height)

        # 2. 针对哑终端的默认值
        if self.is_dumb_terminal:
            return ConsoleDimensions(80, 25)

        width: Optional[int] = None
        height: Optional[int] = None

        # 3. 系统调用获取尺寸
        # Windows 只需要检查标准输出/错误，Linux/Mac 通常需要检查标准输入。
        streams = _STD_STREAMS_OUTPUT if WINDOWS else _STD_STREAMS
        for file_descriptor in streams:
            try:
                # os.get_terminal_size 会查询内核的终端窗口大小
                width, height = os.get_terminal_size(file_descriptor)
            except (AttributeError, ValueError, OSError):  # Probably not a terminal
                pass
            else:
                break

        # 4. 环境变量覆盖（优先级高于系统调用）
        columns = self._environ.get("COLUMNS")
        if columns is not None and columns.isdigit():
            width = int(columns)
        lines = self._environ.get("LINES")
        if lines is not None and lines.isdigit():
            height = int(lines)

        # 5. 最终兜底默认值
        # get_terminal_size 在伪终端下可能返回 (0, 0)，需要兜底。
        width = width or 80
        height = height or 25
        return ConsoleDimensions(
            width - self.legacy_windows if self._width is None else self._width,
            height if self._height is None else self._height,
        )

    @size.setter
    def size(self, new_size: Tuple[int, int]) -> None:
        """Set a new size for the terminal.

        Args:
            new_size (Tuple[int, int]): New width and height.
        """
        width, height = new_size
        self._width = width
        self._height = height

    @property
    def width(self) -> int:
        """Get the width of the console.

        Returns:
            int: The width (in characters) of the console.
        """
        return self.size.width

    @width.setter
    def width(self, width: int) -> None:
        """Set width.

        Args:
            width (int): New width.
        """
        self._width = width

    @property
    def height(self) -> int:
        """Get the height of the console.

        Returns:
            int: The height (in lines) of the console.
        """
        return self.size.height

    @height.setter
    def height(self, height: int) -> None:
        """Set height.

        Args:
            height (int): new height.
        """
        self._height = height

    def bell(self) -> None:
        """Play a 'bell' sound (if supported by the terminal).
        
        发送响铃控制字符 (\a)。
        """
        self.control(Control.bell())

    def capture(self) -> Capture:
        """[上下文管理器工厂：输出捕获]
        
        创建一个上下文管理器，用于拦截 print() 或 log() 的输出，将其转换为字符串而不是写到屏幕。
        
        应用场景：单元测试、生成日志文本。
        
        Example:
            >>> with console.capture() as capture:
            ...     console.print("Hello")
            >>> text = capture.get()
        """
        capture = Capture(self)
        return capture

    def pager(
        self, pager: Optional[Pager] = None, styles: bool = False, links: bool = False
    ) -> PagerContext:
        """[上下文管理器工厂：分页器]
        
        将输出内容通过系统分页器（如 less, more）显示。
        当内容很长，超过一屏时非常有用。
        
        Args:
            pager: 自定义分页器对象，默认使用系统分页器。
            styles: 是否在分页器中显示颜色样式（有些分页器不支持 ANSI 颜色）。
            links: 是否显示链接。
        """
        return PagerContext(self, pager=pager, styles=styles, links=links)

    def line(self, count: int = 1) -> None:
        """Write new line(s).

        Args:
            count (int, optional): Number of new lines. Defaults to 1.
        """
        assert count >= 0, "count must be >= 0"
        # [复用组件] 通过渲染 NewLine 对象来实现换行
        self.print(NewLine(count))

    def clear(self, home: bool = True) -> None:
        """Clear the screen.

        Args:
            home (bool, optional): Also move the cursor to 'home' position (top-left). Defaults to True.
        """
        if home:
            # [控制序列] 发送清屏并移动光标到左上角的指令
            self.control(Control.clear(), Control.home())
        else:
            self.control(Control.clear())

    def status(
        self,
        status: RenderableType,
        *,
        spinner: str = "dots",
        spinner_style: StyleType = "status.spinner",
        speed: float = 1.0,
        refresh_per_second: float = 12.5,
    ) -> "Status":
        """[UI 组件：状态指示器]
        
        创建一个带有旋转动画的状态栏。通常用于长时间任务（如下载、处理）的反馈。
        
        Returns:
            Status: 返回的 Status 对象可以用作上下文管理器，任务结束自动清除。
        """
        from .status import Status

        status_renderable = Status(
            status,
            console=self,
            spinner=spinner,
            spinner_style=spinner_style,
            speed=speed,
            refresh_per_second=refresh_per_second,
        )
        return status_renderable

    def show_cursor(self, show: bool = True) -> bool:
        """Show or hide the cursor.
        
        [UI 控制] 在全屏应用或动画显示期间，通常需要隐藏光标以避免闪烁干扰。
        """
        if self.is_terminal:
            self.control(Control.show_cursor(show))
            return True
        return False

    def set_alt_screen(self, enable: bool = True) -> bool:
        """[终端控制：备用屏幕模式]
        
        开启备用屏幕缓冲区。
        这类似于 Vim 或 top 命令运行时的效果：原有屏幕内容被保存，显示新的全屏内容。
        退出时，原有内容会恢复。
        
        Args:
            enable: True 开启，False 关闭（恢复原屏幕）。
            
        Returns:
            bool: 是否成功写入控制码。
        """
        changed = False
        if self.is_terminal and not self.legacy_windows:
            self.control(Control.alt_screen(enable))
            changed = True
            self._is_alt_screen = enable
        return changed

    @property
    def is_alt_screen(self) -> bool:
        """Check if the alt screen was enabled."""
        return self._is_alt_screen

    def set_window_title(self, title: str) -> bool:
        """[终端控制：设置窗口标题]
        
        修改终端窗口的标题栏文字。
        注意：不是所有终端都支持此功能，且某些 Shell（如 fish）会自动重置标题。
        """
        if self.is_terminal:
            self.control(Control.title(title))
            return True
        return False

    def screen(
        self, hide_cursor: bool = True, style: Optional[StyleType] = None
    ) -> "ScreenContext":
        """[上下文管理器工厂：全屏模式]
        
        返回一个上下文管理器，进入时开启备用屏幕，退出时自动恢复。
        比直接调用 set_alt_screen 更安全，因为它利用了 Python 的 with 语句保证清理。
        
        Returns:
            ~ScreenContext: Context which enables alternate screen on enter, and disables it on exit.
        """
        return ScreenContext(self, hide_cursor=hide_cursor, style=style or "")

    def measure(
        self, renderable: RenderableType, *, options: Optional[ConsoleOptions] = None
    ) -> Measurement:
        """[布局算法：测量]
        
        测量一个对象渲染出来需要多少宽度（最小/最大）。
        这对于动态布局（比如表格自动调整列宽）至关重要。
        
        Returns:
            Measurement: 包含 minimum 和 maximum 宽度的对象。
        """
        measurement = Measurement.get(self, options or self.options, renderable)
        return measurement

    def render(
        self, renderable: RenderableType, options: Optional[ConsoleOptions] = None
    ) -> Iterable[Segment]:
        """[核心引擎：渲染器]
        
        这是 Rich 最核心的方法，负责将任意对象（实现了 __rich_console__ 或字符串）
        转换为终端可绘制的 Segment（文本片段+样式）流。
        
        逻辑流程：
        1. 检查宽度是否合法，防止无限递归。
        2. 尝试将对象转换为 Rich 内部对象 (rich_cast)。
        3. 检查对象是否实现了 __rich_console__ 协议。
        4. 如果是字符串，将其转换为 Text 对象。
        5. 递归渲染：如果对象返回的不是 Segment，而是另一个 Renderable，则递归调用 render。
        """

        _options = options or self.options
        # [防护性编程]
        # 如果最大宽度小于 1，说明没有空间渲染，直接返回空迭代器，防止后续逻辑出错。
        if _options.max_width < 1:
            return
        render_iterable: RenderResult

        # [协议适配：Rich Cast]
        # 尝试将普通对象转换为可渲染对象。
        renderable = rich_cast(renderable)
        
        # [分支 1：实现了 __rich_console__ 协议的对象]
        # 使用 isinstance 检查是因为 renderable 可能是类本身（未实例化），类通常没有渲染逻辑（除非是静态方法）。
        if hasattr(renderable, "__rich_console__") and not isclass(renderable):
            render_iterable = renderable.__rich_console__(self, _options)
        # [分支 2：字符串]
        elif isinstance(renderable, str):
            # 字符串需要先经过 render_str 处理（解析标签代码、高亮等）
            text_renderable = self.render_str(
                renderable, highlight=_options.highlight, markup=_options.markup
            )
            render_iterable = text_renderable.__rich_console__(self, _options)
        else:
            # [分支 3：无法识别的对象]
            raise errors.NotRenderableError(
                f"Unable to render {renderable!r}; "
                "A str, Segment or object with __rich_console__ method is required"
            )

        try:
            iter_render = iter(render_iterable)
        except TypeError:
            raise errors.NotRenderableError(
                f"object {render_iter!r} is not renderable"
            )
        _Segment = Segment
        # [状态重置]
        # 每次开始新一轮渲染时，重置高度限制，防止嵌套渲染时高度被无限累积。
        _options = _options.reset_height()
        
        # [递归生成器逻辑]
        for render_output in iter_render:
            # 情况 A：输出已经是最终的 Segment，直接 yield
            if isinstance(render_output, _Segment):
                yield render_output
            # 情况 B：输出还是 Renderable（嵌套组件），递归调用 render
            # 这允许复杂的组件（如表格）包含简单的组件（如文本）或另一个表格
            else:
                yield from self.render(render_output, _options)

        def render_lines(
        self,
        renderable: RenderableType,
        options: Optional[ConsoleOptions] = None,
        *,
        style: Optional[Style] = None,
        pad: bool = True,
        new_lines: bool = False,
    ) -> List[List[Segment]]:
        #[核心算法：渲染行生成器]
        
        #将任意可渲染对象转换为“二维列表”：List[List[Segment]]。
        #这个二维结构直接对应终端屏幕的布局（外层是行，内层是该行的片段）。
        
        #应用场景：
        #Panel（面板）、Table（表格）等需要预先知道内容精确布局的组件，会调用此方法获取内容后再绘制边框。
       
         with self._lock:
            render_options = options or self.options
            # 1. 调用核心 render 方法生成 Segment 流
            _rendered = self.render(renderable, render_options)
            
            # 2. 应用全局样式（如果指定）
            if style:
                _rendered = Segment.apply_style(_rendered, style)

            render_height = render_options.height
            if render_height is not None:
                render_height = max(0, render_height)

            # 3. [关键步骤：分段与裁剪]
            # Segment.split_and_crop_lines 将扁平的 Segment 流切分成行，并处理换行、溢出裁剪。
            # islice 用于限制输出的高度。
            lines = list(
                islice(
                    Segment.split_and_crop_lines(
                        _rendered,
                        render_options.max_width,
                        include_new_lines=new_lines,
                        pad=pad, # 是否在行尾填充空格
                        style=style,
                    ),
                    None,
                    render_height,
                )
            )
            
            # 4. [填充处理]
            # 如果指定了固定高度，且实际行数不足，需要填充空行。
            if render_options.height is not None:
                extra_lines = render_options.height - len(lines)
                if extra_lines > 0:
                    # 构造一个充满空格的行
                    pad_line = [
                        (
                            [
                                Segment(" " * render_options.max_width, style),
                                Segment("\n"), # 根据 new_lines 参数决定是否加换行符
                            ]
                            if new_lines
                            else [Segment(" " * render_options.max_width, style)]
                        )
                    ]
                    lines.extend(pad_line * extra_lines)

            return lines

    def render_str(
        self,
        text: str,
        *,
        style: Union[str, Style] = "",
        justify: Optional[JustifyMethod] = None,
        overflow: Optional[OverflowMethod] = None,
        emoji: Optional[bool] = None,
        markup: Optional[bool] = None,
        highlight: Optional[bool] = None,
        highlighter: Optional[HighlighterType] = None,
    ) -> "Text":
        """[工厂方法：字符串标准化]
        
        将普通 Python 字符串转换为 Rich 内部的 `Text` 对象。
        这是连接用户输入和 Rich 渲染引擎的桥梁。
        """
        # [参数默认值处理]
        # 如果参数为 None，则继承 Console 实例的默认配置。
        emoji_enabled = emoji or (emoji is None and self._emoji)
        markup_enabled = markup or (markup is None and self._markup)
        highlight_enabled = highlight or (highlight is None and self._highlight)

        if markup_enabled:
            # [路径 A：解析 Markup 标签]
            # 如果启用了 markup，解析 [bold]text[/] 类似的标签。
            rich_text = render_markup(
                text,
                style=style,
                emoji=emoji_enabled,
                emoji_variant=self._emoji_variant,
            )
            rich_text.justify = justify
            rich_text.overflow = overflow
        else:
            # [路径 B：纯文本处理]
            # 仅处理 Emoji 替换，不解析标签。
            rich_text = Text(
                (
                    _emoji_replace(text, default_variant=self._emoji_variant)
                    if emoji_enabled
                    else text
                ),
                justify=justify,
                overflow=overflow,
                style=style,
            )

        # [高亮处理]
        # 如果启用了高亮，使用指定的 highlighter（如 ReprHighlighter）处理文本。
        _highlighter = (highlighter or self.highlighter) if highlight_enabled else None
        if _highlighter is not None:
            highlight_text = _highlighter(str(rich_text))
            highlight_text.copy_styles(rich_text) # 保留原有样式，只覆盖高亮部分
            return highlight_text

        return rich_text

    def get_style(
        self, name: Union[str, Style], *, default: Optional[Union[Style, str]] = None
    ) -> Style:
        """[服务：样式解析器]
        
        根据名称或定义字符串获取 Style 对象。
        它是 Theme（主题）系统的对外接口。
        """
        if isinstance(name, Style):
            return name

        try:
            # 1. 优先从主题栈中查找命名的样式
            style = self._theme_stack.get(name)
            if style is None:
                # 2. 如果主题中没找到，尝试解析为内联样式定义（如 "bold red"）
                style = Style.parse(name)
            return style.copy() if style.link else style
        except errors.StyleSyntaxError as error:
            # 3. 异常回退：如果解析失败且有默认值，尝试解析默认值
            if default is not None:
                return self.get_style(default)
            raise errors.MissingStyle(
                f"Failed to get style {name!r}; {error}"
            ) from None

    def _collect_renderables(
        self,
        objects: Iterable[Any],
        sep: str,
        end: str,
        *,
        justify: Optional[JustifyMethod] = None,
        emoji: Optional[bool] = None,
        markup: Optional[bool] = None,
        highlight: Optional[bool] = None,
    ) -> List[ConsoleRenderable]:
        """[预处理：参数归一化与分组]
        
        将 `print()` 接收到的任意参数列表转换为统一的 `ConsoleRenderable` 列表。
        
        关键逻辑：
        1. 字符串会被转换并**批量合并**（应用 sep 分隔符）。
        2. 非字符串对象（如 Table）会被独立处理。
        3. 这种分离策略避免了将大对象（如 Table）错误地转换为字符串。
        """
        renderables: List[ConsoleRenderable] = []
        _append = renderables.append
        text: List[Text] = []
        append_text = text.append

        append = _append
        # [对齐处理包装]
        if justify in ("left", "center", "right"):
            def align_append(renderable: RenderableType) -> None:
                _append(Align(renderable, cast(AlignMethod, justify)))
            append = align_append

        _highlighter: HighlighterType = _null_highlighter
        if highlight or (highlight is None and self._highlight):
            _highlighter = self.highlighter

        # [辅助函数：将积攒的文本合并并添加到输出列表]
        def check_text() -> None:
            if text:
                sep_text = Text(sep, justify=justify, end=end)
                append(sep_text.join(text))
                text.clear()

        for renderable in objects:
            renderable = rich_cast(renderable)
            if isinstance(renderable, str):
                # [类型：字符串] -> 转换为 Text 并加入待合并列表
                append_text(
                    self.render_str(
                        renderable,
                        emoji=emoji,
                        markup=markup,
                        highlight=highlight,
                        highlighter=_highlighter,
                    )
                )
            elif isinstance(renderable, Text):
                # [类型：Text] -> 加入待合并列表
                append_text(renderable)
            elif isinstance(renderable, ConsoleRenderable):
                # [类型：Renderable] -> 先清空之前的文本缓存，再加入该对象
                check_text()
                append(renderable)
            elif is_expandable(renderable):
                # [类型：可展开对象] (如字典, 列表) -> 使用 Pretty 打印
                check_text()
                append(Pretty(renderable, highlighter=_highlighter))
            else:
                # [类型：其他] -> 转字符串并加入待合并列表
                append_text(_highlighter(str(renderable)))

        # [收尾]：循环结束后，处理最后剩余的文本
        check_text()

        # [全局样式应用]
        if self.style is not None:
            style = self.get_style(self.style)
            renderables = [Styled(renderable, style) for renderable in renderables]

        return renderables

    def rule(
        self,
        title: TextType = "",
        *,
        characters: str = "─",
        style: Union[str, Style] = "rule.line",
        align: AlignMethod = "center",
    ) -> None:
        """[UI 组件：分割线]
        
        绘制一条水平分割线，并可选择在中间显示标题。
        """
        from .rule import Rule

        rule = Rule(title=title, characters=characters, style=style, align=align)
        self.print(rule)

    def control(self, *control: Control) -> None:
        """[底层控制：非打印字符注入]
        
        直接向缓冲区写入控制序列（如移动光标、清屏），不经过正常的渲染流程。
        这主要用于低级的状态变更。
        """
        if not self.is_dumb_terminal:
            with self:
                # 提取 Control 对象中的 Segment 并写入缓冲区
                self._buffer.extend(_control.segment for _control in control)

    def out(
        self,
        *objects: Any,
        sep: str = " ",
        end: str = "\n",
        style: Optional[Union[str, Style]] = None,
        highlight: Optional[bool] = None,
    ) -> None:
        """[低级输出：原始打印]
        
        与 `print` 不同，此方法不会自动换行、不会自动折行、不会解析 Markup。
        它只是简单地连接字符串并可选地应用高亮。
        
        相当于 Rich 版本的 `sys.stdout.write`。
        """
        raw_output: str = sep.join(str(_object) for _object in objects)
        self.print(
            raw_output,
            style=style,
            highlight=highlight,
            emoji=False, # 强制关闭 emoji
            markup=False, # 强制关闭 markup
            no_wrap=True, # 强制不换行
            overflow="ignore", # 忽略溢出
            crop=False,
            end=end,
        )

    def print(
        self,
        *objects: Any,
        sep: str = " ",
        end: str = "\n",
        style: Optional[Union[str, Style]] = None,
        justify: Optional[JustifyMethod] = None,
        overflow: Optional[OverflowMethod] = None,
        no_wrap: Optional[bool] = None,
        emoji: Optional[bool] = None,
        markup: Optional[bool] = None,
        highlight: Optional[bool] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        crop: bool = True,
        soft_wrap: Optional[bool] = None,
        new_line_start: bool = False,
    ) -> None:
        """[主入口：打印方法]
        
        这是用户最常用的方法。它编排了从参数收集到最终缓冲区写入的全过程。
        
        流程：
        1. 参数预处理与默认值覆盖。
        2. 进入渲染上下文（加锁，处理缓冲区）。
        3. 收集并转换 Renderables。
        4. 执行 Render Hooks（渲染钩子）。
        5. 更新渲染选项。
        6. 循环渲染每个对象为 Segment。
        7. 写入缓冲区。
        """
        if not objects:
            objects = (NewLine(),)

        # [Soft Wrap 模式处理]
        # Soft wrap 意味着终端自己处理换行，Rich 不插入硬换行符。
        if soft_wrap is None:
            soft_wrap = self.soft_wrap
        if soft_wrap:
            if no_wrap is None:
                no_wrap = True
            if overflow is None:
                overflow = "ignore"
            crop = False
            
        # [快照] 复制钩子列表，防止迭代过程中被修改
        render_hooks = self._render_hooks[:]
        
        with self:
            # 1. 收集和归一化对象
            renderables = self._collect_renderables(
                objects,
                sep,
                end,
                justify=justify,
                emoji=emoji,
                markup=markup,
                highlight=highlight,
            )
            
            # 2. 执行渲染钩子（允许外部插件修改即将渲染的内容）
            for hook in render_hooks:
                renderables = hook.process_renderables(renderables)
                
            # 3. 准备渲染选项（更新宽高等参数）
            render_options = self.options.update(
                justify=justify,
                overflow=overflow,
                width=min(width, self.width) if width is not None else NO_CHANGE,
                height=height,
                no_wrap=no_wrap,
                markup=markup,
                highlight=highlight,
            )

            new_segments: List[Segment] = []
            extend = new_segments.extend
            render = self.render
            
            # 4. 渲染循环
            # 将每个 Renderable 转换为 Segment 流
            if style is None:
                for renderable in renderables:
                    extend(render(renderable, render_options))
            else:
                # 如果指定了全局样式，应用到所有 segment 上
                for renderable in renderables:
                    extend(
                        Segment.apply_style(
                            render(renderable, render_options), self.get_style(style)
                        )
                    )
            
            # 5. [自动换行前缀]
            # 如果内容包含多行，且要求 new_line_start，则在开头插入一个换行符
            if new_line_start:
                if (
                    len("".join(segment.text for segment in new_segments).splitlines())
                    > 1
                ):
                    new_segments.insert(0, Segment.line())
            
            # 6. 写入缓冲区
            if crop:
                # [模式：裁剪] 使用 split_and_crop_lines 将 segment 转换为行并裁剪超出宽度的部分
                buffer_extend = self._buffer.extend
                for line in Segment.split_and_crop_lines(
                    new_segments, self.width, pad=False
                ):
                    buffer_extend(line)
            else:
                # [模式：不裁剪] 直接将 Segment 流写入缓冲区
                self._buffer.extend(new_segments)

    def print_json(
        self,
        json: Optional[str] = None,
        *,
        data: Any = None,
        indent: Union[None, int, str] = 2,
        highlight: bool = True,
        skip_keys: bool = False,
        ensure_ascii: bool = False,
        check_circular: bool = True,
        allow_nan: bool = True,
        default: Optional[Callable[[Any], Any]] = None,
        sort_keys: bool = False,
    ) -> None:
        """[便捷方法：JSON 美化打印]
        
        专门用于将 JSON 数据或 Python 对象转换为带语法高亮、易读的 JSON 格式输出。
        底层使用了 rich.json.JSON 渲染器。
        """
        from rich.json import JSON

        if json is None:
            # [路径 A：从对象生成]
            json_renderable = JSON.from_data(
                data,
                indent=indent,
                highlight=highlight,
                skip_keys=skip_keys,
                ensure_ascii=ensure_ascii,
                check_circular=check_circular,
                allow_nan=allow_nan,
                default=default,
                sort_keys=sort_keys,
            )
        else:
            # [路径 B：从字符串解析]
            if not isinstance(json, str):
                raise TypeError(
                    f"json must be str. Did you mean print_json(data={json!r}) ?"
                )
            json_renderable = JSON(
                json,
                indent=indent,
                highlight=highlight,
                skip_keys=skip_keys,
                ensure_ascii=ensure_ascii,
                check_circular=check_circular,
                allow_nan=allow_nan,
                default=default,
                sort_keys=sort_keys,
            )
        # JSON 通常比较长，推荐使用 soft_wrap
        self.print(json_renderable, soft_wrap=True)

    def update_screen(
        self,
        renderable: RenderableType,
        *,
        region: Optional[Region] = None,
        options: Optional[ConsoleOptions] = None,
    ) -> None:
        """[TUI 核心方法：局部屏幕刷新]
        
        仅更新屏幕的特定区域，而不是重绘整个屏幕。
        这对于制作高性能的终端用户界面（TUI）至关重要。
        
        Args:
            region: 指定更新的矩形区域。
            
        Raises:
            errors.NoAltScreen: 如果不在备用屏幕模式下，不允许调用此方法。
        """
        if not self.is_alt_screen:
            raise errors.NoAltScreen("Alt screen must be enabled to call update_screen")
        render_options = options or self.options
        if region is None:
            # [全屏更新]
            x = y = 0
            render_options = render_options.update_dimensions(
                render_options.max_width, render_options.height or self.height
            )
        else:
            # [局部更新]
            x, y, width, height = region
            render_options = render_options.update_dimensions(width, height)

        # 1. 渲染为行
        lines = self.render_lines(renderable, options=render_options)
        # 2. 将行写到指定坐标
        self.update_screen_lines(lines, x, y)


    def update_screen_lines(
        self, lines: List[List[Segment]], x: int = 0, y: int = 0
    ) -> None:
        """[TUI 核心方法：局部刷新]
        
        将渲染好的行直接更新到屏幕的指定位置，而不重绘整个屏幕。
        这对于高性能的终端界面（如进度条、全屏应用）至关重要，可以减少闪烁。
        
        实现原理：
        1. 创建一个 ScreenUpdate 对象（包含移动光标和内容的指令）。
        2. 将其渲染为 Segment 流。
        3. 直接写入缓冲区并立即刷新。
        """
        if not self.is_alt_screen:
            raise errors.NoAltScreen("Alt screen must be enabled to call update_screen")
        # [封装] 将行列表和坐标封装为可渲染对象
        screen_update = ScreenUpdate(lines, x, y)
        segments = self.render(screen_update)
        self._buffer.extend(segments)
        # [立即刷新] 确保显示立即生效，不等待缓冲区满
        self._check_buffer()

    def print_exception(
        self,
        *,
        width: Optional[int] = 100,
        extra_lines: int = 3,
        theme: Optional[str] = None,
        word_wrap: bool = False,
        show_locals: bool = False,
        suppress: Iterable[Union[str, ModuleType]] = (),
        max_frames: int = 100,
    ) -> None:
        """[工具方法：异常美化]
        
        自动捕获当前的异常堆栈信息，并使用 Rich 的 Traceback 组件进行彩色渲染。
        极大地提升了调试体验，比黑白回溯易读得多。
        """
        from .traceback import Traceback

        traceback = Traceback(
            width=width,
            extra_lines=extra_lines,
            theme=theme,
            word_wrap=word_wrap,
            show_locals=show_locals,
            suppress=suppress,
            max_frames=max_frames,
        )
        self.print(traceback)

    @staticmethod
    def _caller_frame_info(
        offset: int,
        currentframe: Callable[[], Optional[FrameType]] = inspect.currentframe,
    ) -> Tuple[str, int, Dict[str, Any]]:
        """[反射工具：获取调用者信息]
        
        这是一个静态方法，用于向上遍历调用栈，获取调用 `log` 方法的代码位置。
        
        Args:
            offset: 栈偏移量。例如 offset=1 表示上一级（调用 log 的地方）。
            currentframe: 注入依赖，默认使用 inspect.currentframe。
                        允许在测试时 Mock 这个函数，避免实际操作栈帧。
                        
        Returns:
            (文件名, 行号, 局部变量字典)
        """
        # 忽略本 helper 函数的一帧
        offset += 1

        frame = currentframe()
        if frame is not None:
            # [路径 A：高性能栈遍历]
            # 直接操作 frame 对象（f_back）比 inspect.stack() 快得多。
            while offset and frame is not None:
                frame = frame.f_back
                offset -= 1
            assert frame is not None
            return frame.f_code.co_filename, frame.f_lineno, frame.f_locals
        else:
            # [路径 B：兼容性回退]
            # 某些实现（如 PyPy 或某些优化环境）可能不支持 currentframe，回退到 inspect.stack()。
            frame_info = inspect.stack()[offset]
            return frame_info.filename, frame_info.lineno, frame_info.frame.f_locals

    def log(
        self,
        *objects: Any,
        sep: str = " ",
        end: str = "\n",
        style: Optional[Union[str, Style]] = None,
        justify: Optional[JustifyMethod] = None,
        emoji: Optional[bool] = None,
        markup: Optional[bool] = None,
        highlight: Optional[bool] = None,
        log_locals: bool = False,
        _stack_offset: int = 1,
    ) -> None:
        """[功能：增强型日志]
        
        类似于 `print`，但会自动添加时间戳、文件路径和行号。
        这是 Rich 区别于普通 print 的重要功能。
        """
        if not objects:
            objects = (NewLine(),)

        render_hooks = self._render_hooks[:]

        with self:
            # 1. 收集可渲染对象
            renderables = self._collect_renderables(
                objects,
                sep,
                end,
                justify=justify,
                emoji=emoji,
                markup=markup,
                highlight=highlight,
            )
            if style is not None:
                renderables = [Styled(renderable, style) for renderable in renderables]

            # 2. [反射] 获取调用者的文件名、行号和局部变量
            filename, line_no, locals = self._caller_frame_info(_stack_offset)
            link_path = None if filename.startswith("<") else os.path.abspath(filename)
            path = filename.rpartition(os.sep)[-1]
            
            # 3. [局部变量打印]
            # 如果开启 log_locals，将调用处的局部变量渲染出来，方便调试。
            if log_locals:
                locals_map = {
                    key: value
                    for key, value in locals.items()
                    if not key.startswith("__")
                }
                renderables.append(render_scope(locals_map, title="[i]locals"))

            # 4. [日志格式化]
            # 使用 _log_render 将内容包装成带时间、路径的格式
            renderables = [
                self._log_render(
                    self,
                    renderables,
                    log_time=self.get_datetime(),
                    path=path,
                    line_no=line_no,
                    link_path=link_path,
                )
            ]
            for hook in render_hooks:
                renderables = hook.process_renderables(renderables)
            new_segments: List[Segment] = []
            extend = new_segments.extend
            render = self.render
            render_options = self.options
            for renderable in renderables:
                extend(render(renderable, render_options))
            buffer_extend = self._buffer.extend
            for line in Segment.split_and_crop_lines(
                new_segments, self.width, pad=False
            ):
                buffer_extend(line)

    def on_broken_pipe(self) -> None:
        """[异常处理：管道破裂]
        
        当用户通过管道 `|` 将 Rich 的输出传给其他程序（如 `less` 或 `head`），
        且接收程序提前退出时，会触发 BrokenPipeError。
        
        默认行为：
        1. 设置 quiet=True 停止输出。
        2. 重定向 stdout 到 /dev/null。
        3. 退出程序。
        这是处理 Unix 管道的标准做法。
        """
        self.quiet = True
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, sys.stdout.fileno())
        raise SystemExit(1)

    def _check_buffer(self) -> None:
        """[状态检查：缓冲区刷新门卫]
        
        检查当前是否可以刷新缓冲区（例如不在 quiet 模式）。
        如果可以，则调用 _write_buffer。
        """
        if self.quiet:
            del self._buffer[:]
            return

        try:
            self._write_buffer()
        except BrokenPipeError:
            self.on_broken_pipe()

    def _write_buffer(self) -> None:
        """[底层核心：物理写入]
        
        将内存中的 Segment 列表转换为最终字符串，并写入文件对象。
        处理了 Jupyter、Windows Legacy、Windows Modern 和 Unix 等多种环境差异。
        """
        with self._lock:
            # 1. [录制功能]
            # 如果开启了 record，且在顶层缓冲区（非嵌套），将 Segment 复制到录制缓冲区。
            if self.record and not self._buffer_index:
                with self._record_buffer_lock:
                    self._record_buffer.extend(self._buffer[:])

            # 2. [仅在最顶层缓冲区时才实际输出]
            if self._buffer_index == 0:
                if self.is_jupyter:  # pragma: no cover
                    # [环境：Jupyter]
                    # Jupyter 有特殊的 HTML 显示协议，不能直接 write text
                    from .jupyter import display

                    display(self._buffer, self._render_buffer(self._buffer[:]))
                    del self._buffer[:]
                else:
                    if WINDOWS:
                        # [环境：Windows]
                        use_legacy_windows_render = False
                        if self.legacy_windows:
                            fileno = get_fileno(self.file)
                            if fileno is not None:
                                use_legacy_windows_render = (
                                    fileno in _STD_STREAMS_OUTPUT
                                )

                        if use_legacy_windows_render:
                            # [分支：Windows Legacy API]
                            # 旧版 Windows 不支持 ANSI，必须调用 Win32 API 设置颜色
                            from rich._win32_console import LegacyWindowsTerm
                            from rich._windows_renderer import legacy_windows_render

                            buffer = self._buffer[:]
                            if self.no_color and self._color_system:
                                buffer = list(Segment.remove_color(buffer))

                            legacy_windows_render(buffer, LegacyWindowsTerm(self.file))
                        else:
                            # [分支：Windows Modern / Unix]
                            # 使用 ANSI 转义序列输出
                            text = self._render_buffer(self._buffer[:])
                            
                            # [Bug 修复：Python 写入限制]
                            # Python 在 Windows 上对单次 write 的大小有限制（约 32KB）。
                            # 参见: https://bugs.python.org/issue37871
                            # 必须分批写入，否则数据会丢失。
                            write = self.file.write
                            # 估算最坏情况：每个字符 4 字节 (UTF-8)
                            MAX_WRITE = 32 * 1024 // 4
                            try:
                                if len(text) <= MAX_WRITE:
                                    write(text)
                                else:
                                    # [分块写入逻辑]
                                    batch: List[str] = []
                                    batch_append = batch.append
                                    size = 0
                                    for line in text.splitlines(True):
                                        if size + len(line) > MAX_WRITE and batch:
                                            write("".join(batch))
                                            batch.clear()
                                            size = 0
                                        batch_append(line)
                                        size += len(line)
                                    if batch:
                                        write("".join(batch))
                                        batch.clear()
                            except UnicodeEncodeError as error:
                                error.reason = f"{error.reason}\n*** You may need to add PYTHONIOENCODING=utf-8 to your environment ***"
                                raise
                    else:
                        # [环境：Unix/Linux/macOS]
                        text = self._render_buffer(self._buffer[:])
                        try:
                            self.file.write(text)
                        except UnicodeEncodeError as error:
                            error.reason = f"{error.reason}\n*** You may need to add PYTHONIOENCODING=utf-8 to your environment ***"
                            raise

                    # [刷新] 确保数据从缓冲区刷入设备
                    self.file.flush()
                    # 清空已写入的缓冲区
                    del self._buffer[:]

    def _render_buffer(self, buffer: Iterable[Segment]) -> str:
        """[转换核心：Segment -> String]
        
        将抽象的 Segment 对象列表转换为具体的字符串。
        这是样式生效的地方：Style 对象被转换为 ANSI 转义序列。
        """
        output: List[str] = []
        append = output.append
        color_system = self._color_system
        legacy_windows = self.legacy_windows
        not_terminal = not self.is_terminal
        
        # [全局过滤：No Color]
        # 如果设置了 no_color，移除所有样式相关的 Segment
        if self.no_color and color_system:
            buffer = Segment.remove_color(buffer)
            
        for text, style, control in buffer:
            if style:
                # [关键] 调用 Style.render 将样式转为控制码
                append(
                    style.render(
                        text,
                        color_system=color_system,
                        legacy_windows=legacy_windows,
                    )
                )
            elif not (not_terminal and control):
                # 如果不是控制字符，或者是终端环境，直接追加文本
                append(text)

        rendered = "".join(output)
        return rendered

    def input(
        self,
        prompt: TextType = "",
        *,
        markup: bool = True,
        emoji: bool = True,
        password: bool = False,
        stream: Optional[TextIO] = None,
    ) -> str:
        """[交互工具：增强版 Input]
        
        类似 Python 内置的 input()，但支持 Rich 的颜色、Markup 和 Emoji。
        """
        if prompt:
            # 打印提示符（不换行）
            self.print(prompt, markup=markup, emoji=emoji, end="")
        if password:
            # [安全] 使用 getpass 隐藏输入
            result = getpass("", stream=stream)
        else:
            if stream:
                result = stream.readline()
            else:
                result = input()
        return result

    def export_text(self, *, clear: bool = True, styles: bool = False) -> str:
        """[导出功能：转为文本]
        
        将之前录制的输出（需要 record=True）导出为纯文本。
        
        Args:
            styles: 如果为 True，保留 ANSI 颜色码（使得文本在支持颜色的终端里看仍有颜色）。
        """
        assert (
            self.record
        ), "To export console contents set record=True in the constructor or instance"

        with self._record_buffer_lock:
            if styles:
                # [带样式] 拼接 text 和 style.render(text) 的结果
                text = "".join(
                    (style.render(text) if style else text)
                    for text, style, _ in self._record_buffer
                )
            else:
                # [纯文本] 仅提取 text 字段，忽略 control
                text = "".join(
                    segment.text
                    for segment in self._record_buffer
                    if not segment.control
                )
            if clear:
                del self._record_buffer[:]
        return text

    def save_text(self, path: str, *, clear: bool = True, styles: bool = False) -> None:
        """[导出功能：保存文本]
        
        将控制台内容保存到指定路径的文件中。
        """
        text = self.export_text(clear=clear, styles=styles)
        with open(path, "w", encoding="utf-8") as write_file:
            write_file.write(text)

    def export_html(
        self,
        *,
        theme: Optional[TerminalTheme] = None,
        clear: bool = True,
        code_format: Optional[str] = None,
        inline_styles: bool = False,
    ) -> str:
        """[导出功能：转为 HTML]
        
        将终端输出转换为 HTML 页面。这对于生成文档或分享日志非常有用。
        
        Args:
            theme: 指定颜色主题，将终端颜色映射为 CSS 颜色。
            inline_styles: 如果为 True，样式写在 <span style=""> 中；否则写在 <style> 标签中。
        """
        assert (
            self.record
        ), "To export console contents set record=True in the constructor or instance"
        fragments: List[str] = []
        append = fragments.append
        # [默认主题]
        _theme = theme or DEFAULT_TERMINAL_THEME
        stylesheet = ""

            # [延续 export_html 的后半部分]
    render_code_format = CONSOLE_HTML_FORMAT if code_format is None else code_format

    with self._record_buffer_lock:
        # [分支 A：内联样式模式]
        if inline_styles:
            for text, style, _ in Segment.filter_control(
                Segment.simplify(self._record_buffer)
            ):
                text = escape(text) # HTML 转义
                if style:
                    rule = style.get_html_style(_theme)
                    if style.link:
                        text = f'<a href="{style.link}">{text}</a>'
                    # 直接将 CSS 写入 style 属性，文件体积大但兼容性好
                    text = f'<span style="{rule}">{text}</span>' if rule else text
                append(text)
        # [分支 B：类样式模式]
        else:
            styles: Dict[str, int] = {}
            # 收集所有唯一的样式规则，并分配编号（r1, r2...）
            for text, style, _ in Segment.filter_control(
                Segment.simplify(self._record_buffer)
            ):
                text = escape(text)
                if style:
                    rule = style.get_html_style(_theme)
                    style_number = styles.setdefault(rule, len(styles) + 1)
                    if style.link:
                        text = f'<a class="r{style_number}" href="{style.link}">{text}</a>'
                    else:
                        text = f'<span class="r{style_number}">{text}</span>'
                append(text)
            # 生成 <style> 标签内容
            stylesheet_rules: List[str] = []
            stylesheet_append = stylesheet_rules.append
            for style_rule, style_number in styles.items():
                if style_rule:
                    stylesheet_append(f".r{style_number} {{{style_rule}}}")
            stylesheet = "\n".join(stylesheet_rules)

        # [模板填充]
        rendered_code = render_code_format.format(
            code="".join(fragments),
            stylesheet=stylesheet,
            foreground=_theme.foreground_color.hex,
            background=_theme.background_color.hex,
        )
        if clear:
            del self._record_buffer[:]
        rendered_code

    def save_html(
        self,
        path: str,
        *,
        theme: Optional[TerminalTheme] = None,
        clear: bool = True,
        code_format: str = CONSOLE_HTML_FORMAT,
        inline_styles: bool = False,
    ) -> None:
        """[导出功能：保存 HTML]
        
        将录制的内容渲染为 HTML 并写入文件。
        """
        html = self.export_html(
            theme=theme,
            clear=clear,
            code_format=code_format,
            inline_styles=inline_styles,
        )
        with open(path, "w", encoding="utf-8") as write_file:
            write_file.write(html)

    def export_svg(
        self,
        *,
        title: str = "Rich",
        theme: Optional[TerminalTheme] = None,
        clear: bool = True,
        code_format: str = CONSOLE_SVG_FORMAT,
        font_aspect_ratio: float = 0.61,
        unique_id: Optional[str] = None,
    ) -> str:
        """[核心渲染引擎：SVG 矢量图生成]
        
        这是 Rich 最复杂的导出功能之一。它将终端文本精确地转换为 SVG 矢量图形。
        
        挑战：
        1. 坐标映射：将文本的行列号转换为 SVG 的 x,y 像素坐标。
        2. 背景渲染：终端的背景色通常是矩形容器，需要单独绘制。
        3. 字体处理：需要考虑字符宽高比，以及全角字符（如中文）的宽度计算。
        """

        from rich.cells import cell_len

        # [性能优化：样式缓存]
        # 避免为每个字符生成重复的 CSS 类。
        style_cache: Dict[Style, str] = {}

        def get_svg_style(style: Style) -> str:
            """[转换器：Style -> CSS]
            
            将 Rich 内部的 Style 对象转换为 SVG/CSS 属性字符串。
            """
            if style in style_cache:
                return style_cache[style]
            css_rules = []
            # [颜色处理]：处理前景色和背景色，考虑默认值和反转色
            color = (
                _theme.foreground_color
                if (style.color is None or style.color.is_default)
                else style.color.get_truecolor(_theme)
            )
            bgcolor = (
                _theme.background_color
                if (style.bgcolor is None or style.bgcolor.is_default)
                else style.bgcolor.get_truecolor(_theme)
            )
            if style.reverse:
                color, bgcolor = bgcolor, color
            if style.dim:
                color = blend_rgb(color, bgcolor, 0.4)
            css_rules.append(f"fill: {color.hex}")
            
            # [字体样式处理]
            if style.bold:
                css_rules.append("font-weight: bold")
            if style.italic:
                css_rules.append("font-style: italic;")
            if style.underline:
                css_rules.append("text-decoration: underline;")
            if style.strike:
                css_rules.append("text-decoration: line-through;")

            css = ";".join(css_rules)
            style_cache[style] = css
            return css

        _theme = theme or SVG_EXPORT_THEME

        # [布局参数计算]
        # SVG 不像终端那样有“字符”单位，必须转换为像素。
        width = self.width
        char_height = 20  # 假设每个字符高 20px
        char_width = char_height * font_aspect_ratio # 宽度由宽高比决定 (0.61 近似 Fira Code)
        line_height = char_height * 1.22 # 行高略大于字高

        margin_top = 1
        margin_right = 1
        margin_bottom = 1
        margin_left = 1

        padding_top = 40
        padding_right = 8
        padding_bottom = 8
        padding_left = 8

        padding_width = padding_left + padding_right
        padding_height = padding_top + padding_bottom
        margin_width = margin_left + margin_right
        margin_height = margin_top + margin_bottom

        text_backgrounds: List[str] = []
        text_group: List[str] = []
        classes: Dict[str, int] = {}
        style_no = 1

        def escape_text(text: str) -> str:
            """HTML escape text and replace spaces with nbsp."""
            # [细节处理]：普通空格在 HTML 中会折叠，必须用 &nbsp; 保持对齐
            return escape(text).replace(" ", "&#160;")

        def make_tag(
            name: str, content: Optional[str] = None, **attribs: object
        ) -> str:
            """[辅助函数：XML 标签生成器]"""
            def stringify(value: object) -> str:
                if isinstance(value, (float)):
                    return format(value, "g")
                return str(value)

            tag_attribs = " ".join(
                f'{k.lstrip("_").replace("_", "-")}="{stringify(v)}"'
                for k, v in attribs.items()
            )
            return (
                f"<{name} {tag_attribs}>{content}</{name}>"
                if content
                else f"<{name} {tag_attribs}/>"
            )

        with self._record_buffer_lock:
            segments = list(Segment.filter_control(self._record_buffer))
            if clear:
                self._record_buffer.clear()

        # [ID 生成]：确保 SVG 内部 ID 唯一，避免多次导出冲突
        if unique_id is None:
            unique_id = "terminal-" + str(
                zlib.adler32(
                    ("".join(repr(segment) for segment in segments)).encode(
                        "utf-8",
                        "ignore",
                    )
                    + title.encode("utf-8", "ignore")
                )
            )
            
        y = 0
        # [主渲染循环]
        for y, line in enumerate(Segment.split_and_crop_lines(segments, length=width)):
            x = 0
            for text, style, _control in line:
                style = style or Style()
                rules = get_svg_style(style)
                # [CSS 类复用]：相同的样式共用一个 CSS 类
                if rules not in classes:
                    classes[rules] = style_no
                    style_no += 1
                class_name = f"r{classes[rules]}"

                # [背景色渲染]
                # SVG 文本没有背景色属性，需要画一个 <rect> 在文字下面
                if style.reverse:
                    has_background = True
                    background = (
                        _theme.foreground_color.hex
                        if style.color is None
                        else style.color.get_truecolor(_theme).hex
                    )
                else:
                    bgcolor = style.bgcolor
                    has_background = bgcolor is not None and not bgcolor.is_default
                    background = (
                        _theme.background_color.hex
                        if style.bgcolor is None
                        else style.bgcolor.get_truecolor(_theme).hex
                    )

                text_length = cell_len(text) # 使用 cell_len 处理全角字符宽度
                if has_background:
                    text_backgrounds.append(
                        make_tag(
                            "rect", # 矩形标签
                            fill=background,
                            x=x * char_width, # 像素坐标 X
                            y=y * line_height + 1.5, # 像素坐标 Y
                            width=char_width * text_length, # 矩形宽度
                            height=line_height + 0.25, # 矩形高度
                            shape_rendering="crispEdges", # 锐化边缘，防止模糊
                        )
                    )

                if text != " " * len(text):
                    # [文本渲染]
                    text_group.append(
                        make_tag(
                            "text",
                            escape_text(text),
                            _class=f"{unique_id}-{class_name}",
                            x=x * char_width,
                            y=y * line_height + char_height, # 基线对齐
                            textLength=char_width * len(text),
                            # [裁剪路径]：防止文本溢出到背景块之外（特别是对于特殊字符）
                            clip_path=f"url(#{unique_id}-line-{y})",
                        )
                    )
                x += cell_len(text)

        # [剪切路径定义]
        # 为每一行定义一个剪切区域，防止溢出
        line_offsets = [line_no * line_height + 1.5 for line_no in range(y)]
        lines = "\n".join(
            f"""<clipPath id="{unique_id}-line-{line_no}">
    {make_tag("rect", x=0, y=offset, width=char_width * width, height=line_height + 0.25)}
            </clipPath>"""
            for line_no, offset in enumerate(line_offsets)
        )

        # [样式表生成]
        styles = "\n".join(
            f".{unique_id}-r{rule_no} {{ {css} }}" for css, rule_no in classes.items()
        )
        backgrounds = "".join(text_backgrounds)
        matrix = "".join(text_group)

        # [画布尺寸计算]
        terminal_width = ceil(width * char_width + padding_width)
        terminal_height = (y + 1) * line_height + padding_height
        
        # [UI 装饰：窗口边框]
        chrome = make_tag(
            "rect",
            fill=_theme.background_color.hex,
            stroke="rgba(255,255,255,0.35)",
            stroke_width="1",
            x=margin_left,
            y=margin_top,
            width=terminal_width,
            height=terminal_height,
            rx=8, # 圆角
        )

        # [UI 装饰：标题栏]
        title_color = _theme.foreground_color.hex
        if title:
            chrome += make_tag(
                "text",
                escape_text(title),
                _class=f"{unique_id}-title",
                fill=title_color,
                text_anchor="middle",
                x=terminal_width // 2,
                y=margin_top + char_height + 6,
            )
        # [UI 装饰：macOS 风格的红黄绿按钮]
        chrome += f"""
            <g transform="translate(26,22)">
            <circle cx="0" cy="0" r="7" fill="#ff5f57"/>
            <circle cx="22" cy="0" r="7" fill="#febc2e"/>
            <circle cx="44" cy="0" r="7" fill="#28c840"/>
            </g>
        """

        # [模板填充与返回]
        svg = code_format.format(
            unique_id=unique_id,
            char_width=char_width,
            char_height=char_height,
            line_height=line_height,
            terminal_width=char_width * width - 1,
            terminal_height=(y + 1) * line_height - 1,
            width=terminal_width + margin_width,
            height=terminal_height + margin_height,
            terminal_x=margin_left + padding_left,
            terminal_y=margin_top + padding_top,
            styles=styles,
            chrome=chrome,
            backgrounds=backgrounds,
            matrix=matrix,
            lines=lines,
        )
        return svg

    def save_svg(
        self,
        path: str,
        *,
        title: str = "Rich",
        theme: Optional[TerminalTheme] = None,
        clear: bool = True,
        code_format: str = CONSOLE_SVG_FORMAT,
        font_aspect_ratio: float = 0.61,
        unique_id: Optional[str] = None,
    ) -> None:
        """[导出功能：保存 SVG]"""
        svg = self.export_svg(
            title=title,
            theme=theme,
            clear=clear,
            code_format=code_format,
            font_aspect_ratio=font_aspect_ratio,
            unique_id=unique_id,
        )
        with open(path, "w", encoding="utf-8") as write_file:
            write_file.write(svg)


def _svg_hash(svg_main_code: str) -> str:
    """[辅助函数：哈希生成]
    
    使用 Adler32 算法生成内容的哈希值。
    Adler32 比 MD5/SHA 更快，虽然安全性较低，但在这里用于生成唯一 ID 已经足够。
    """
    return str(zlib.adler32(svg_main_code.encode()))


if __name__ == "__main__":  # pragma: no cover
    # [模块测试入口]
    # 当直接运行此文件时，执行以下测试代码。
    console = Console(record=True)

    console.log(
        "JSONRPC [i]request[/i]",
        5,
        1.3,
        True,
        False,
        None,
        {
            "jsonrpc": "2.0",
            "method": "subtract",
            "params": {"minuend": 42, "subtrahend": 23},
            "id": 3,
        },
    )

        # [功能演示：日志输出]
    # 使用 console.log() 打印信息。
    # 区别：log() 会自动在输出前添加“时间戳”、“文件路径”和“行号”，非常适合调试和记录程序运行状态。
    console.log("Hello, World!", "{'a': 1}", repr(console))

    # [功能演示：结构化数据美化打印]
    # 使用 console.print() 打印一个复杂的嵌套字典。
    # 
    # 核心特性：
    # 1. 自动检测类型：识别出这是一个 dict。
    # 2. 递归渲染：深入到多层嵌套结构中。
    # 3. 语法高亮：字典的键、字符串值、布尔值会有不同的颜色，极大提升可读性。
    # 4. 自动缩进：根据层级自动对齐。
    console.print(
        {
            "name": None,
            "empty": [],
            "quiz": {
                "sport": {
                    "answered": True,
                    "q1": {
                        "question": "Which one is correct team name in NBA?",
                        "options": [
                            "New York Bulls",
                            "Los Angeles Kings",
                            "Golden State Warriors",
                            "Huston Rocket",
                        ],
                        "answer": "Huston Rocket",
                    },
                },
                "maths": {
                    "answered": False,
                    "q1": {
                        "question": "5 + 7 = ?",
                        "options": [10, 11, 12, 13],
                        "answer": 12,
                    },
                    "q2": {
                        "question": "12 - 8 = ?",
                        "options": [1, 2, 3, 4],
                        "answer": 4,
                    },
                },
            },
        }
    )
