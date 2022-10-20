Console API
===========

For complete control over terminal formatting, Rich offers a :class:`~rich.console.Console` class. Most applications will require a single Console instance, so you may want to create one at the module level or as an attribute of your top-level object. For example, you could add a file called "console.py" to your project::

    from rich.console import Console
    console = Console()

Then you can import the console from anywhere in your project like this::

    from my_project.console import console

The console object handles the mechanics of generating ANSI escape sequences for color and style. It will auto-detect the capabilities of the terminal and convert colors if necessary.


Attributes
----------

The console will auto-detect a number of properties required when rendering.

* :obj:`~rich.console.Console.size` is the current dimensions of the terminal (which may change if you resize the window).
* :obj:`~rich.console.Console.encoding` is the default encoding (typically "utf-8").
* :obj:`~rich.console.Console.is_terminal` is a boolean that indicates if the Console instance is writing to a terminal or not.
* :obj:`~rich.console.Console.color_system` is a string containing the Console color system (see below).


Color systems
-------------

There are several "standards" for writing color to the terminal which are not all universally supported. Rich will auto-detect the appropriate color system, or you can set it manually by supplying a value for ``color_system`` to the :class:`~rich.console.Console` constructor.

You can set ``color_system`` to one of the following values:

* ``None`` Disables color entirely.
* ``"auto"`` Will auto-detect the color system.
* ``"standard"`` Can display 8 colors, with normal and bright variations, for 16 colors in total.
* ``"256"`` Can display the 16 colors from "standard" plus a fixed palette of 240 colors.
* ``"truecolor"`` Can display 16.7 million colors, which is likely all the colors your monitor can display.
* ``"windows"`` Can display 8 colors in legacy Windows terminal. New Windows terminal can display "truecolor".

.. warning::
    Be careful when setting a color system, if you set a higher color system than your terminal supports, your text may be unreadable.


Printing
--------

To write rich content to the terminal use the :meth:`~rich.console.Console.print` method. Rich will convert any object to a string via its (``__str__``) method and perform some simple syntax highlighting. It will also do pretty printing of any containers, such as dicts and lists. If you print a string it will render :ref:`console_markup`. Here are some examples::

    console.print([1, 2, 3])
    console.print("[blue underline]Looks like a link")
    console.print(locals())
    console.print("FOO", style="white on blue")

You can also use :meth:`~rich.console.Console.print` to render objects that support the :ref:`protocol`, which includes Rich's built-in objects such as :class:`~rich.text.Text`, :class:`~rich.table.Table`, and :class:`~rich.syntax.Syntax` -- or other custom objects.


Logging
-------

The :meth:`~rich.console.Console.log` method offers the same capabilities as print, but adds some features useful for debugging a running application. Logging writes the current time in a column to the left, and the file and line where the method was called to a column on the right. Here's an example::

    >>> console.log("Hello, World!")

.. raw:: html

    <pre style="font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="color: #7fbfbf">[16:32:08] </span>Hello, World!                                         <span style="color: #7f7f7f">&lt;stdin&gt;:1</span>
    </pre>

To help with debugging, the log() method has a ``log_locals`` parameter. If you set this to ``True``, Rich will display a table of local variables where the method was called.


Printing JSON
-------------

The :meth:`~rich.console.Console.print_json` method will pretty print (format and style) a string containing JSON. Here's a short example::

    console.print_json('[false, true, null, "foo"]')

You can also *log* json by logging a :class:`~rich.json.JSON` object::

    from rich.json import JSON
    console.log(JSON('["foo", "bar"]'))

Because printing JSON is a common requirement, you may import ``print_json`` from the main namespace::

    from rich import print_json

You can also pretty print JSON via the command line with the following::

    python -m rich.json cats.json


Low level output
----------------

In additional to :meth:`~rich.console.Console.print` and :meth:`~rich.console.Console.log`, Rich has an :meth:`~rich.console.Console.out` method which provides a lower-level way of writing to the terminal. The out() method converts all the positional arguments to strings and won't pretty print, word wrap, or apply markup to the output, but can apply a basic style and will optionally do highlighting.

Here's an example::

    >>> console.out("Locals", locals())


Rules
-----

The :meth:`~rich.console.Console.rule` method will draw a horizontal line with an optional title, which is a good way of dividing your terminal output into sections.

    >>> console.rule("[bold red]Chapter 2")

