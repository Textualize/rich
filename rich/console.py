import inspect
import os
import platform
import shutil
import sys
import threading
from abc import ABC, abstractmethod
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field, replace
from functools import wraps
from getpass import getpass
from typing import (
    IO,
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    NamedTuple,
    Optional,
    TextIO,
    Union,
    cast,
)

from typing_extensions import Literal, Protocol, runtime_checkable

from . import errors, themes
from ._emoji_replace import _emoji_replace
from ._log_render import LogRender
from .align import Align, AlignValues
from .color import ColorSystem
from .control import Control
from .highlighter import NullHighlighter, ReprHighlighter
from .markup import render as render_markup
from .measure import Measurement, measure_renderables
from .pretty import Pretty
from .scope import render_scope
from .segment import Segment
from .style import Style
from .terminal_theme import DEFAULT_TERMINAL_THEME, TerminalTheme
from .text import Text, TextType
from .theme import Theme

if TYPE_CHECKING:
    from ._windows import WindowsConsoleFeatures

WINDOWS = platform.system() == "Windows"

HighlighterType = Callable[[Union[str, "Text"]], "Text"]
JustifyMethod = Literal["default", "left", "center", "right", "full"]
OverflowMethod = Literal["fold", "crop", "ellipsis", "ignore"]


CONSOLE_HTML_FORMAT = """\
<!DOCTYPE html>
<head>
<style>
{stylesheet}
body {{
    color: {foreground};
    background-color: {background};
}}
</style>
</head>
<html>
<body>
    <code>
        <pre style="font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">{code}</pre>
    </code>
</body>
</html>
"""

_TERM_COLORS = {"256color": ColorSystem.EIGHT_BIT, "16color": ColorSystem.STANDARD}


@dataclass
class ConsoleOptions:
    """Options for __rich_console__ method."""

    min_width: int
    """Minimum width of renderable."""
    max_width: int
    """Maximum width of renderable."""
    is_terminal: bool
    """True if the target is a terminal, otherwise False."""
    encoding: str
    """Encoding of terminal."""
    justify: Optional[JustifyMethod] = None
    """Justify value override for renderable."""
    overflow: Optional[OverflowMethod] = None
    """Overflow value override for renderable."""
    no_wrap: Optional[bool] = False
    """"Disable wrapping for text."""

    def update(
        self,
        width: int = None,
        min_width: int = None,
        max_width: int = None,
        justify: JustifyMethod = None,
        overflow: OverflowMethod = None,
        no_wrap: bool = None,
    ) -> "ConsoleOptions":
        """Update values, return a copy."""
        options = replace(self)
        if width is not None:
            options.min_width = options.max_width = width
        if min_width is not None:
            options.min_width = min_width
        if max_width is not None:
            options.max_width = max_width
        if justify is not None:
            options.justify = justify
        if overflow is not None:
            options.overflow = overflow
        if no_wrap is not None:
            options.no_wrap = no_wrap
        return options


@runtime_checkable
class RichCast(Protocol):
    """An object that may be 'cast' to a console renderable."""

    def __rich__(self) -> Union["ConsoleRenderable", str]:  # pragma: no cover
        ...


@runtime_checkable
class ConsoleRenderable(Protocol):
    """An object that supports the console protocol."""

    def __rich_console__(
        self, console: "Console", options: "ConsoleOptions"
    ) -> "RenderResult":  # pragma: no cover
        ...


RenderableType = Union[ConsoleRenderable, RichCast, str]
"""A type that may be rendered by Console."""

RenderResult = Iterable[Union[RenderableType, Segment]]
"""The result of calling a __rich_console__ method."""


_null_highlighter = NullHighlighter()


class RenderGroup:
    """Takes a group of renderables and returns a renderable object that renders the group.

    Args:
        renderables (Iterable[RenderableType]): An iterable of renderable objects.

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

    def __rich_measure__(self, console: "Console", max_width: int) -> "Measurement":
        if self.fit:
            return measure_renderables(console, self.renderables, max_width)
        else:
            return Measurement(max_width, max_width)

    def __rich_console__(
        self, console: "Console", options: "ConsoleOptions"
    ) -> RenderResult:
        yield from self.renderables


def render_group(fit: bool = False) -> Callable:
    def decorator(method):
        """Convert a method that returns an iterable of renderables in to a RenderGroup."""

        @wraps(method)
        def _replace(*args, **kwargs):
            renderables = method(*args, **kwargs)
            return RenderGroup(*renderables, fit=fit)

        return _replace

    return decorator


class ConsoleDimensions(NamedTuple):
    """Size of the terminal."""

    width: int
    """The width of the console in 'cells'."""
    height: int
    """The height of the console in lines."""


def _is_jupyter() -> bool:  # pragma: no cover
    """Check if we're running in a Jupyter notebook."""
    try:
        get_ipython  # type: ignore
    except NameError:
        return False
    shell = get_ipython().__class__.__name__  # type: ignore
    if shell == "ZMQInteractiveShell":
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


