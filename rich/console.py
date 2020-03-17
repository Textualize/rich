from collections import ChainMap
from collections.abc import Mapping, Sequence
from contextlib import contextmanager
from dataclasses import dataclass, field, replace
from enum import Enum
from functools import wraps
import inspect
from itertools import chain
import os
from operator import itemgetter
import platform
import re
import shutil
import sys
import threading
from typing import (
    Any,
    Callable,
    Dict,
    IO,
    Iterable,
    List,
    Optional,
    NamedTuple,
    overload,
    Tuple,
    TYPE_CHECKING,
    Union,
)
from typing_extensions import Protocol, runtime_checkable, Literal


from ._emoji_replace import _emoji_replace

from .markup import render as render_markup
from .measure import measure_renderables, Measurement
from ._log_render import LogRender
from .default_styles import DEFAULT_STYLES
from . import errors
from .color import ColorSystem
from .control import Control
from .highlighter import NullHighlighter, ReprHighlighter
from .pretty import Pretty
from .style import Style
from .tabulate import tabulate_mapping
from . import highlighter
from . import themes
from .pretty import Pretty
from .terminal_theme import TerminalTheme, DEFAULT_TERMINAL_THEME
from .segment import Segment
from .text import Text
from .theme import Theme

if TYPE_CHECKING:  # pragma: no cover
    from .text import Text

WINDOWS = platform.system() == "Windows"

HighlighterType = Callable[[Union[str, "Text"]], "Text"]
JustifyValues = Optional[Literal["left", "center", "right", "full"]]


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


@dataclass
class ConsoleOptions:
    """Options for __console__ method."""

    min_width: int
    max_width: int
    is_terminal: bool
    encoding: str
    justify: Optional[JustifyValues] = None

    def update(
        self,
        width: int = None,
        min_width: int = None,
        max_width: int = None,
        justify: JustifyValues = None,
    ):
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
        return options


@runtime_checkable
class RichCast(Protocol):
    """An object that may be 'cast' to a console renderable."""

    def __rich__(self) -> Union["ConsoleRenderable", str]:  # pragma: no cover
        ...


@runtime_checkable
class ConsoleRenderable(Protocol):
    """An object that supports the console protocol."""

    def __console__(
        self, console: "Console", options: "ConsoleOptions"
    ) -> "RenderResult":  # pragma: no cover
        ...


"""A type that may be rendered by Console."""
RenderableType = Union[ConsoleRenderable, RichCast, Control, str]

"""The result of calling a __console__ method."""
RenderResult = Iterable[Union[RenderableType, Segment, Control]]


_null_highlighter = NullHighlighter()


class RichRenderable:
    def __init__(self, rich_cast: Callable[[], ConsoleRenderable]) -> None:
        self.rich_cast = rich_cast

    def __console__(
        self, console: "Console", options: "ConsoleOptions"
    ) -> RenderResult:
        yield self.rich_cast()


class RenderGroup:
    def __init__(
        self, renderables: Iterable[RenderableType], fit: bool = False
    ) -> None:
        """Takes a group of renderables and returns a renderable object,
        that renders the group.
        
        Args:
            renderables (Iterable[RenderableType]): An iterable of renderable objects.
        """
        self._renderables = renderables
        self.fit = fit
        self._render: Optional[List[RenderableType]] = None

    @property
    def renderables(self) -> List["RenderableType"]:
        if self._render is None:
            self._render = list(self._renderables)
        return self._render

    def __measure__(self, console: "Console", max_width: int) -> "Measurement":
        if self.fit:
            return measure_renderables(console, self.renderables, max_width)
        else:
            return Measurement(max_width, max_width)

    def __console__(
        self, console: "Console", options: "ConsoleOptions"
    ) -> RenderResult:
        yield from self.renderables


