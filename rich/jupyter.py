import io
from typing import Any, IO, Union

from .console import Console as BaseConsole
from .style import Style

JUPYTER_HTML_FORMAT = """\
<pre style="white-space:pre;overflow-x:auto;line-height:1em;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace">{code}</pre>
"""


class JupyterRenderable:
    """A shim to write html to Jupyter notebook."""

    def __init__(self, text: str, html: str) -> None:
        self.text = text
        self.html = html

    def __str__(self) -> str:
        return self.text

    def _repr_html_(self) -> str:
        return self.html


class Console(BaseConsole):
    def __init__(self, **kwargs) -> None:
        kwargs["file"] = io.StringIO()
        kwargs["record"] = True
        if "width" not in kwargs:
            kwargs["width"] = 100
        super().__init__(**kwargs)

    def is_terminal(self) -> bool:
        return True

    def print(  # type: ignore
        self,
        *objects: Any,
        sep=" ",
        end="\n",
        file: IO[str] = None,
        style: Union[str, Style] = None,
        emoji: bool = None,
        markup: bool = None,
        highlight: bool = None,
        flush: bool = False
    ) -> JupyterRenderable:
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
        if file is None:
            super().print(
                *objects,
                sep=sep,
                end=end,
                style=style,
                emoji=emoji,
                markup=markup,
                highlight=highlight,
            )
        else:
            Console(file=file).print(
                *objects,
                sep=sep,
                end=end,
                style=style,
                emoji=emoji,
                markup=markup,
                highlight=highlight,
            )

        html = self.export_html(code_format=JUPYTER_HTML_FORMAT, inline_styles=True)
        text = self.file.getvalue()  # type: ignore
        self.file = io.StringIO()
        jupyter_renderable = JupyterRenderable(text, html)
        return jupyter_renderable


console = Console()
print = console.print