.. raw:: html

    <pre style="font-family:Menlo,\'DejaVu Sans Mono\',consolas,\'Courier New\',monospace"><span style="color: #00ff00">─────────────────────────────── </span><span style="color: #800000; font-weight: bold">Chapter 2</span><span style="color: #00ff00"> ───────────────────────────────</span></pre>

The rule method also accepts a ``style`` parameter to set the style of the line, and an ``align`` parameter to align the title ("left", "center", or "right").


Status
------

Rich can display a status message with a 'spinner' animation that won't interfere with regular console output. Run the following command for a demo of this feature::

    python -m rich.status

To display a status message, call :meth:`~rich.console.Console.status` with the status message (which may be a string, Text, or other renderable). The result is a context manager which starts and stops the status display around a block of code. Here's an example::

    with console.status("Working..."):
        do_work()

You can change the spinner animation via the ``spinner`` parameter::

    with console.status("Monkeying around...", spinner="monkey"):
        do_work()

Run the following command to see the available choices for ``spinner``::

    python -m rich.spinner


Justify / Alignment
-------------------

Both print and log support a ``justify`` argument which if set must be one of "default", "left", "right", "center", or "full".  If "left", any text printed (or logged) will be left aligned, if "right" text will be aligned to the right of the terminal, if "center" the text will be centered, and if "full" the text will be lined up with both the left and right edges of the terminal (like printed text in a book).

The default for ``justify`` is ``"default"`` which will generally look the same as ``"left"`` but with a subtle difference. Left justify will pad the right of the text with spaces, while a default justify will not. You will only notice the difference if you set a background color with the ``style`` argument. The following example demonstrates the difference::

    from rich.console import Console

    console = Console(width=20)

    style = "bold white on blue"
    console.print("Rich", style=style)
    console.print("Rich", style=style, justify="left")
    console.print("Rich", style=style, justify="center")
    console.print("Rich", style=style, justify="right")


This produces the following output:

.. raw:: html

    <pre style="font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="color: #c0c0c0; background-color: #000080; font-weight: bold">Rich
    Rich               &nbsp;
            Rich       &nbsp;
                    Rich
    </span></pre>

Overflow
--------

Overflow is what happens when text you print is larger than the available space. Overflow may occur if you print long 'words' such as URLs for instance, or if you have text inside a panel or table cell with restricted space.

You can specify how Rich should handle overflow with the ``overflow`` argument to :meth:`~rich.console.Console.print` which should be one of the following strings: "fold", "crop", "ellipsis", or "ignore". The default is "fold" which will put any excess characters on the following line, creating as many new lines as required to fit the text.

The "crop" method truncates the text at the end of the line, discarding any characters that would overflow.

The "ellipsis" method is similar to "crop", but will insert an ellipsis character ("…") at the end of any text that has been truncated.

The following code demonstrates the basic overflow methods::

    from typing import List
    from rich.console import Console, OverflowMethod

    console = Console(width=14)
    supercali = "supercalifragilisticexpialidocious"

    overflow_methods: List[OverflowMethod] = ["fold", "crop", "ellipsis"]
    for overflow in overflow_methods:
        console.rule(overflow)
        console.print(supercali, overflow=overflow, style="bold blue")
        console.print()

This produces the following output:

.. raw:: html

    <pre style="font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="color: #00ff00">──── </span>fold<span style="color: #00ff00"> ────</span>
    <span style="color: #000080; font-weight: bold">supercalifragi
    listicexpialid
    ocious
    </span>
    <span style="color: #00ff00">──── </span>crop<span style="color: #00ff00"> ────</span>
    <span style="color: #000080; font-weight: bold">supercalifragi
    </span>
    <span style="color: #00ff00">── </span>ellipsis<span style="color: #00ff00"> ──</span>
    <span style="color: #000080; font-weight: bold">supercalifrag…
    </span>
    </pre>

You can also set overflow to "ignore" which allows text to run on to the next line. In practice this will look the same as "crop" unless you also set ``crop=False`` when calling :meth:`~rich.console.Console.print`.


Console style
-------------

The Console has a ``style`` attribute which you can use to apply a style to everything you print. By default ``style`` is None meaning no extra style is applied, but you can set it to any valid style. Here's an example of a Console with a style attribute set::

    from rich.console import Console
    blue_console = Console(style="white on blue")
    blue_console.print("I'm blue. Da ba dee da ba di.")


Soft Wrapping
-------------

Rich word wraps text you print by inserting line breaks. You can disable this behavior by setting ``soft_wrap=True`` when calling :meth:`~rich.console.Console.print`. With *soft wrapping* enabled any text that doesn't fit will run on to the following line(s), just like the built-in ``print``.


