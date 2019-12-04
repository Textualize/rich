from __future__ import annotations


from collections import ChainMap
from contextlib import contextmanager
from dataclasses import dataclass, replace
from enum import Enum
from itertools import chain
import os
from operator import itemgetter
import re
import shutil
import sys
from typing import (
    Any,
    Dict,
    IO,
    Iterable,
    List,
    Optional,
    NamedTuple,
    overload,
    Protocol,
    Tuple,
    runtime_checkable,
    Union,
)
from typing_extensions import Literal

from ._emoji_replace import _emoji_replace
from .default_styles import DEFAULT_STYLES
from . import errors
from .color import ColorSystem
from .style import Style
from . import themes
from .theme import Theme
from .segment import Segment


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

    max_width: int
    is_terminal: bool
    encoding: str
    min_width: int = 1
    justify: Optional[JustifyValues] = None

    def copy(self) -> ConsoleOptions:
        """Get a copy of this object.
        
        Returns:
            ConsoleOptions: New instance with same settings.
        """
        return replace(self)

    def with_width(self, width: int) -> ConsoleOptions:
        """Get a new console options with a changed width.
        
        Args:
            width (int): New min and max_width.
        
        Returns:
            ConsoleOptions: new ConsoleOptions instance.
        """
        return replace(self, min_width=width, max_width=width)


class SupportsStr(Protocol):
    def __str__(self) -> str:
        ...


@runtime_checkable
class ConsoleRenderable(Protocol):
    """An object that supports the console protocol."""

    def __console__(
        self, console: Console, options: ConsoleOptions
    ) -> Iterable[Union[ConsoleRenderable, Segment]]:
        ...


RenderableType = Union[ConsoleRenderable, Segment, str]
RenderResult = Iterable[Union[ConsoleRenderable, Segment]]


class ConsoleDimensions(NamedTuple):
    """Size of the terminal."""

    width: int
    height: int


class RenderWidth(NamedTuple):
    """Range of widths for a renderable object."""

    minimum: int
    maximum: int

    @property
    def span(self) -> int:
        """Get difference between maximum and minimum."""
        return self.maximum - self.minimum

    def with_maximum(self, width: int) -> RenderWidth:
        """Get a RenderableWith where the widths are <= width.
        
        Args:
            width (int): Maximum desred width.
        
        Returns:
            RenderableWidth: new RenderableWidth object.
        """
        minimum, maximum = self
        return RenderWidth(min(minimum, width), min(maximum, width))

    @classmethod
    def get(cls, renderable: RenderableType, max_width: int) -> RenderWidth:
        """Get desired width for a renderable."""
        if hasattr(renderable, "__console__"):
            get_console_width = getattr(renderable, "__console_width__", None)
            if get_console_width is not None:
                render_width = get_console_width(max_width).with_maximum(max_width)
                return render_width
            else:
                return RenderWidth(1, max_width)
        elif isinstance(renderable, Segment):
            text, _style = renderable
            width = min(max_width, len(text))
            return RenderWidth(width, width)
        elif isinstance(renderable, str):
            text = renderable.rstrip()
            return RenderWidth(len(text), len(text))
        else:
            raise errors.NotRenderableError(
                f"Unable to get render width for {renderable!r}; "
                "a str, Segment, or object with __console__ method is required"
            )


class StyleContext:
    """A context manager to manage a style."""

    def __init__(self, console: Console, style: Style):
        self.console = console
        self.style = style

    def __enter__(self) -> Console:
        self.console.push_style(self.style)
        self.console._enter_buffer()
        return self.console

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.console._exit_buffer()
        self.console.pop_style()


COLOR_SYSTEMS = {
    "none": ColorSystem.NONE,
    "standard": ColorSystem.STANDARD,
    "256": ColorSystem.EIGHT_BIT,
    "truecolor": ColorSystem.TRUECOLOR,
}


