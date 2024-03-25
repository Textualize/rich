Introduction
============

Rich is a Python library for writing *rich* text (with color and style) to the terminal, and for displaying advanced content such as tables, markdown, and syntax highlighted code.

Use Rich to make your command line applications visually appealing and present data in a more readable way. Rich can also be a useful debugging aid by pretty printing and syntax highlighting data structures.

Requirements
------------

Rich works with macOS, Linux and Windows.

On Windows both the (ancient) cmd.exe terminal is supported and the new `Windows Terminal <https://github.com/microsoft/terminal/releases>`_. The latter has much improved support for color and style.

Rich requires Python 3.7.0 and above.

.. note::
    PyCharm users will need to enable "emulate terminal" in output console option in run/debug configuration to see styled output.

Installation
------------

You can install Rich from PyPI with `pip` or your favorite package manager::

    pip install rich

Add the ``-U`` switch to update to the current version, if Rich is already installed.

If you intend to use Rich with Jupyter then there are some additional dependencies which you can install with the following command::

    pip install "rich[jupyter]"


Quick Start
-----------

The quickest way to get up and running with Rich is to import the alternative ``print`` function which takes the same arguments as the built-in ``print`` and may be used as a drop-in replacement. Here's how you would do that::

    from rich import print

You can then print strings or objects to the terminal in the usual way. Rich will do some basic syntax :ref:`highlighting<highlighting>` and format data structures to make them easier to read.

Strings may contain :ref:`console_markup` which can be used to insert color and styles in to the output.

The following demonstrates both console markup and pretty formatting of Python objects::

    >>> print("[italic red]Hello[/italic red] World!", locals())

This writes the following output to the terminal (including all the colors and styles):

.. raw:: html

    <pre style="font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="color: #800000; font-style: italic">Hello</span> World!
    <span style="font-weight: bold">{</span>
        <span style="color: #008000">'__annotations__'</span>: <span style="font-weight: bold">{}</span>,
        <span style="color: #008000">'__builtins__'</span>: <span style="font-weight: bold"><</span><span style="color: #ff00ff">module</span><span style="color: #000000"> </span><span style="color: #008000">'builtins'</span><span style="color: #000000"> </span><span style="color: #000000; font-weight: bold">(</span><span style="color: #000000">built-in</span><span style="color: #000000; font-weight: bold">)</span><span style="font-weight: bold">></span>,
        <span style="color: #008000">'__doc__'</span>: <span style="color: #800080; font-style: italic">None</span>,
        <span style="color: #008000">'__loader__'</span>: <span style="font-weight: bold"><</span><span style="color: #ff00ff">class</span><span style="color: #000000"> </span><span style="color: #008000">'_frozen_importlib.BuiltinImporter'</span><span style="font-weight: bold">></span>,
        <span style="color: #008000">'__name__'</span>: <span style="color: #008000">'__main__'</span>,
        <span style="color: #008000">'__package__'</span>: <span style="color: #800080; font-style: italic">None</span>,
        <span style="color: #008000">'__spec__'</span>: <span style="color: #800080; font-style: italic">None</span>,
        <span style="color: #008000">'print'</span>: <span style="font-weight: bold"><</span><span style="color: #ff00ff">function</span><span style="color: #000000"> print at </span><span style="color: #000080; font-weight: bold">0x1027fd4c0</span><span style="font-weight: bold">></span>,
    <span style="font-weight: bold">}</span> </pre>


If you would rather not shadow Python's built-in print, you can import ``rich.print`` as ``rprint`` (for example)::

    from rich import print as rprint

Continue reading to learn about the more advanced features of Rich.

Rich in the REPL
----------------

Rich may be installed in the REPL so that Python data structures are automatically pretty printed with syntax highlighting. Here's how::

    >>> from rich import pretty
    >>> pretty.install()
    >>> ["Rich and pretty", True]

You can also use this feature to try out Rich *renderables*. Here's an example::

    >>> from rich.panel import Panel
    >>> Panel.fit("[bold yellow]Hi, I'm a Panel", border_style="red")

Read on to learn more about Rich renderables.

IPython Extension
~~~~~~~~~~~~~~~~~

Rich also includes an IPython extension that will do this same pretty install + pretty tracebacks. Here's how to load it::

    In [1]: %load_ext rich

You can also have it load by default by adding `"rich"` to the ``c.InteractiveShellApp.extension`` variable in
`IPython Configuration <https://ipython.readthedocs.io/en/stable/config/intro.html>`_.

Rich Inspect
------------

Rich has an :meth:`~rich.inspect` function which can generate a report on any Python object. It is a fantastic debug aid, and a good example of the output that Rich can generate. Here is a simple example::

    >>> from rich import inspect
    >>> from rich.color import Color
    >>> color = Color.parse("red")
    >>> inspect(color, methods=True)
