Syntax
======

Rich can syntax highlight various programming languages with line numbers.

To syntax highlight code, construct a :class:`~rich.syntax.Syntax` object and print it to the console. Here's an example::

    from rich.console import Console
    from rich.syntax import Syntax

    console = Console()
    with open("syntax.py", "rt") as code_file:
        syntax = Syntax(code_file.read(), "python")
    console.print(syntax)

You may also use the :meth:`~rich.syntax.Syntax.from_path` alternative constructor which will load the code from disk and auto-detect the file type. The example above could be re-written as follows::


    from rich.console import Console
    from rich.syntax import Syntax

    console = Console()
    syntax = Syntax.from_path("syntax.py")
    console.print(syntax)


Line numbers
------------

If you set ``line_numbers=True``, Rich will render a column for line numbers::

    syntax = Syntax.from_path("syntax.py", line_numbers=True)


Theme
-----

The Syntax constructor (and :meth:`~rich.syntax.Syntax.from_path`) accept a ``theme`` attribute which should be the name of a `Pygments theme <https://pygments.org/demo/>`_. It may also be one of the special case theme names "ansi_dark" or "ansi_light" which will use the color theme configured by the terminal.


Background color
----------------

You can override the background color from the theme by supplying a ``background_color`` argument to the constructor. This should be a string in the same format a style definition accepts, e.g. "red", "#ff0000", "rgb(255,0,0)" etc. You may also set the special value "default" which will use the default background color set in the terminal.


Stylize Range
-------------

You can apply custom styling to specific portions of syntax highlighted code
using the :meth:`~rich.syntax.Syntax.stylize_range` method::

    from rich.console import Console
    from rich.syntax import Syntax
    from rich.style import Style

    console = Console()

    code = """\
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)"""

    syntax = Syntax(code, "python", line_numbers=True)
    syntax.stylize_range(Style(bgcolor="bright_yellow"), (3, 4), (3, 13))
    console.print(syntax)

The ``stylize_range`` method accepts a :class:`~rich.style.Style` object and
two positional tuples: ``start`` and ``end``.

Positions are specified as ``(line, column)`` tuples where:

- ``line`` is 1-based (the first line is 1)
- ``column`` is 0-based (the first character on a line is 0)

You can also pass ``style_before=True`` to apply the style underneath
any existing styles, instead of on top::

    syntax.stylize_range(
        Style(bold=True),
        (1, 0), (1, 3),
        style_before=True,
    )

.. note::

    Line numbers are based on the original code, not the displayed output.
    If your code contains newline characters (``\\n``), each newline
    increments the line number.

For a complete working example, see
``examples/sintaxy_with_styles.py``.


Syntax CLI
----------

You can use this class from the command line. Here's how you would syntax highlight a file called "syntax.py"::

    python -m rich.syntax syntax.py

For the full list of arguments, run the following::

    python -m rich.syntax -h
    