class Console:
    """A high level console interface."""

    default_style = Style.reset()

    def __init__(
        self,
        color_system: Literal["auto", "none", "standard", "256", "truecolor"] = "auto",
        styles: Dict[str, Style] = DEFAULT_STYLES,
        file: IO = None,
        width: int = None,
        height: int = None,
        record: bool = False,
        markup: Optional[str] = "markdown",
    ):

        self._styles = ChainMap(styles)
        self.file = file or sys.stdout
        self._width = width
        self._height = height
        self._record = record
        self._markup = markup

        if color_system == "auto":
            color_system = self._detect_color_system()
        self._color_system = COLOR_SYSTEMS[color_system]

        self.buffer: List[Segment] = []
        self._buffer_index = 0
        self._record_buffer: List[Segment] = []

        default_style = Style()
        self.style_stack: List[Style] = [default_style]
        self.current_style = default_style

    def __repr__(self) -> str:
        return f"<console width={self.width} {str(self._color_system)}>"

    def _detect_color_system(
        self,
    ) -> Literal["auto", "none", "standard", "256", "truecolor"]:
        """Detect color system from env vars."""
        if not self.is_terminal:
            return "none"
        if os.environ.get("COLORTERM", "").strip().lower() == "truecolor":
            return "truecolor"
        # 256 can be considered standard nowadays
        return "256"

    def _enter_buffer(self) -> None:
        """Enter in to a buffer context, and buffer all output."""
        self._buffer_index += 1

    def _exit_buffer(self) -> None:
        """Leave buffer context, and render content if required."""
        self._buffer_index -= 1
        self._check_buffer()

    def __enter__(self) -> Console:
        """Own context manager to enter buffer context."""
        self._enter_buffer()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """Exit buffer context."""
        self._exit_buffer()

    @property
    def encoding(self) -> str:
        """Get the encoding of the console file.
        
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
            max_width=self.width, encoding=self.encoding, is_terminal=self.is_terminal
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
        if not count:
            return
        self.buffer.append(Segment("\n" * count))
        self._check_buffer()

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
        render_iterable: Iterable[RenderableType]
        render_options = options or self.options
        if isinstance(renderable, Segment):
            yield renderable
        elif isinstance(renderable, ConsoleRenderable):
            render_iterable = renderable.__console__(self, render_options)
        elif isinstance(renderable, str):
            render_iterable = self.render_str(renderable, render_options)
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
        style = style or self.current_style
        render_options = options or self.options

        lines = Segment.split_lines(
            Segment.apply_style(self.render(renderable, render_options), style),
            render_options.max_width,
        )
        return list(lines)

    def render_str(
        self, text: str, options: ConsoleOptions
    ) -> Iterable[RenderableType]:
        """Convert a string to something renderable.
        
        Args:
            text (str): Text to render.
            options (ConsoleOptions): Options for render.
        
        Returns:
            Iterable[RenderableType]: Renderable objects.
        
        """

        if self._markup == "markdown":
            from .markdown import Markdown

            yield Markdown(text)
        else:
            from .text import Text

            yield Text(text, self.current_style)

    def _get_style(self, name: str) -> Optional[Style]:
        """Get a named style, or `None` if it doesn't exist.
        
        Args:
            name (str): The name of a style.
        
        Returns:
            Optional[Style]: A Style object for the given name, or `None`.
        """
        return self._styles.get(name, None)

    def get_style(self, name: Union[str, Style]) -> Optional[Style]:
        """Get a style.

        Args:
            name (str): The name of a style.
        
        Returns:
            Optional[Style]: A Style object or `None` if it couldn't be found / parsed.

        """
        if isinstance(name, Style):
            return name
        try:
            return self._styles.get(name, None) or Style.parse(name)
        except errors.StyleSyntaxError:
            return None

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
            style = Style.parse(style)
        self.current_style = self.current_style.apply(style)
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

    def style(self, style: Union[str, Style]) -> StyleContext:
        """A context manager to apply a new style.

        Example:
            with context.style("bold red"):
                context.print("Danger Will Robinson!")
        
        Args:
            style (Union[str, Style]): New style to apply.
        
        Returns:
            StyleContext: A style context manager.
        """
        if isinstance(style, str):
            _style = self.get_style(style) or Style()
        else:
            if not isinstance(style, Style):
                raise TypeError(f"style must be a str or Style instance, not {style!r}")
            _style = style
        return StyleContext(self, _style)

    def write(self, text: str, style: str = None) -> None:
        """Write text in the current style.
        
        Args:
            text (str): Text to write
        
        Returns:
            None: 
        """
        write_style = self.current_style or self._get_style(style or "none")
        self.buffer.append(Segment(text, write_style))
        self._check_buffer()

    def print(
        self,
        *objects: RenderableType,
        sep=" ",
        end="\n",
        style: Union[str, Style] = None,
        emoji=True,
    ) -> None:
        """Print to the console.
        
        Args:
            *objects: Arbitrary objects to print to the console.
            sep (str, optional): Separator to print between objects. Defaults to " ".
            end (str, optional): Character to end print with. Defaults to "\n".
            style (Union[str, Style], optional): 
            emoji (bool): If True, emoji codes will be replaced, otherwise emoji codes will be left in.
        """
        if not objects:
            self.line()
            return
        options = self.options
        buffer_extend = self.buffer.extend
        strings: List[str] = []

        def check_strings() -> None:
            """Check strings buffer."""
            if strings:
                text = f"{sep.join(strings)}{end}"
                if emoji:
                    text = _emoji_replace(text)
                buffer_extend(self.render(text, options))

        if style is not None:
            self.push_style(style)
        with self:
            try:
                for console_object in objects:
                    if isinstance(console_object, (ConsoleRenderable, Segment)):
                        check_strings()
                        buffer_extend(self.render(console_object, options))
                    else:
                        strings.append(str(console_object))
                check_strings()
            finally:
                if style is not None:
                    self.pop_style()

    def _check_buffer(self) -> None:
        """Check if the buffer may be rendered."""
        if self._buffer_index == 0:
            text = self._render_buffer()
            self.file.write(text)

    def _render_buffer(self) -> str:
        """Render buffered output, and clear buffer."""
        output: List[str] = []
        append = output.append
        current_style = self.current_style
        color_system = self._color_system
        buffer = self.buffer[:]
        if self._record:
            self._record_buffer.extend(buffer)
        del self.buffer[:]
        for line in Segment.split_lines(buffer, self.width):
            for text, style in line:
                if style:
                    style = current_style.apply(style)
                    append(style.render(text, color_system=color_system, reset=True))
                else:
                    append(text)
            append("\n")
        rendered = "".join(output)
        return rendered

    def save_html(
        self,
        path: str,
        theme: Theme = None,
        clear: bool = True,
        code_format=CONSOLE_HTML_FORMAT,
        inline_styles: bool = False,
    ) -> None:
        """Write console data to HTML file (required record=True argument in constructor).
        
        Args:
            path (str): A path to html file to write.            
            theme (Theme, optional): Theme object containing console colors.
            clear (bool, optional): Set to True to clear the record buffer after saving HTML.
            code_format (str, optional): Format string to render HTML, should contain {foreground}
                {background} and {code}.
            inline_styes (bool, optional): If True styles will be inlined in to spans, which makes files
                larger but easier to cut and paste markup. If False, styles will be embedded in a style tag.
                Defaults to False.
        """

        fragments: List[str] = []
        append = fragments.append
        _theme = theme or themes.DEFAULT
        stylesheet = ""

        if inline_styles:
            for text, style in Segment.simplify(self._record_buffer):
                if style:
                    rule = style.get_html_style(_theme)
                    append(f'<span style="{rule}">{text}</span>' if rule else text)
                else:
                    append(text)
        else:
            styles: Dict[str, int] = {}
            for text, style in Segment.simplify(self._record_buffer):
                if style:
                    rule = style.get_html_style(_theme)
                    if rule:
                        style_number = styles.setdefault(rule, len(styles) + 1)
                        append(f'<span class="rich{style_number}">{text}</span>')
                    else:
                        append(text)
                else:
                    append(text)
            stylesheet_rules: List[str] = []
            stylesheet_append = stylesheet_rules.append
            for style_number, style_rule in sorted((v, k) for k, v in styles.items()):
                if style_rule:
                    stylesheet_append(f".rich{style_number} {{ {style_rule} }}\n")
            stylesheet = "".join(stylesheet_rules)

        rendered_code = code_format.format(
            code="".join(fragments),
            stylesheet=stylesheet,
            foreground=_theme.foreground_color.css,
            background=_theme.background_color.css,
        )
        with open(path, "wt") as write_file:
            write_file.write(rendered_code)
        if clear:
            del self._record_buffer[:]


if __name__ == "__main__":
    console = Console(width=80)
    # console.write_text("Hello", style="bold magenta on white", end="").write_text(
    #     " World!", "italic blue"
    # )
    # "[b]This is bold [style not bold]This is not[/style] this is[/b]"

    # console.write("Hello ")
    # with console.style("bold blue"):
    #     console.write("World ")
    #     with console.style("italic"):
    #         console.write("in style")
    # console.write("!")

    with console.style("dim on black"):
        console.print("**Hello**, *World*!")
        console.print("Hello, *World*!")

    # console.print("foo")

