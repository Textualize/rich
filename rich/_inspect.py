from __future__ import absolute_import

from inspect import cleandoc, getdoc, getfile, isclass, ismodule, signature
from typing import Any, Iterable, Optional, Tuple

from .console import RenderableType, RenderGroup
from .highlighter import ReprHighlighter
from .jupyter import JupyterMixin
from .panel import Panel
from .pretty import Pretty
from .table import Table
from .text import Text, TextType


def _first_paragraph(doc: str) -> str:
    """Get the first paragraph from a docstring."""
    paragraph, _, _ = doc.partition("\n\n")
    return paragraph


def _reformat_doc(doc: str) -> str:
    """Reformat docstring."""
    doc = cleandoc(doc).strip()
    return doc


class Inspect(JupyterMixin):
    """A renderable to inspect any Python Object.

    Args:
        obj (Any): An object to inspect.
        title (str, optional): Title to display over inspect result, or None use type. Defaults to None.
        help (bool, optional): Show full help text rather than just first paragraph. Defaults to False.
        methods (bool, optional): Enable inspection of callables. Defaults to False.
        docs (bool, optional): Also render doc strings. Defaults to True.
        private (bool, optional): Show private attributes (begining with underscore). Defaults to False.
        dunder (bool, optional): Show attributes starting with double underscore. Defaults to False.
        sort (bool, optional): Sort attributes alphabetically. Defaults to True.
        all (bool, optional): Show all attributes. Defaults to False.
    """

    def __init__(
        self,
        obj: Any,
        *,
        title: TextType = None,
        help: bool = False,
        methods: bool = False,
        docs: bool = True,
        private: bool = False,
        dunder: bool = False,
        sort: bool = True,
        all: bool = True,
    ) -> None:
        self.highlighter = ReprHighlighter()
        self.obj = obj
        self.title = title or self._make_title(obj)
        if all:
            methods = private = dunder = True
        self.help = help
        self.methods = methods
        self.docs = docs or help
        self.private = private or dunder
        self.dunder = dunder
        self.sort = sort

    def _make_title(self, obj: Any) -> Text:
        """Make a default title."""
        title_str = (
            str(obj)
            if (isclass(obj) or callable(obj) or ismodule(obj))
            else str(type(obj))
        )
        title_text = self.highlighter(title_str)
        return title_text

    def __rich__(self) -> Panel:
        return Panel.fit(
            RenderGroup(*self._render()),
            title=self.title,
            border_style="scope.border",
            padding=(0, 1),
        )

    def _get_signature(self, name: str, obj: Any) -> Text:
        """Get a signature for a callable."""
        try:
            _signature = str(signature(obj)) + ":"
        except ValueError:
            _signature = "(...)"

        source_filename: Optional[str] = None
        try:
            source_filename = getfile(obj)
        except TypeError:
            pass

        callable_name = Text(name, style="inspect.callable")
        if source_filename:
            callable_name.stylize(f"link file://{source_filename}")
        signature_text = self.highlighter(_signature)

        qualname = name or getattr(obj, "__qualname__", name)
        qual_signature = Text.assemble(
            ("def ", "inspect.def"), (qualname, "inspect.callable"), signature_text
        )

        return qual_signature

    def _render(self) -> Iterable[RenderableType]:
        """Render object."""

        def sort_items(item: Tuple[str, Any]) -> Tuple[bool, str]:
            key, (_error, value) = item
            return (callable(value), key.strip("_").lower())

        def safe_getattr(attr_name: str) -> Tuple[Any, Any]:
            """Get attribute or any exception."""
            try:
                return (None, getattr(obj, attr_name))
            except Exception as error:
                return (error, None)

        obj = self.obj
        keys = dir(obj)
        total_items = len(keys)
        if not self.dunder:
            keys = [key for key in keys if not key.startswith("__")]
        if not self.private:
            keys = [key for key in keys if not key.startswith("_")]
        not_shown_count = total_items - len(keys)
        items = [(key, safe_getattr(key)) for key in keys]
        if self.sort:
            items.sort(key=sort_items)

        items_table = Table.grid(padding=(0, 1), expand=False)
        items_table.add_column(justify="right")
        add_row = items_table.add_row
        highlighter = self.highlighter

        if callable(obj):
            yield self._get_signature("", obj)
            yield ""

        _doc = getdoc(obj)
        if _doc is not None:
            if not self.help:
                _doc = _first_paragraph(_doc)
            doc_text = Text(_reformat_doc(_doc), style="inspect.help")
            doc_text = highlighter(doc_text)
            yield doc_text
            yield ""

        for key, (error, value) in items:
            key_text = Text.assemble(
                (
                    key,
                    "inspect.attr.dunder" if key.startswith("__") else "inspect.attr",
                ),
                (" =", "inspect.equals"),
            )
            if error is not None:
                warning = key_text.copy()
                warning.stylize("inspect.error")
                add_row(warning, highlighter(repr(error)))
                continue

            if callable(value):
                if not self.methods:
                    continue
                _signature_text = self._get_signature(key, value)

                if self.docs:
                    docs = getdoc(value)
                    if docs is not None:
                        _doc = _reformat_doc(str(docs))
                        if not self.help:
                            _doc = _first_paragraph(_doc)
                        _signature_text.append("\n" if "\n" in _doc else " ")
                        doc = highlighter(_doc)
                        doc.stylize("inspect.doc")
                        _signature_text.append(doc)

                add_row(key_text, _signature_text)
            else:
                add_row(key_text, Pretty(value, highlighter=highlighter))
        if items_table.row_count:
            yield items_table
        else:
            yield self.highlighter(
                Text.from_markup(
                    f"[i]{not_shown_count} attribute(s) not shown.[/i] Use inspect(<OBJECT>, all=True) to see all attributes."
                )
            )


if __name__ == "__main__":  # type: ignore
    from rich import print

    inspect = Inspect({}, docs=True, methods=True, dunder=True)
    print(inspect)

    t = Text("Hello, World")
    print(Inspect(t))

    from rich.style import Style
    from rich.color import Color

    print(Inspect(Style.parse("bold red on black"), methods=True, docs=True))
    print(Inspect(Color.parse("#ffe326"), methods=True, docs=True))

    from rich import get_console

    print(Inspect(get_console(), methods=False))

    print(Inspect(open("foo.txt", "wt"), methods=False))

    print(Inspect("Hello", methods=False, dunder=True))
    print(Inspect(inspect, methods=False, dunder=False, docs=False))

    class Foo:
        @property
        def broken(self):
            1 / 0

    f = Foo()
    print(Inspect(f))

    print(Inspect(object, dunder=True))

    print(Inspect(None, dunder=False))

    print(Inspect(str, help=True))
    print(Inspect(1, help=False))