Cropping
--------

The :meth:`~rich.console.Console.print` method has a boolean ``crop`` argument. The default value for crop is True which tells Rich to crop any content that would otherwise run on to the next line. You generally don't need to think about cropping, as Rich will resize content to fit within the available width.

.. note::
    Cropping is automatically disabled if you print with ``soft_wrap=True``.


Input
-----

The console class has an :meth:`~rich.console.Console.input` method which works in the same way as Python's built-in :func:`input` function, but can use anything that Rich can print as a prompt. For example, here's a colorful prompt with an emoji::

    from rich.console import Console
    console = Console()
    console.input("What is [i]your[/i] [bold red]name[/]? :smiley: ")

If Python's builtin :mod:`readline` module is previously loaded, elaborate line editing and history features will be available.

Exporting
---------

The Console class can export anything written to it as either text, svg, or html. To enable exporting, first set ``record=True`` on the constructor. This tells Rich to save a copy of any data you ``print()`` or ``log()``. Here's an example::

    from rich.console import Console
    console = Console(record=True)

After you have written content, you can call :meth:`~rich.console.Console.export_text`, :meth:`~rich.console.Console.export_svg` or :meth:`~rich.console.Console.export_html` to get the console output as a string. You can also call :meth:`~rich.console.Console.save_text`, :meth:`~rich.console.Console.save_svg`, or :meth:`~rich.console.Console.save_html` to write the contents directly to disk.

For examples of the html output generated by Rich Console, see :ref:`appendix-colors`.

Exporting SVGs
^^^^^^^^^^^^^^

When using :meth:`~rich.console.Console.export_svg` or :meth:`~rich.console.Console.save_svg`, the width of the SVG will match the width of your terminal window (in terms of characters), while the height will scale automatically to accommodate the console output.

You can open the SVG in a web browser. You can also insert it in to a webpage with an ``<img>`` tag or by copying the markup in to your HTML.

The image below shows an example of an SVG exported by Rich.

.. image:: ../images/svg_export.svg

You can customize the theme used during SVG export by importing the desired theme from the :mod:`rich.terminal_theme` module and passing it to :meth:`~rich.console.Console.export_svg` or :meth:`~rich.console.Console.save_svg` via the ``theme`` parameter::


    from rich.console import Console
    from rich.terminal_theme import MONOKAI

    console = Console(record=True)
    console.save_svg("example.svg", theme=MONOKAI)

Alternatively, you can create a theme of your own by constructing a :class:`rich.terminal_theme.TerminalTheme` instance yourself and passing that in.

.. note::
    The SVGs reference the Fira Code font. If you embed a Rich SVG in your page, you may also want to add a link to the `Fira Code CSS <https://cdnjs.com/libraries/firacode>`_

Error console
-------------

The Console object will write to ``sys.stdout`` by default (so that you see output in the terminal). If you construct the Console with ``stderr=True`` Rich will write to ``sys.stderr``. You may want to use this to create an *error console* so you can split error messages from regular output. Here's an example::

    from rich.console import Console
    error_console = Console(stderr=True)

You might also want to set the ``style`` parameter on the Console to make error messages visually distinct. Here's how you might do that::

    error_console = Console(stderr=True, style="bold red")

File output
-----------

You can tell the Console object to write to a file by setting the ``file`` argument on the constructor -- which should be a file-like object opened for writing text. You could use this to write to a file without the output ever appearing on the terminal. Here's an example::

    import sys
    from rich.console import Console
    from datetime import datetime

    with open("report.txt", "wt") as report_file:
        console = Console(file=report_file)
        console.rule(f"Report Generated {datetime.now().ctime()}")

Note that when writing to a file you may want to explicitly set the ``width`` argument if you don't want to wrap the output to the current console width.

Capturing output
----------------

There may be situations where you want to *capture* the output from a Console rather than writing it directly to the terminal. You can do this with the :meth:`~rich.console.Console.capture` method which returns a context manager. On exit from this context manager, call :meth:`~rich.console.Capture.get` to return the string that would have been written to the terminal. Here's an example::

    from rich.console import Console
    console = Console()
    with console.capture() as capture:
        console.print("[bold red]Hello[/] World")
    str_output = capture.get()