def render_group(fit: bool = False) -> Callable:
    def decorator(method):
        """Convert a method that returns an iterable of renderables in to a RenderGroup."""

        @wraps(method)
        def _replace(*args, **kwargs):
            renderables = method(*args, **kwargs)
            return RenderGroup(renderables, fit=fit)

        return _replace

    return decorator


class ConsoleDimensions(NamedTuple):
    """Size of the terminal."""

    width: int
    height: int


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
    style_stack: List[Style] = field(default_factory=lambda: [Style()])
    control: List[str] = field(default_factory=list)


class Console:
    """A high level console interface.

    Args:
        color_system (str, optional): The color system supported by your terminal,
            either ``"standard"``, ``"256"`` or ``"truecolor"``. Leave as ``"auto"`` to autodetect.
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
        highlighter(HighlighterType, optional): Default highlighter.    
    """

    def __init__(
        self,
        color_system: Optional[
            Literal["auto", "standard", "256", "truecolor", "windows"]
        ] = "auto",
        theme: Theme = None,
        file: IO = None,
        width: int = None,
        height: int = None,
        tab_size: int = 8,
        record: bool = False,
        markup: bool = True,
        emoji: bool = True,
        highlight: bool = True,
        log_time: bool = True,
        log_path: bool = True,
        log_time_format: str = "[%X] ",
        highlighter: Optional["HighlighterType"] = ReprHighlighter(),
    ):
        self._styles = ChainMap(
            themes.DEFAULT.styles if theme is None else theme.styles
        )
        self.file = file or sys.stdout
        self._width = width
        self._height = height
        self.tab_size = tab_size
        self.record = record
        self._markup = markup
        self._emoji = emoji
        self._highlight = highlight

        if color_system is None:
            self._color_system = None
        elif color_system == "auto":
            self._color_system = self._detect_color_system()
        else:
            self._color_system = COLOR_SYSTEMS[color_system]

        self._log_render = LogRender(
            show_time=log_time, show_path=log_path, time_format=log_time_format
        )
        self.highlighter: HighlighterType = highlighter or _null_highlighter

        self._record_buffer_lock = threading.RLock()
        self._thread_locals = ConsoleThreadLocals()
        self._record_buffer: List[Segment] = []

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

    @property
    def _style_stack(self) -> List[Style]:
        """Get a thread local style stack."""
        return self._thread_locals.style_stack

    @property
    def _control(self) -> List[str]:
        """Get control codes buffer."""
        return self._thread_locals.control

    def _detect_color_system(self) -> Optional[ColorSystem]:
        """Detect color system from env vars."""
        if not self.is_terminal:
            return None
        if os.environ.get("COLORTERM", "").strip().lower() in ("truecolor", "24bit"):
            return ColorSystem.TRUECOLOR
        # 256 can be considered standard nowadays
        return ColorSystem.EIGHT_BIT

    def _enter_buffer(self) -> None:
        """Enter in to a buffer context, and buffer all output."""
        self._buffer_index += 1

    def _exit_buffer(self) -> None:
        """Leave buffer context, and render content if required."""
        self._buffer_index -= 1
        self._check_buffer()

    def __enter__(self) -> "Console":
        """Own context manager to enter buffer context."""
        self._enter_buffer()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """Exit buffer context."""
        self._exit_buffer()

    def push_styles(self, styles: Dict[str, Style]) -> None:
        """Merge set of styles with currently active styles.

        Args:
            styles (Dict[str, Style]): A mapping of style name to Style instance.
        """
        self._styles.maps.append(styles)

    def pop_styles(self) -> None:
        """Restore styles to state before `push_styles`."""
        self._styles.maps.pop()

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
            bool: True if the console writting to a device capable of
            understanding terminal codes, otherwise False.
        """
        isatty = getattr(self.file, "isatty", None)
        return False if isatty is None else isatty()

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

        width, height = shutil.get_terminal_size()
        return ConsoleDimensions(
            width if self._width is None else self._width,
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

    def show_cursor(self, show: bool = True) -> None:
        """Show or hide the cursor.
        
        Args:
            show (bool, optional): Set visibility of the cursor.
        """
        self._check_buffer()
        self.file.write("\033[?25h" if show else "\033[?25l")

    def _render(
        self,
        renderable: Union[RenderableType, Segment, Control],
        options: Optional[ConsoleOptions],
    ) -> Iterable[Segment]:
        """Render an object in to an iterable of `Segment` instances.

        This method contains the logic for rendering objects with the console protocol.
        You are unlikely to need to use it directly, unless you are extending the library.

        Args:
            renderable (RenderableType): An object supporting the console protocol, or
                an object that may be converted to a string.
            options (ConsoleOptions, optional): An options objects. Defaults to None.

        Returns:
            Iterable[Segment]: An iterable of segments that may be rendered.
        """
        render_iterable: RenderResult
        if isinstance(renderable, Segment):
            yield renderable
            return
        if isinstance(renderable, Control):
            self._control.append(renderable.codes)
            return
        render_options = options or self.options
        if isinstance(renderable, ConsoleRenderable):
            render_iterable = renderable.__console__(self, render_options)
        elif isinstance(renderable, str):
            yield from self.render(self.render_str(renderable), render_options)
            return
        else:
            raise errors.NotRenderableError(
                f"Unable to render {renderable!r}; "
                "A str, Segment or object with __console__ method is required"
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
                yield from self.render(render_output, render_options)

    def render(
        self, renderable: RenderableType, options: Optional[ConsoleOptions]
    ) -> Iterable[Segment]:
        """Render an object in to an iterable of `Segment` instances.

        This method contains the logic for rendering objects with the console protocol.
        You are unlikely to need to use it directly, unless you are extending the library.


        Args:
            renderable (RenderableType): An object supporting the console protocol, or
                an object that may be converted to a string.
            options (ConsoleOptions, optional): An options objects. Defaults to None.

        Returns:
            Iterable[Segment]: An iterable of segments that may be rendered.
        """

        yield from self._render(renderable, options)

    def render_all(
        self, renderables: Iterable[RenderableType], options: Optional[ConsoleOptions]
    ) -> Iterable[Segment]:
        """Render a number of console objects.

        Args:
            renderables (Iterable[RenderableType]): Console objects.
            options (Optional[ConsoleOptions]): Options for render.

        Returns:
            Iterable[Segment]: Segments to be written to the console.

        """
        render_options = options or self.options
        for renderable in renderables:
            yield from self.render(renderable, render_options)

    def render_lines(
        self,
        renderable: RenderableType,
        options: Optional[ConsoleOptions],
        style: Optional[Style] = None,
        pad: bool = True,
    ) -> List[List[Segment]]:
        """Render objects in to a list of lines.

        The output of render_lines is useful when further formatting of rendered console text
        is required, such as the Panel class which draws a border around any renderable object.

        Args:
            renderables (Iterable[RenderableType]): Any object or objects renderable in the console.
            options (Optional[ConsoleOptions]): Console options used to render with.

        Returns:
            List[List[Segment]]: A list of lines, where a line is a list of Segment objects.
        """
        render_options = options or self.options
        with self:
            _rendered = self.render(renderable, render_options)
            if style is not None:
                _rendered = Segment.apply_style(_rendered, style)
            lines = list(
                Segment.split_and_crop_lines(
                    _rendered,
                    render_options.max_width,
                    style=style,
                    include_new_lines=False,
                    pad=pad,
                )
            )
        return lines

    def render_str(
        self,
        text: str,
        style: Union[str, Style] = "",
        emoji: bool = None,
        markup: bool = None,
    ) -> "Text":
        """Convert a string to a Text instance.

        Args:
            text (str): Text to render.
            style (Union[str, Style], optional): Style to apply to rendered text.
            emoji (Optional[bool], optional): Enable emoji, or ``None`` to use Console default.
            markup (Optional[bool], optional): Enable markup, or ``None`` to use Console default.
        Returns:
            ConsoleRenderable: Renderable object.

        """
        if emoji or (emoji is None and self._emoji):
            text = _emoji_replace(text)

        if markup or (markup is None and self._markup):
            return render_markup(text, style=style)

        return Text(text, style=style)

    def _get_style(self, name: str) -> Optional[Style]:
        """Get a named style, or `None` if it doesn't exist.

        Args:
            name (str): The name of a style.

        Returns:
            Optional[Style]: A Style object for the given name, or `None`.
        """
        return self._styles.get(name, None)

    def get_style(
        self, name: Union[str, Style], *, default: Union[Style, str] = None
    ) -> Style:
        """Get a style merged with the current style.

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
            return self._styles.get(name) or Style.parse(name)
        except errors.StyleSyntaxError as error:
            if default is not None:
                return self.get_style(default)
            if " " in name:
                raise
            raise errors.MissingStyle(f"No style named {name!r}; {error}")

    def _collect_renderables(
        self,
        objects: Iterable[Any],
        sep: str,
        end: str,
        emoji: bool = None,
        markup: bool = None,
        highlight: bool = None,
    ) -> List[ConsoleRenderable]:
        """Combined a number of renderables and text in to one renderable.

        Args:
            renderables (Iterable[Union[str, ConsoleRenderable]]): Anyting that Rich can render.
            sep (str, optional): String to write between print data. Defaults to " ".
            end (str, optional): String to write at end of print data. Defaults to "\n".            
            emoji (Optional[bool], optional): Enable emoji code, or ``None`` to use console default.
            markup (Optional[bool], optional): Enable markup, or ``None`` to use console default.
            highlight (Optional[bool], optional): Enable automatic highlighting, or ``None`` to use console default.

        Returns:
            List[ConsoleRenderable]: A list of things to render.
        """
        sep_text = Text(sep, end=end)
        renderables: List[ConsoleRenderable] = []
        append = renderables.append
        text: List[Text] = []
        append_text = text.append

        _highlighter: HighlighterType
        if highlight or (highlight is None and self._highlight):
            _highlighter = self.highlighter
        else:
            _highlighter = _null_highlighter

        def check_text() -> None:
            if text:
                append(sep_text.join(text))
                del text[:]

        for renderable in objects:
            rich_cast = getattr(renderable, "__rich__", None)
            if rich_cast:
                renderable = rich_cast()
            if isinstance(renderable, str):
                append_text(
                    _highlighter(
                        self.render_str(renderable, emoji=emoji, markup=markup)
                    )
                )
            elif isinstance(renderable, Text):
                append_text(renderable)
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
        character: str = "─",
        style: Union[str, Style] = "rule.line",
    ) -> None:
        """Draw a line with optional centered title.
        
        Args:
            title (str, optional): Text to render over the rule. Defaults to "".
            character (str, optional): Character to form the line. Defaults to "─".
        """
        from .rule import Rule

        rule = Rule(title=title, character=character, style=style)
        self.print(rule)

    def print(
        self,
        *objects: Any,
        sep=" ",
        end="\n",
        style: Union[str, Style] = None,
        emoji: bool = None,
        markup: bool = None,
        highlight: bool = None,
    ) -> None:
        r"""Print to the console.

        Args:
            objects (positional args): Objects to log to the terminal.
            sep (str, optional): String to write between print data. Defaults to " ".
            end (str, optional): String to write at end of print data. Defaults to "\n".
            style (Union[str, Style], optional): A style to apply to output. Defaults to None.
            emoji (Optional[bool], optional): Enable emoji code, or ``None`` to use console default. Defaults to None.
            markup (Optional[bool], optional): Enable markup, or ``None`` to use console default. Defaults to None
            highlight (Optional[bool], optional): Enable automatic highlighting, or ``None`` to use console default. Defaults to None.
        """
        if not objects:
            self.line()
            return

        with self:
            renderables = self._collect_renderables(
                objects, sep, end, emoji=emoji, markup=markup, highlight=highlight
            )
            render_options = self.options
            extend = self._buffer.extend
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

    def print_exception(
        self,
        width: Optional[int] = 88,
        extra_lines: int = 3,
        theme: Optional[str] = None,
    ) -> None:
        """Prints a rich render of the last exception and traceback.
        
        Args:
            code_width (Optional[int], optional): Number of characters used to render code. Defaults to 88.
            extra_lines (int, optional): Additional lines of code to render. Defaults to 3.
            theme (str, optional): Override pygments theme used in traceback
        """
        from .traceback import Traceback

        traceback = Traceback(width=width, extra_lines=extra_lines, theme=theme)
        self.print(traceback)

    def log(
        self,
        *objects: Any,
        sep=" ",
        end="\n",
        emoji: bool = None,
        markup: bool = None,
        highlight: bool = None,
        log_locals: bool = False,
        _stack_offset=1,
    ) -> None:
        r"""Log rich content to the terminal.

        Args:
            objects (positional args): Objects to log to the terminal.
            sep (str, optional): String to write between print data. Defaults to " ".
            end (str, optional): String to write at end of print data. Defaults to "\n".
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
        renderables = self._collect_renderables(
            objects, sep, end, emoji=emoji, markup=markup, highlight=highlight
        )

        caller = inspect.stack()[_stack_offset]
        path = caller.filename.rpartition(os.sep)[-1]
        line_no = caller.lineno
        if log_locals:
            locals_map = {
                key: value
                for key, value in caller.frame.f_locals.items()
                if not key.startswith("__")
            }
            renderables.append(tabulate_mapping(locals_map, title="Locals"))

        with self:
            self._buffer.extend(
                self.render(
                    self._log_render(self, renderables, path=path, line_no=line_no),
                    self.options,
                )
            )

    def _check_buffer(self) -> None:
        """Check if the buffer may be rendered."""
        if self._buffer_index == 0:
            text = self._render_buffer()
            self.file.write(text)
            self.file.flush()

    def _render_buffer(self) -> str:
        """Render buffered output, and clear buffer."""
        output: List[str] = []
        append = output.append
        color_system = self._color_system
        buffer = self._buffer[:]
        if self.record:
            with self._record_buffer_lock:
                self._record_buffer.extend(buffer)
        del self._buffer[:]
        for line in Segment.split_and_crop_lines(buffer, self.width, pad=False):
            for text, style in line:
                if style:
                    append(style.render(text, color_system=color_system))
                else:
                    append(text)

        rendered = "".join(self._control) + "".join(output)
        del self._control[:]
        return rendered

    def export_text(self, clear: bool = True, styles: bool = False) -> str:
        """Generate text from console contents (requires record=True argument in constructor).

        Args:
            clear (bool, optional): Set to ``True`` to clear the record buffer after exporting.
            styles (bool, optional): If ``True``, ansi style codes will be included. ``False`` for plain text.
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
                    for text, style in self._record_buffer
                )
            else:
                text = "".join(text for text, _ in self._record_buffer)
            if clear:
                del self._record_buffer[:]
        return text

    def save_text(self, path: str, clear: bool = True, styles: bool = False) -> None:
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
            inline_styes (bool, optional): If ``True`` styles will be inlined in to spans, which makes files
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
                for text, style in Segment.simplify(self._record_buffer):
                    text = escape(text)
                    if style:
                        rule = style.get_html_style(_theme)
                        append(f'<span style="{rule}">{text}</span>' if rule else text)
                    else:
                        append(text)
            else:
                styles: Dict[str, int] = {}
                for text, style in Segment.simplify(self._record_buffer):
                    text = escape(text)
                    if style:
                        rule = style.get_html_style(_theme)
                        if rule:
                            style_number = styles.setdefault(rule, len(styles) + 1)
                            append(f'<span class="r{style_number}">{text}</span>')
                        else:
                            append(text)
                    else:
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

    console.log(
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

