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


@dataclass
class ConsoleOptions:
    """Options for __console__ method."""

    max_width: int
    min_width: int = 1


@runtime_checkable
class SupportsConsole(Protocol):
    def __console__(self) -> StyledText:
        ...


class SupportsStr(Protocol):
    def __str__(self) -> str:
        ...


@runtime_checkable
class ConsoleRenderable(Protocol):
    """An object that supports the console protocol."""

    def __console_render__(
        self, console: Console, options: ConsoleOptions
    ) -> Iterable[Union[SupportsConsole, StyledText]]:
        ...


class StyledText(NamedTuple):
    """A piece of text with associated style."""

    text: str
    style: Optional[Style] = None

    def __repr__(self) -> str:
        """Simplified repr."""
        return f"StyleText({self.text!r}, {self.style!r})"


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
        self.console._enter_buffer()
        self.console.push_style(self.style)
        return self.console

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.console.pop_style()
        self.console._exit_buffer()


class Console:
    """A high level console interface."""

    default_style = Style.reset()

    def __init__(self, styles: Dict[str, Style] = DEFAULT_STYLES, file: IO = None):
        self._styles = ChainMap(styles)
        self.file = file or sys.stdout
        self.style_stack: List[Style] = [Style()]
        self.buffer: List[StyledText] = []
        self.current_style = Style()
        self._buffer_index = 0

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

    def get_style(self, name: str) -> Optional[Style]:
        """Get a named style, or `None` if it doesn't exist.
        
        Args:
            name (str): The name of a style.
        
        Returns:
            Optional[Style]: A Style object for the given name, or `None`.
        """
        return self._styles.get(name, None)

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
        write_style = self.current_style or self.get_style(style)
        self.buffer.append(StyledText(text, write_style))
        self._check_buffer()

    def print(self, *objects: Union[ConsoleRenderable, SupportsStr]) -> None:
        options = ConsoleOptions(max_width=self.width)
        buffer_append = self.buffer.append
        with self:
            for console_object in objects:
                if isinstance(console_object, ConsoleRenderable):
                    render = console_object.__console_render__(self, options)
                    for console_output in render:
                        if isinstance(console_output, SupportsConsole):
                            styled_text = console_output.__console__()
                        else:
                            styled_text = console_output
                        buffer_append(styled_text)
                else:
                    styled_text = StyledText(str(console_object), None)
                    buffer_append(styled_text)
            buffer_append(StyledText("\n"))

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
        width, height = shutil.get_terminal_size()
        return ConsoleDimensions(width, height)

    @property
    def width(self) -> int:
        """Get the width of the console.
        
        Returns:
            int: The width (in characters) of the console.
        """
        width, _ = shutil.get_terminal_size()
        return width

    # def write(self, console_object: Any) -> Console:
    #     if isinstance(console_object, SupportsConsole):
    #         return self.write_object(console_object)
    #     else:
    #         text = str(console_object)
    #         return self.write_text(text)

    # def write_object(self, console_object: SupportsConsole) -> Console:
    #     console_object.__console__(self)
    #     return self

    # def write_text(
    #     self, text: str, style: Union[str, Style] = None, *, end="\n"
    # ) -> Console:
    #     if isinstance(style, str):
    #         render_style = Style.parse(style)
    #     elif isinstance(style, Style):
    #         render_style = style

    #     prefix = render_style.render(Style())
    #     self.file.write(f"{prefix}{text}\x1b[0m{end}")
    #     return self

    # def new_line(self) -> Console:
    #     return self


if __name__ == "__main__":
    console = Console()
    # console.write_text("Hello", style="bold magenta on white", end="").write_text(
    #     " World!", "italic blue"
    # )
    # "[b]This is bold [style not bold]This is not[/style] this is[/b]"

    console.write("Hello ")
    with console.style("bold blue"):
        console.write("World ")
        with console.style("italic"):
            console.write("in style")
    console.write("!")

