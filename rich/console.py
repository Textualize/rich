from collections import ChainMap
from collections.abc import Mapping, Sequence
from contextlib import contextmanager
from dataclasses import dataclass, replace
from enum import Enum
import inspect
from itertools import chain
import os
from operator import itemgetter
import re
import shutil
import sys
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

from . import markup
from .render_width import RenderWidth
from ._log_render import LogRender
from .default_styles import DEFAULT_STYLES
from . import errors
from .color import ColorSystem
from .highlighter import NullHighlighter, ReprHighlighter
from .pretty import Pretty
from .style import Style
from .tabulate import tabulate_mapping
from . import highlighter
from . import themes
from .pretty import Pretty
from .theme import Theme
from .segment import Segment

if TYPE_CHECKING:  # pragma: no cover
    from .text import Text

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
class ConsoleRenderable(Protocol):
    """An object that supports the console protocol."""

    def __console__(
        self, console: "Console", options: "ConsoleOptions"
    ) -> Iterable[Union["ConsoleRenderable", Segment]]:  # pragma: no cover
        ...


RenderableType = Union[ConsoleRenderable, Segment, str]
RenderResult = Iterable[Union[ConsoleRenderable, Segment]]


_null_highlighter = NullHighlighter()


class ConsoleDimensions(NamedTuple):
    """Size of the terminal."""

    width: int
    height: int


class StyleContext:
    """A context manager to manage a style."""

    def __init__(self, console: "Console", style: Optional[Style]):
        self.console = console
        self.style = style

    def __enter__(self) -> "Console":
        if self.style is not None:
            self.console.push_style(self.style)
        self.console._enter_buffer()
        return self.console

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.console._exit_buffer()
        if self.style is not None:
            self.console.pop_style()


COLOR_SYSTEMS = {
    "standard": ColorSystem.STANDARD,
    "256": ColorSystem.EIGHT_BIT,
    "truecolor": ColorSystem.TRUECOLOR,
}


_COLOR_SYSTEMS_NAMES = {system: name for name, system in COLOR_SYSTEMS.items()}