_COLOR_SYSTEMS_NAMES = {system: name for name, system in COLOR_SYSTEMS.items()}


@dataclass
class ConsoleThreadLocals(threading.local):
    """Thread local values for Console context."""

    buffer: List[Segment] = field(default_factory=list)
    buffer_index: int = 0


class RenderHook(ABC):
    """Provides hooks in to the render process."""

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


_windows_console_features: Optional["WindowsConsoleFeatures"] = None


def get_windows_console_features() -> "WindowsConsoleFeatures":  # pragma: no cover
    global _windows_console_features
    if _windows_console_features is not None:
        return _windows_console_features
    from ._windows import get_windows_console_features

    _windows_console_features = get_windows_console_features()
    return _windows_console_features


def detect_legacy_windows() -> bool:
    """Detect legacy Windows."""
    return WINDOWS and not get_windows_console_features().vt


if detect_legacy_windows():  # pragma: no cover
    from colorama import init

    init()


class Console:
    """A high level console interface.

    Args:
        color_system (str, optional): The color system supported by your terminal,
            either ``"standard"``, ``"256"`` or ``"truecolor"``. Leave as ``"auto"`` to autodetect.
        force_terminal (bool, optional): Force the Console to write control codes even when a terminal is not detected. Defaults to False.
        force_jupyter (bool, optional): Force the Console to write to Jupyter even when Jupyter is not detected. Defaults to False
        theme (Theme, optional): An optional style theme object, or ``None`` for default theme.
        file (IO, optional): A file object where the console should write to. Defaults to stdoutput.
        width (int, optional): The width of the terminal. Leave as default to auto-detect width.
        height (int, optional): The height of the terminal. Leave as default to auto-detect height.
        record (bool, optional): Boolean to enable recording of terminal output,
            required to call :meth:`export_html` and :meth:`export_text`. Defaults to False.        
        markup (bool, optional): Boolean to enable :ref:`console_markup`. Defaults to True.
        emoji (bool, optional): Enable emoji code. Defaults to True.
        highlight (bool, optional): Enable automatic highlighting. Defaults to True.
        log_time (bool, optional): Boolean to enable logging of time by :meth:`log` methods. Defaults to True.
        log_path (bool, optional): Boolean to enable the logging of the caller by :meth:`log`. Defaults to True.
        log_time_format (str, optional): Log time format if ``log_time`` is enabled. Defaults to "[%X] ".
        highlighter (HighlighterType, optional): Default highlighter.
        legacy_windows (bool, optional): Enable legacy Windows mode, or ``None`` to auto detect. Defaults to ``None``.
        safe_box (bool, optional): Restrict box options that don't render on legacy Windows.
    """

    def __init__(
        self,
        *,
        color_system: Optional[
            Literal["auto", "standard", "256", "truecolor", "windows"]
        ] = "auto",
        force_terminal: bool = False,
        force_jupyter: bool = False,
        theme: Theme = None,
        file: IO[str] = None,
        width: int = None,
        height: int = None,
        tab_size: int = 8,
        record: bool = False,
        markup: bool = True,
        emoji: bool = True,
        highlight: bool = True,
        log_time: bool = True,
        log_path: bool = True,
        log_time_format: str = "[%X]",
        highlighter: Optional["HighlighterType"] = ReprHighlighter(),
        legacy_windows: bool = None,
        safe_box: bool = True,
        _environ: Dict[str, str] = None,
    ):
        # Copy of os.environ allows us to replace it for testing
        self._environ = os.environ if _environ is None else _environ

        self.is_jupyter = force_jupyter or _is_jupyter()
        if self.is_jupyter:
            width = width or 93
            height = height or 100
        self._styles = themes.DEFAULT.styles if theme is None else theme.styles
        self._width = width
        self._height = height
        self.tab_size = tab_size
        self.record = record
        self._markup = markup
        self._emoji = emoji
        self._highlight = highlight
        self.legacy_windows: bool = (
            (detect_legacy_windows() and not self.is_jupyter)
            if legacy_windows is None
            else legacy_windows
        )

        self._color_system: Optional[ColorSystem]
        self._force_terminal = force_terminal
        self.file = file or sys.stdout

        if color_system is None:
            self._color_system = None
        elif color_system == "auto":
            self._color_system = self._detect_color_system()
        else:
            self._color_system = COLOR_SYSTEMS[color_system]

        self._lock = threading.RLock()
        self._log_render = LogRender(
            show_time=log_time, show_path=log_path, time_format=log_time_format,
        )
        self.highlighter: HighlighterType = highlighter or _null_highlighter
        self.safe_box = safe_box

        self._record_buffer_lock = threading.RLock()
        self._thread_locals = ConsoleThreadLocals()
        self._record_buffer: List[Segment] = []
        self._render_hooks: List[RenderHook] = []

    def __repr__(self) -> str:
        return f"<console width={self.width} {str(self._color_system)}>"

    @property
    def _buffer(self) -> List[Segment]:
        """Get a thread local buffer."""
        return self._thread_locals.buffer

    @property
    def _buffer_index(self) -> int:
        """Get a thread local buffer."""
        return self._thread_locals.buffer_index

    @_buffer_index.setter
    def _buffer_index(self, value: int) -> None:
        self._thread_locals.buffer_index = value

    def _detect_color_system(self) -> Optional[ColorSystem]:
        """Detect color system from env vars."""
        if self.is_jupyter:
            return ColorSystem.TRUECOLOR
        if not self.is_terminal or "NO_COLOR" in self._environ or self.is_dumb_terminal:
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
            if color_term in ("truecolor", "24bit"):
                return ColorSystem.TRUECOLOR
            term = self._environ.get("TERM", "").strip().lower()
            _term_name, _hyphen, colors = term.partition("-")
            color_system = _TERM_COLORS.get(colors, ColorSystem.STANDARD)
            return color_system

    def _enter_buffer(self) -> None:
        """Enter in to a buffer context, and buffer all output."""
        self._buffer_index += 1

    def _exit_buffer(self) -> None:
        """Leave buffer context, and render content if required."""
        self._buffer_index -= 1
        self._check_buffer()

    def push_render_hook(self, hook: RenderHook) -> None:
        """Add a new render hook to the stack.

        Args:
            hook (RenderHook): Render hook instance.
        """

        self._render_hooks.append(hook)

    def pop_render_hook(self) -> None:
        """Pop the last renderhook from the stack."""
        self._render_hooks.pop()

    def __enter__(self) -> "Console":
        """Own context manager to enter buffer context."""
        self._enter_buffer()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """Exit buffer context."""
        self._exit_buffer()

    @property
    def color_system(self) -> Optional[str]:
        """Get color system string.

        Returns:
            Optional[str]: "standard", "256" or "truecolor".
        """

        if self._color_system is not None:
            return _COLOR_SYSTEMS_NAMES[self._color_system]
        else:
            return None

    @property
    def encoding(self) -> str:
        """Get the encoding of the console file, e.g. ``"utf-8"``.

        Returns:
            str: A standard encoding string.
        """
        return getattr(self.file, "encoding", "utf-8")

    @property
    def is_terminal(self) -> bool:
        """Check if the console is writing to a terminal.

        Returns:
            bool: True if the console writing to a device capable of
            understanding terminal codes, otherwise False.
        """
        if self._force_terminal:
            return True
        isatty = getattr(self.file, "isatty", None)
        return False if isatty is None else isatty()

    @property
    def is_dumb_terminal(self) -> bool:
        """Detect dumb terminal.
        
        Returns:
            bool: True if writing to a dumb terminal, otherwise False.
        
        """
        is_dumb = "TERM" in self._environ and self._environ["TERM"].lower() in (
            "dumb",
            "unknown",
        )
        return self.is_terminal and is_dumb

    @property
    def options(self) -> ConsoleOptions:
        """Get default console options."""
        return ConsoleOptions(
            min_width=1,
            max_width=self.width,
            encoding=self.encoding,
            is_terminal=self.is_terminal,
        )

    @property
    def size(self) -> ConsoleDimensions:
        """Get the size of the console.

        Returns:
            ConsoleDimensions: A named tuple containing the dimensions.
        """

        if self._width is not None and self._height is not None:
            return ConsoleDimensions(self._width, self._height)

        if self.is_terminal and self.is_dumb_terminal:
            return ConsoleDimensions(80, 25)

        width, height = shutil.get_terminal_size()
        # get_terminal_size can report 0, 0 if run from psuedo-terminal
        width = width or 80
        height = height or 25
        return ConsoleDimensions(
            (width - self.legacy_windows) if self._width is None else self._width,
            height if self._height is None else self._height,
        )

    @property
    def width(self) -> int:
        """Get the width of the console.

        Returns:
            int: The width (in characters) of the console.
        """
        width, _ = self.size
        return width

    def line(self, count: int = 1) -> None:
        """Write new line(s).

        Args:
            count (int, optional): Number of new lines. Defaults to 1.
        """

        assert count >= 0, "count must be >= 0"
        if count:
            self._buffer.append(Segment("\n" * count))
            self._check_buffer()

    def clear(self, home: bool = True) -> None:
        """Clear the screen.

        Args:
            home (bool, optional): Also move the cursor to 'home' position. Defaults to True.
        """
        self.control("\033[2J\033[H" if home else "\033[2J")

    def show_cursor(self, show: bool = True) -> None:
        """Show or hide the cursor.
        
        Args:
            show (bool, optional): Set visibility of the cursor.
        """
        if self.is_terminal and not self.legacy_windows:
            self.control("\033[?25h" if show else "\033[?25l")

    def render(
        self, renderable: RenderableType, options: ConsoleOptions = None
    ) -> Iterable[Segment]:
        """Render an object in to an iterable of `Segment` instances.

        This method contains the logic for rendering objects with the console protocol.
        You are unlikely to need to use it directly, unless you are extending the library.

        Args:
            renderable (RenderableType): An object supporting the console protocol, or
                an object that may be converted to a string.
            options (ConsoleOptions, optional): An options object, or None to use self.options. Defaults to None.

        Returns:
            Iterable[Segment]: An iterable of segments that may be rendered.
        """

        _options = options or self.options
        render_iterable: RenderResult
        if isinstance(renderable, ConsoleRenderable):
            render_iterable = renderable.__rich_console__(self, _options)
        elif isinstance(renderable, str):
            yield from self.render(self.render_str(renderable), _options)
            return
        else:
            raise errors.NotRenderableError(
                f"Unable to render {renderable!r}; "
                "A str, Segment or object with __rich_console__ method is required"
            )

        try:
            iter_render = iter(render_iterable)
        except TypeError:
            raise errors.NotRenderableError(
                f"object {render_iterable!r} is not renderable"
            )
        for render_output in iter_render:
            if isinstance(render_output, Segment):
                yield render_output
            else:
                yield from self.render(render_output, _options)

    def render_lines(
        self,
        renderable: RenderableType,
        options: Optional[ConsoleOptions] = None,
        *,
        style: Optional[Style] = None,
        pad: bool = True,
    ) -> List[List[Segment]]:
        """Render objects in to a list of lines.

        The output of render_lines is useful when further formatting of rendered console text
        is required, such as the Panel class which draws a border around any renderable object.

        Args:
            renderables (Iterable[RenderableType]): Any object or objects renderable in the console.
            options (Optional[ConsoleOptions], optional): Console options, or None to use self.options. Default to ``None``.
            style (Style, optional): Optional style to apply to renderables. Defaults to ``None``.
            pad (bool, optional): Pad lines shorter than render width. Defaults to ``True``.

        Returns:
            List[List[Segment]]: A list of lines, where a line is a list of Segment objects.
        """
        render_options = options or self.options
        _rendered = self.render(renderable, render_options)
        if style is not None:
            _rendered = Segment.apply_style(_rendered, style)
        lines = list(
            Segment.split_and_crop_lines(
                _rendered, render_options.max_width, include_new_lines=False, pad=pad
            )
        )
        return lines

    def render_str(
        self,
        text: str,
        *,
        style: Union[str, Style] = "",
        justify: JustifyMethod = None,
        overflow: OverflowMethod = None,
        emoji: bool = None,
        markup: bool = None,
        highlighter: HighlighterType = None,
    ) -> "Text":
        """Convert a string to a Text instance. This is is called automatically if
        you print or log a string.

        Args:
            text (str): Text to render.
            style (Union[str, Style], optional): Style to apply to rendered text.
            justify (str, optional): Justify method: "default", "left", "center", "full", or "right". Defaults to ``None``.
            overflow (str, optional): Overflow method: "crop", "fold", or "ellipsis". Defaults to ``None``.
            emoji (Optional[bool], optional): Enable emoji, or ``None`` to use Console default.
            markup (Optional[bool], optional): Enable markup, or ``None`` to use Console default.
            highlighter (HighlighterType, optional): Optional highlighter to apply.
        Returns:
            ConsoleRenderable: Renderable object.

        """
        emoji_enabled = emoji or (emoji is None and self._emoji)
        markup_enabled = markup or (markup is None and self._markup)

        if markup_enabled:
            rich_text = render_markup(text, style=style, emoji=emoji_enabled)
            rich_text.justify = justify
            rich_text.overflow = overflow
        else:
            rich_text = Text(
                _emoji_replace(text) if emoji_enabled else text,
                justify=justify,
                overflow=overflow,
                style=style,
            )

        if highlighter is not None:
            highlight_text = highlighter(str(rich_text))
            highlight_text.copy_styles(rich_text)
            return highlight_text

        return rich_text

    def get_style(
        self, name: Union[str, Style], *, default: Union[Style, str] = None
    ) -> Style:
        """Get a Style instance by it's theme name or parse a definition.

        Args:
            name (str): The name of a style or a style definition.

        Returns:
            Style: A Style object.

        Raises:
            MissingStyle: If no style could be parsed from name.

        """
        if isinstance(name, Style):
            return name

        try:
            style = self._styles.get(name)
            return style.copy() if style is not None else Style.parse(name).copy()
        except errors.StyleSyntaxError as error:
            if default is not None:
                return self.get_style(default)
            raise errors.MissingStyle(f"Failed to get style {name!r}; {error}")

    def _collect_renderables(
        self,
        objects: Iterable[Any],
        sep: str,
        end: str,
        *,
        justify: JustifyMethod = None,
        emoji: bool = None,
        markup: bool = None,
        highlight: bool = None,
    ) -> List[ConsoleRenderable]:
        """Combined a number of renderables and text in to one renderable.

        Args:
            renderables (Iterable[Union[str, ConsoleRenderable]]): Anyting that Rich can render.
            sep (str, optional): String to write between print data. Defaults to " ".
            end (str, optional): String to write at end of print data. Defaults to "\\n".
            justify (str, optional): One of "left", "right", "center", or "full". Defaults to ``None``.       
            emoji (Optional[bool], optional): Enable emoji code, or ``None`` to use console default.
            markup (Optional[bool], optional): Enable markup, or ``None`` to use console default.
            highlight (Optional[bool], optional): Enable automatic highlighting, or ``None`` to use console default.

        Returns:
            List[ConsoleRenderable]: A list of things to render.
        """
        renderables: List[ConsoleRenderable] = []
        _append = renderables.append
        text: List[Text] = []
        append_text = text.append

        append = _append
        if justify in ("left", "center", "right"):

            def align_append(renderable: RenderableType) -> None:
                _append(Align(renderable, cast(AlignValues, justify)))

            append = align_append

        _highlighter: HighlighterType = _null_highlighter
        if highlight or (highlight is None and self._highlight):
            _highlighter = self.highlighter

        def check_text() -> None:
            if text:
                sep_text = Text(sep, end=end)
                append(sep_text.join(text))
                del text[:]

        for renderable in objects:
            rich_cast = getattr(renderable, "__rich__", None)
            if rich_cast:
                renderable = rich_cast()
            if isinstance(renderable, str):
                append_text(
                    self.render_str(
                        renderable,
                        emoji=emoji,
                        markup=markup,
                        highlighter=_highlighter,
                    )
                )
            elif isinstance(renderable, ConsoleRenderable):
                check_text()
                append(renderable)
            elif isinstance(renderable, (Mapping, Sequence)):
                check_text()
                append(Pretty(renderable, highlighter=_highlighter))
            else:
                append_text(_highlighter(str(renderable)))

        check_text()

        return renderables

    def rule(
        self,
        title: str = "",
        *,
        character: Optional[str] = None,
        characters: str = "─",
        style: Union[str, Style] = "rule.line",
    ) -> None:
        """Draw a line with optional centered title.
        
        Args:
            title (str, optional): Text to render over the rule. Defaults to "".
            character: Will be deprecated in v6.0.0, please use characters argument instead.
            characters (str, optional): Character(s) to form the line. Defaults to "─".
        """
        from .rule import Rule

        rule = Rule(title=title, characters=character or characters, style=style)
        self.print(rule)

    def control(self, control_codes: Union["Control", str]) -> None:
        """Insert non-printing control codes.

        Args:
            control_codes (str): Control codes, such as those that may move the cursor.
        """
        if not self.is_dumb_terminal:
            self._buffer.append(Segment.control(str(control_codes)))
            self._check_buffer()

    def print(
        self,
        *objects: Any,
        sep=" ",
        end="\n",
        style: Union[str, Style] = None,
        justify: JustifyMethod = None,
        overflow: OverflowMethod = None,
        no_wrap: bool = None,
        emoji: bool = None,
        markup: bool = None,
        highlight: bool = None,
        width: int = None,
        crop: bool = True,
    ) -> None:
        """Print to the console.

        Args:
            objects (positional args): Objects to log to the terminal.
            sep (str, optional): String to write between print data. Defaults to " ".
            end (str, optional): String to write at end of print data. Defaults to "\\n".
            style (Union[str, Style], optional): A style to apply to output. Defaults to None.
            justify (str, optional): Justify method: "default", "left", "right", "center", or "full". Defaults to ``None``.
            overflow (str, optional): Overflow method: "crop", "fold", or "ellipsis". Defaults to None.
            no_wrap (Optional[bool], optional): Disable word wrapping. Defaults to None.
            emoji (Optional[bool], optional): Enable emoji code, or ``None`` to use console default. Defaults to ``None``.
            markup (Optional[bool], optional): Enable markup, or ``None`` to use console default. Defaults to ``None``.
            highlight (Optional[bool], optional): Enable automatic highlighting, or ``None`` to use console default. Defaults to ``None``.
            width (Optional[int], optional): Width of output, or ``None`` to auto-detect. Defaults to ``None``.
            crop (Optional[bool], optional): Crop output to width of terminal. Defaults to True.
        """
        if not objects:
            self.line()
            return

        with self:
            renderables = self._collect_renderables(
                objects,
                sep,
                end,
                justify=justify,
                emoji=emoji,
                markup=markup,
                highlight=highlight,
            )
            for hook in self._render_hooks:
                renderables = hook.process_renderables(renderables)
            render_options = self.options.update(
                justify=justify, overflow=overflow, width=width, no_wrap=no_wrap
            )
            new_segments: List[Segment] = []
            extend = new_segments.extend
            render = self.render
            if style is None:
                for renderable in renderables:
                    extend(render(renderable, render_options))
            else:
                for renderable in renderables:
                    extend(
                        Segment.apply_style(
                            render(renderable, render_options), self.get_style(style)
                        )
                    )
            if crop:
                buffer_extend = self._buffer.extend
                for line in Segment.split_and_crop_lines(
                    new_segments, self.width, pad=False
                ):
                    buffer_extend(line)
            else:
                self._buffer.extend(new_segments)

    def print_exception(
        self,
        *,
        width: Optional[int] = 88,
        extra_lines: int = 3,
        theme: Optional[str] = None,
        word_wrap: bool = False,
    ) -> None:
        """Prints a rich render of the last exception and traceback.
        
        Args:
            code_width (Optional[int], optional): Number of characters used to render code. Defaults to 88.
            extra_lines (int, optional): Additional lines of code to render. Defaults to 3.
            theme (str, optional): Override pygments theme used in traceback
            word_wrap (bool, optional): Enable word wrapping of long lines. Defaults to False.
        """
        from .traceback import Traceback

        traceback = Traceback(
            width=width, extra_lines=extra_lines, theme=theme, word_wrap=word_wrap
        )
        self.print(traceback)

    def log(
        self,
        *objects: Any,
        sep=" ",
        end="\n",
        justify: JustifyMethod = None,
        emoji: bool = None,
        markup: bool = None,
        highlight: bool = None,
        log_locals: bool = False,
        _stack_offset=1,
    ) -> None:
        """Log rich content to the terminal.

        Args:
            objects (positional args): Objects to log to the terminal.
            sep (str, optional): String to write between print data. Defaults to " ".
            end (str, optional): String to write at end of print data. Defaults to "\\n".
            justify (str, optional): One of "left", "right", "center", or "full". Defaults to ``None``.
            overflow (str, optional): Overflow method: "crop", "fold", or "ellipsis". Defaults to None.
            emoji (Optional[bool], optional): Enable emoji code, or ``None`` to use console default. Defaults to None.
            markup (Optional[bool], optional): Enable markup, or ``None`` to use console default. Defaults to None.
            highlight (Optional[bool], optional): Enable automatic highlighting, or ``None`` to use console default. Defaults to None.
            log_locals (bool, optional): Boolean to enable logging of locals where ``log()``
                was called. Defaults to False.
            _stack_offset (int, optional): Offset of caller from end of call stack. Defaults to 1.
        """
        if not objects:
            self.line()
            return
        with self:
            renderables = self._collect_renderables(
                objects,
                sep,
                end,
                justify=justify,
                emoji=emoji,
                markup=markup,
                highlight=highlight,
            )

            caller = inspect.stack()[_stack_offset]
            link_path = (
                None
                if caller.filename.startswith("<")
                else os.path.abspath(caller.filename)
            )
            path = caller.filename.rpartition(os.sep)[-1]
            line_no = caller.lineno
            if log_locals:
                locals_map = {
                    key: value
                    for key, value in caller.frame.f_locals.items()
                    if not key.startswith("__")
                }
                renderables.append(render_scope(locals_map, title="[i]locals"))

            renderables = [
                self._log_render(
                    self, renderables, path=path, line_no=line_no, link_path=link_path,
                )
            ]
            for hook in self._render_hooks:
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

    def _check_buffer(self) -> None:
        """Check if the buffer may be rendered."""
        with self._lock:
            if self._buffer_index == 0:
                if self.is_jupyter:  # pragma: no cover
                    from .jupyter import display

                    display(self._buffer)
                    del self._buffer[:]
                else:
                    text = self._render_buffer()
                    if text:
                        try:
                            if WINDOWS:  # pragma: no cover
                                # https://bugs.python.org/issue37871
                                write = self.file.write
                                for line in text.splitlines(True):
                                    write(line)
                            else:
                                self.file.write(text)
                            self.file.flush()
                        except UnicodeEncodeError as error:
                            error.reason = f"{error.reason}\n*** You may need to add PYTHONIOENCODING=utf-8 to your environment ***"
                            raise

    def _render_buffer(self) -> str:
        """Render buffered output, and clear buffer."""
        output: List[str] = []
        append = output.append
        color_system = self._color_system
        legacy_windows = self.legacy_windows
        buffer = self._buffer[:]
        if self.record:
            with self._record_buffer_lock:
                self._record_buffer.extend(buffer)
        del self._buffer[:]
        not_terminal = not self.is_terminal
        for text, style, is_control in buffer:
            if style and not is_control:
                append(
                    style.render(
                        text, color_system=color_system, legacy_windows=legacy_windows,
                    )
                )
            else:
                if not (not_terminal and is_control):
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
        stream: TextIO = None,
    ) -> str:
        """Displays a prompt and waits for input from the user. The prompt may contain color / style. 

        Args:
            prompt (Union[str, Text]): Text to render in the prompt.
            markup (bool, optional): Enable console markup (requires a str prompt). Defaults to True.
            emoji (bool, optional): Enable emoji (requires a str prompt). Defaults to True.
            password: (bool, optional): Hide typed text. Defaults to False.
            stream: (TextIO, optional): Optional file to read input from (rather than stdin). Defaults to None.
        
        Returns:
            str: Text read from stdin.
        """
        if prompt:
            self.print(prompt, markup=markup, emoji=emoji, end="")
        result = (
            getpass("", stream=stream)
            if password
            else (stream.readline() if stream else input())
        )
        return result

    def export_text(self, *, clear: bool = True, styles: bool = False) -> str:
        """Generate text from console contents (requires record=True argument in constructor).

        Args:
            clear (bool, optional): Set to ``True`` to clear the record buffer after exporting.
            styles (bool, optional): If ``True``, ansi escape codes will be included. ``False`` for plain text.
                Defaults to ``False``.

        Returns:
            str: String containing console contents.

        """
        assert (
            self.record
        ), "To export console contents set record=True in the constructor or instance"

        with self._record_buffer_lock:
            if styles:
                text = "".join(
                    (style.render(text) if style else text)
                    for text, style, _ in self._record_buffer
                )
            else:
                text = "".join(
                    segment.text
                    for segment in self._record_buffer
                    if not segment.is_control
                )
            if clear:
                del self._record_buffer[:]
        return text

    def save_text(self, path: str, *, clear: bool = True, styles: bool = False) -> None:
        """Generate text from console and save to a given location (requires record=True argument in constructor).

        Args:
            path (str): Path to write text files.
            clear (bool, optional): Set to ``True`` to clear the record buffer after exporting.
            styles (bool, optional): If ``True``, ansi style codes will be included. ``False`` for plain text.
                Defaults to ``False``.

        """
        text = self.export_text(clear=clear, styles=styles)
        with open(path, "wt", encoding="utf-8") as write_file:
            write_file.write(text)

    def export_html(
        self,
        *,
        theme: TerminalTheme = None,
        clear: bool = True,
        code_format: str = None,
        inline_styles: bool = False,
    ) -> str:
        """Generate HTML from console contents (requires record=True argument in constructor).

        Args:
            theme (TerminalTheme, optional): TerminalTheme object containing console colors.
            clear (bool, optional): Set to ``True`` to clear the record buffer after generating the HTML.
            code_format (str, optional): Format string to render HTML, should contain {foreground}
                {background} and {code}.
            inline_styles (bool, optional): If ``True`` styles will be inlined in to spans, which makes files
                larger but easier to cut and paste markup. If ``False``, styles will be embedded in a style tag.
                Defaults to False.

        Returns:
            str: String containing console contents as HTML.
        """
        assert (
            self.record
        ), "To export console contents set record=True in the constructor or instance"
        fragments: List[str] = []
        append = fragments.append
        _theme = theme or DEFAULT_TERMINAL_THEME
        stylesheet = ""

        def escape(text: str) -> str:
            """Escape html."""
            return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

        render_code_format = CONSOLE_HTML_FORMAT if code_format is None else code_format

        with self._record_buffer_lock:
            if inline_styles:
                for text, style, _ in Segment.filter_control(
                    Segment.simplify(self._record_buffer)
                ):
                    text = escape(text)
                    if style:
                        rule = style.get_html_style(_theme)
                        text = f'<span style="{rule}">{text}</span>' if rule else text
                        if style.link:
                            text = f'<a href="{style.link}">{text}</a>'
                    append(text)
            else:
                styles: Dict[str, int] = {}
                for text, style, _ in Segment.filter_control(
                    Segment.simplify(self._record_buffer)
                ):
                    text = escape(text)
                    if style:
                        rule = style.get_html_style(_theme)
                        if rule:
                            style_number = styles.setdefault(rule, len(styles) + 1)
                            text = f'<span class="r{style_number}">{text}</span>'
                        if style.link:
                            text = f'<a href="{style.link}">{text}</a>'
                    append(text)
                stylesheet_rules: List[str] = []
                stylesheet_append = stylesheet_rules.append
                for style_rule, style_number in styles.items():
                    if style_rule:
                        stylesheet_append(f".r{style_number} {{{style_rule}}}")
                stylesheet = "\n".join(stylesheet_rules)

            rendered_code = render_code_format.format(
                code="".join(fragments),
                stylesheet=stylesheet,
                foreground=_theme.foreground_color.hex,
                background=_theme.background_color.hex,
            )
            if clear:
                del self._record_buffer[:]
        return rendered_code

    def save_html(
        self,
        path: str,
        *,
        theme: TerminalTheme = None,
        clear: bool = True,
        code_format=CONSOLE_HTML_FORMAT,
        inline_styles: bool = False,
    ) -> None:
        """Generate HTML from console contents and write to a file (requires record=True argument in constructor).

        Args:
            path (str): Path to write html file.
            theme (TerminalTheme, optional): TerminalTheme object containing console colors.
            clear (bool, optional): Set to True to clear the record buffer after generating the HTML.
            code_format (str, optional): Format string to render HTML, should contain {foreground}
                {background} and {code}.
            inline_styes (bool, optional): If ``True`` styles will be inlined in to spans, which makes files
                larger but easier to cut and paste markup. If ``False``, styles will be embedded in a style tag.
                Defaults to False.

        """
        html = self.export_html(
            theme=theme,
            clear=clear,
            code_format=code_format,
            inline_styles=inline_styles,
        )
        with open(path, "wt", encoding="utf-8") as write_file:
            write_file.write(html)


if __name__ == "__main__":  # pragma: no cover
    console = Console()

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

    console.log("Hello, World!", "{'a': 1}", repr(console))

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
                            "Golden State Warriros",
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
    console.log("foo")