An alternative way of capturing output is to set the Console file to a :py:class:`io.StringIO`. This is the recommended method if you are testing console output in unit tests. Here's an example::

    from io import StringIO
    from rich.console import Console
    console = Console(file=StringIO())
    console.print("[bold red]Hello[/] World")
    str_output = console.file.getvalue()

Paging
------

If you have some long output to present to the user you can use a *pager* to display it. A pager is typically an application on your operating system which will at least support pressing a key to scroll, but will often support scrolling up and down through the text and other features.

You can page output from a Console by calling :meth:`~rich.console.Console.pager` which returns a context manager. When the pager exits, anything that was printed will be sent to the pager. Here's an example::

    from rich.__main__ import make_test_card
    from rich.console import Console

    console = Console()
    with console.pager():
        console.print(make_test_card())

Since the default pager on most platforms don't support color, Rich will strip color from the output. If you know that your pager supports color, you can set ``styles=True`` when calling the :meth:`~rich.console.Console.pager` method.

.. note::
    Rich will look at ``MANPAGER`` then the ``PAGER`` environment variables (``MANPAGER`` takes priority) to get the pager command. On Linux and macOS you can set one of these to ``less -r`` to enable paging with ANSI styles.

Alternate screen
----------------

.. warning::
    This feature is currently experimental. You might want to wait before using it in production.

Terminals support an 'alternate screen' mode which is separate from the regular terminal and allows for full-screen applications that leave your stream of input and commands intact. Rich supports this mode via the :meth:`~rich.console.Console.set_alt_screen` method, although it is recommended that you use :meth:`~rich.console.Console.screen` which returns a context manager that disables alternate mode on exit.

Here's an example of an alternate screen::

    from time import sleep
    from rich.console import Console

    console = Console()
    with console.screen():
        console.print(locals())
        sleep(5)

The above code will display a pretty printed dictionary on the alternate screen before returning to the command prompt after 5 seconds.

You can also provide a renderable to :meth:`~rich.console.Console.screen` which will be displayed in the alternate screen when you call :meth:`~rich.ScreenContext.update`.

Here's an example::

    from time import sleep

    from rich.console import Console
    from rich.align import Align
    from rich.text import Text
    from rich.panel import Panel

    console = Console()

    with console.screen(style="bold white on red") as screen:
        for count in range(5, 0, -1):
            text = Align.center(
                Text.from_markup(f"[blink]Don't Panic![/blink]\n{count}", justify="center"),
                vertical="middle",
            )
            screen.update(Panel(text))
            sleep(1)

Updating the screen with a renderable allows Rich to crop the contents to fit the screen without scrolling.

For a more powerful way of building full screen interfaces with Rich, see :ref:`live`.


.. note::
    If you ever find yourself stuck in alternate mode after exiting Python code, type ``reset`` in the terminal

Terminal detection
------------------

If Rich detects that it is not writing to a terminal it will strip control codes from the output. If you want to write control codes to a regular file then set ``force_terminal=True`` on the constructor.

Letting Rich auto-detect terminals is useful as it will write plain text when you pipe output to a file or other application.

Interactive mode
----------------

Rich will remove animations such as progress bars and status indicators when not writing to a terminal as you probably don't want to write these out to a text file (for example). You can override this behavior by setting the ``force_interactive`` argument on the constructor. Set it to True to enable animations or False to disable them.

.. note::
    Some CI systems support ANSI color and style but not anything that moves the cursor or selectively refreshes parts of the terminal. For these you might want to set ``force_terminal`` to ``True`` and ``force_interactive`` to ``False``.

Environment variables
---------------------

Rich respects some standard environment variables.

Setting the environment variable ``TERM`` to ``"dumb"`` or ``"unknown"`` will disable color/style and some features that require moving the cursor, such as progress bars.

If the environment variable ``FORCE_COLOR`` is set, then color/styles will be enabled regardless of the value of ``TERM``. This is useful on CI systems which aren't terminals but can none-the-less display ANSI escape sequences.

If the environment variable ``NO_COLOR`` is set, Rich will disable all color in the output. This takes precedence over ``FORCE_COLOR``. See `no_color <https://no-color.org/>`_ for details.

.. note::
    The ``NO_COLOR`` environment variable removes *color* only. Styles such as dim, bold, italic, underline etc. are preserved.

If ``width`` / ``height`` arguments are not explicitly provided as arguments to ``Console`` then the environment variables ``COLUMNS``/``LINES`` can be used to set the console width/height. ``JUPYTER_COLUMNS``/``JUPYTER_LINES`` behave similarly and are used in Jupyter.