class Console:
    """A high level console interface.

    Args:
        color_system (str, optional): The color system supported by your terminal,
            either ``"standard"``, ``"256"`` or ``"truecolor"``. Leave as ``"auto"`` to autodetect.
        styles (Dict[str, Style], optional): An optional mapping of style name strings to :class:`~rich.style.Style` objects.
        file (IO, optional): A file object where the console should write to. Defaults to stdoutput.
        width (int, optional): The width of the terminal. Leave as default to auto-detect width.
        height (int, optional): The height of the terminal. Leave as default to auto-detect height.
        record (bool, optional): Boolean to enable recording of terminal output,
            required to call :meth:`export_html` and :meth:`export_text`. Defaults to False.
        markup (bool, optional): Boolean to enable :ref:`console_markup`. Defaults to True.
        log_time (bool, optional): Boolean to enable logging of time by :meth:`log` methods. Defaults to True.
        log_path (bool, optional): Boolean to enable the logging of the caller by :meth:`log`. Defaults to True.
        log_time_format (str, optional): Log time format if ``log_time`` is enabled. Defaults to "[%X] ".
        highlighter(HighlighterType, optional): Default highlighter.    
    """

    def __init__(
        self,
        color_system: Optional[
            Literal["auto", "standard", "256", "truecolor"]
        ] = "auto",
        styles: Dict[str, Style] = None,
        file: IO = None,
        width: int = None,
        height: int = None,
        record: bool = False,
        markup: bool = True,
        log_time: bool = True,
        log_path: bool = True,
        log_time_format: str = "[%X] ",
        highlighter: Optional["HighlighterType"] = ReprHighlighter(),
    ):
        self._styles = ChainMap(DEFAULT_STYLES if styles is None else styles)
        self.file = file or sys.stdout
        self._width = width
        self._height = height
        self.record = record
        self._markup = markup

        if color_system is None:
            self._color_system = None
        elif color_system == "auto":
            self._color_system = self._detect_color_system()
        else:
            self._color_system = COLOR_SYSTEMS[color_system]

        self.buffer: List[Segment] = []
        self._buffer_index = 0
        self._record_buffer: List[Segment] = []

        default_style = Style()
        self.style_stack: List[Style] = [default_style]
        self.current_style = default_style

        self._log_render = LogRender(
            show_time=log_time, show_path=log_path, time_format=log_time_format
        )
        self.highlighter: HighlighterType = highlighter or _null_highlighter

    def __repr__(self) -> str:
        return f"<console width={self.width} {str(self._color_system)}>"

    def _detect_color_system(self,) -> Optional[ColorSystem]:
        """Detect color system from env vars."""
        if not self.is_terminal:
            return None
        if os.environ.get("COLORTERM", "").strip().lower() == "truecolor":
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
            self.buffer.append(Segment("\n" * count))
            self._check_buffer()

    def _render(
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
        render_iterable: Iterable[RenderableType]
        render_options = options or self.options
        if isinstance(renderable, Segment):
            yield renderable
            return
        elif isinstance(renderable, ConsoleRenderable):
            render_iterable = renderable.__console__(self, render_options)
        elif isinstance(renderable, str):
            from .text import Text

            yield from self._render(Text(renderable), render_options)
            return
        else:
            raise errors.NotRenderableError(
                f"Unable to render {renderable!r}; "
                "A str, Segment or object with __console__ method is required"
            )

        for render_output in render_iterable:
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
        yield from Segment.apply_style(
            self._render(renderable, options), self.current_style
        )

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

        with self.style(style or "none"):
            _rendered = self.render(renderable, render_options)
            lines = list(
                Segment.split_and_crop_lines(
                    _rendered, render_options.max_width, style=style
                )
            )
        return lines

    def render_str(self, text: str) -> "Text":
        """Convert a string to a Text instance.

        Args:
            text (str): Text to render.

        Returns:
            ConsoleRenderable: Renderable object.

        """
        if self._markup:
            return markup.render(text)

        return markup.render_text(text)

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

    def push_style(self, style: Union[str, Style]) -> None:
        """Push a style on to the stack.

        The new style will be applied to all `write` calls, until
        `pop_style` is called.

        Args:
            style (Union[str, Style]): New style to merge with current style.

        Returns:
            None: [description]
        """
        if isinstance(style, str):
            style = self.get_style(style)
        self.current_style = self.current_style + style
        self.style_stack.append(self.current_style)

    def pop_style(self) -> Style:
        """Pop a style from the stack.

        This will revert to the style applied prior to the corresponding `push_style`.

        Returns:
            Style: The previously applied style.
        """
        if len(self.style_stack) == 1:
            raise errors.StyleStackError(
                "Can't pop the default style (check there is `push_style` for every `pop_style`)"
            )
        style = self.style_stack.pop()
        self.current_style = self.style_stack[-1]
        return style

    def style(self, style: Optional[Union[str, Style]]) -> StyleContext:
        """A context manager to apply a new style.

        Example:
            with context.style("bold red"):
                context.print("Danger Will Robinson!")

        Args:
            style (Union[str, Style]): New style to apply.

        Returns:
            StyleContext: A style context manager.
        """
        if style is None:
            return StyleContext(self, None)
        if isinstance(style, str):
            _style = self.get_style(style)
        else:
            if not isinstance(style, Style):
                raise TypeError(f"style must be a str or Style instance, not {style!r}")
            _style = style
        return StyleContext(self, _style)

    def _collect_renderables(
        self,
        objects: Iterable[Any],
        sep: str,
        end: str,
        emoji=True,
        highlight: bool = True,
    ) -> List[ConsoleRenderable]:
        """Combined a number of renderables and text in to one renderable.

        Args:
            renderables (Iterable[Union[str, ConsoleRenderable]]): [description]
            sep (str, optional): String to write between print data. Defaults to " ".
            end (str, optional): String to write at end of print data. Defaults to "\n".            
            emoji (bool): If True, emoji codes will be replaced, otherwise emoji codes will be left in.
            highlight (bool, optional): Perform highlighting. Defaults to True.

        Returns:
            List[ConsoleRenderable]: A list of things to render.
        """
        from .text import Text

        sep_text = Text(sep)
        end_text = Text(end)
        renderables: List[ConsoleRenderable] = []
        append = renderables.append
        text: List[Text] = []
        append_text = text.append

        _highlighter: HighlighterType
        if highlight:
            _highlighter = self.highlighter
        else:
            _highlighter = _null_highlighter

        def check_text() -> None:
            if text:
                if end:
                    append_text(end_text)
                append(sep_text.join(text))
                del text[:]

        for renderable in objects:
            if isinstance(renderable, ConsoleRenderable):
                check_text()
                append(renderable)
                continue
            console_str_callable = getattr(renderable, "__console_str__", None)
            if console_str_callable is not None:
                append_text(console_str_callable())
                continue
            if isinstance(renderable, str):
                render_str = renderable
                if emoji:
                    render_str = _emoji_replace(render_str)
                render_text = self.render_str(render_str)
                append_text(_highlighter(render_text))
            elif isinstance(renderable, Text):
                append_text(renderable)
            elif isinstance(renderable, (int, float, bool, bytes, type(None))):
                append_text(_highlighter(repr(renderable)))
            elif isinstance(renderable, (Mapping, Sequence)):
                check_text()
                append(Pretty(renderable, highlighter=_highlighter))
            else:
                append_text(_highlighter(repr(renderable)))

        check_text()
        return renderables

    def rule(self, title: str = "", character: str = "─") -> None:
        """Draw a line with optional centered title.
        
        Args:
            title (str, optional): Text to render over the rule. Defaults to "".
            character (str, optional): Character to form the line. Defaults to "─".
        """

        from .text import Text

        width = self.width

        if not title:
            self.print(Text(character * width, "rule.line"))
        else:
            title_text = Text.from_markup(title, "rule.text")
            if len(title_text) > width - 4:
                title_text.set_length(width - 4)

            rule_text = Text()

            center = (width - len(title_text)) // 2
            rule_text.append(character * (center - 1) + " ", "rule.line")
            rule_text.append(title_text)
            rule_text.append(
                " " + character * (width - len(rule_text) - 1), "rule.line"
            )
            self.print(rule_text)

    def print(
        self,
        *objects: Any,
        sep=" ",
        end="\n",
        style: Union[str, Style] = None,
        emoji=True,
        highlight: bool = True,
    ) -> None:
        r"""Print to the console.

        Args:

            objects (positional args): Objects to log to the terminal.
            sep (str, optional): String to write between print data. Defaults to " ".
            end (str, optional): String to write at end of print data. Defaults to "\n".
            style (Union[str, Style], optional): A style to apply to output. Defaults to None.
            emoji (bool): If True, emoji codes will be replaced, otherwise emoji codes will be left in.
            highlight (bool, optional): Perform highlighting. Defaults to True.
        """
        if not objects:
            self.line()
            return

        renderables = self._collect_renderables(
            objects, sep=sep, end=end, emoji=emoji, highlight=highlight,
        )

        render_options = self.options
        extend = self.buffer.extend
        render = self.render
        with self.style(style):
            for renderable in renderables:
                extend(render(renderable, render_options))

    def log(
        self,
        *objects: Any,
        sep=" ",
        end="\n",
        highlight: bool = True,
        log_locals: bool = False,
        _stack_offset=1,
    ) -> None:
        r"""Log rich content to the terminal.

        Args:
            objects (positional args): Objects to log to the terminal.
            sep (str, optional): String to write between print data. Defaults to " ".
            end (str, optional): String to write at end of print data. Defaults to "\n".
            highlight (bool, optional): Perform highlighting. Defaults to True.
            log_locals (bool, optional): Boolean to enable logging of locals where ``log()``
                was called. Defaults to False.
            _stack_offset (int, optional): Offset of caller from end of call stack. Defaults to 1.
        """
        if not objects:
            self.line()
            return
        renderables = self._collect_renderables(
            objects, sep=sep, end=end, highlight=highlight
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
            self.buffer.extend(
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

    def _render_buffer(self) -> str:
        """Render buffered output, and clear buffer."""
        output: List[str] = []
        append = output.append
        color_system = self._color_system
        buffer = self.buffer[:]
        if self.record:
            self._record_buffer.extend(buffer)
        del self.buffer[:]
        for line in Segment.split_and_crop_lines(buffer, self.width):
            for text, style in line:
                if style:
                    append(style.render(text, color_system=color_system, reset=True))
                else:
                    append(text)
            append("\n")
        rendered = "".join(output)
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
        if styles:
            text = "".join(
                (style.render(text, reset=True) if style else text)
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
        with open(path, "wt") as write_file:
            write_file.write(text)

    def export_html(
        self,
        theme: Theme = None,
        clear: bool = True,
        code_format: str = None,
        inline_styles: bool = False,
    ) -> str:
        """Generate HTML from console contents (requires record=True argument in constructor).

        Args:
            theme (Theme, optional): Theme object containing console colors.
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
        _theme = theme or themes.DEFAULT
        stylesheet = ""

        def escape(text: str) -> str:
            """Escape html."""
            return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

        render_code_format = CONSOLE_HTML_FORMAT if code_format is None else code_format

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
        theme: Theme = None,
        clear: bool = True,
        code_format=CONSOLE_HTML_FORMAT,
        inline_styles: bool = False,
    ) -> None:
        """Generate HTML from console contents and write to a file (requires record=True argument in constructor).

        Args:
            path (str): Path to write html file.
            theme (Theme, optional): Theme object containing console colors.
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
        with open(path, "wt") as write_file:
            write_file.write(html)


if __name__ == "__main__":  # pragma: no cover
    console = Console()

    with console.style("dim on black"):
        console.print("[b]Hello[/b], [i]World[/i]!")
        console.print("Hello, *World*!")

    console.log(
        "JSONRPC *request*",
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

    console.log("# Hello, **World**!")
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

