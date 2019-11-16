from __future__ import annotations


from collections import ChainMap
from contextlib import contextmanager
from dataclasses import dataclass
from enum import Enum
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
    runtime_checkable,
    Union,
)

from .default_styles import DEFAULT_STYLES
from . import errors
from .style import Style
from .styled_text import StyledText


@dataclass
class ConsoleOptions:
    """Options for __console__ method."""

    max_width: int
    is_terminal: bool
    encoding: str
    min_width: int = 1


class SupportsStr(Protocol):
    def __str__(self) -> str:
        ...


@runtime_checkable
class ConsoleRenderable(Protocol):
    """An object that supports the console protocol."""

    def __console__(
        self, console: Console, options: ConsoleOptions
    ) -> Iterable[Union[ConsoleRenderable, StyledText]]:
        ...


RenderableType = Union[ConsoleRenderable, StyledText, SupportsStr]
RenderResult = Iterable[Union[ConsoleRenderable, StyledText]]


class ConsoleDimensions(NamedTuple):
    """Size of the terminal."""

    width: int
    height: int


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


class Console:
    """A high level console interface."""

    default_style = Style.reset()

    def __init__(
        self,
        styles: Dict[str, Style] = DEFAULT_STYLES,
        file: IO = None,
        width: int = None,
        height: int = None,
        markup: str = "markdown",
    ):
        self._styles = ChainMap(styles)
        self.file = file or sys.stdout
        self._width = width
        self._height = height
        self._markup = markup

        self.buffer: List[StyledText] = []
        self._buffer_index = 0

        default_style = Style()
        self.style_stack: List[Style] = [default_style]
        self.current_style = default_style

    # def push_styles(self, styles: Dict[str, Style]) -> None:
    #     """Push a new set of styles on to the style stack.

    #     Args:
    #         styles (Dict[str, Style]): A mapping of styles.

    #     """
    #     self._styles.maps.insert(0, styles)

    # def pop_styles(self) -> None:
    #     if len(self._styles.maps) == 1:
    #         raise StyleError("Can't pop default styles")
    #     self._styles.maps.pop(0)

    def _enter_buffer(self) -> None:
        self._buffer_index += 1

    def _exit_buffer(self) -> None:
        self._buffer_index -= 1
        self._check_buffer()

    def __enter__(self) -> Console:
        self._enter_buffer()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
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

    def line(self, count: int = 1) -> None:
        self.buffer.append(StyledText("\n" * count))
        self._check_buffer()

    def render(
        self, renderable: RenderableType, options: ConsoleOptions
    ) -> Iterable[StyledText]:
        """Render an object in to an iterable of `StyledText` instances.

        This method contains the logic for rendering objects with the console protocol. 
        You are unlikely to need to use it directly, unless you are extending the library.

        
        Args:
            renderable (RenderableType): An object supporting the console protocol, or
                an object that may be converted to a string.
            options (ConsoleOptions, optional): An options objects. Defaults to None.
        
        Returns:
            Iterable[StyledText]: An iterable of styled text that may be rendered.
        """
        render_iterable: Iterable[RenderableType]
        if isinstance(renderable, StyledText):
            yield renderable
        elif isinstance(renderable, ConsoleRenderable):
            render_iterable = renderable.__console__(self, options)
        else:
            render_iterable = self.render_str(str(renderable), options)

        for render_output in render_iterable:
            if isinstance(render_output, StyledText):
                yield render_output
            else:
                yield from self.render(render_output, options)

    def render_str(
        self, text: str, options: ConsoleOptions
    ) -> Iterable[RenderableType]:
        """Render a string."""
        if self._markup == "markdown":
            from .markdown import Markdown

            yield Markdown(text)
        else:
            yield StyledText(text, self.current_style)

    def get_style(self, name: str) -> Optional[Style]:
        """Get a named style, or `None` if it doesn't exist.
        
        Args:
            name (str): The name of a style.
        
        Returns:
            Optional[Style]: A Style object for the given name, or `None`.
        """
        return self._styles.get(name, None)

    def parse_style(self, name: str) -> Optional[Style]:
        """Get a named style, or parse a style definition.

        Args:
            name (str): The name of a style.
        
        Returns:
            Optional[Style]: A Style object or `None` if it couldn't be found / parsed.

        """
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
            style = Style.parse(style)
        return StyleContext(self, style)

    def write(self, text: str, style: str = None) -> None:
        """Write text in the current style.
        
        Args:
            text (str): Text to write
        
        Returns:
            None: 
        """
        write_style = self.current_style or self.get_style(style or "none")
        self.buffer.append(StyledText(text, write_style))
        self._check_buffer()

    def print(self, *objects: RenderableType, sep=" ", end="\n") -> None:
        """Print to the console.
        
        Args:
            *objects: Arbitrary objects to print to the console.
            sep (str, optional): Separator to print between objects. Defaults to " ".
            end (str, optional): Character to end print with. Defaults to "\n".
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
                buffer_extend(self.render(text, options))

        with self:
            for console_object in objects:
                if isinstance(console_object, (ConsoleRenderable, StyledText)):
                    check_strings()
                    buffer_extend(self.render(console_object, options))
                else:
                    strings.append(str(console_object))
            check_strings()

    def _check_buffer(self) -> None:
        """Check if the buffer may be rendered."""
        if self._buffer_index == 0:
            text = self._render_buffer()
            self.file.write(text)

    def _render_buffer(self) -> str:
        """Render buffered output, and clear buffer."""
        output: List[str] = []
        append = output.append
        for text, style in self.buffer:
            if style:
                style = self.current_style.apply(style)
                append(style.render(text, reset=True))
            else:
                append(text)
        rendered = "".join(output)

        del self.buffer[:]
        return rendered

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

    console.print("Hello", "*World*")
    console.print()
    with console.style("dim on black"):
        console.print("**Hello**, *World*!")
        console.print("Hello, *World*!")

    # console.print("foo")

