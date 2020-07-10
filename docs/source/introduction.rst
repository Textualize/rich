Introduction
============

Rich is a Python library for writing *rich* text (with color and formatting) to the terminal, and for rendering rich content such as tables, markdown, syntax highlighted code.

Use Rich to make command line applications more visually appealing and present data in a more readable way. Rich can also be a useful debugging aid by pretty printing and syntax highlighting data structures.

Requirements
------------

Rich works with OSX, Linux and Windows.

On Windows both the (ancient) cmd.exe terminal is supported and the new `Windows Terminal <https://github.com/microsoft/terminal/releases>`_. The later has much improved support for color and style.

Rich requires Python 3.6.1 and above. Note that Python 3.6.0 is *not* supported due to lack of support for methods on NamedTuples.

Installation
------------

You can install Rich with from PyPi with `pip` or your favorite package manager::

    pip install rich

Add the ``-U`` switch to update to the current version, if Rich is already installed.

If you intend to use Rich with Jupyter then there are some additional dependencies, which you can install with the following command::

    pip install rich[jupyter]


Quick Start
-----------

The quickest way to get up and running with Rich is to import the alternative ``print`` function, which can be used as a drop-in replacement for Python's built in function. Here's how you would do that::

    from rich import print

You can then print content to the terminal in the usual way. Rich will pretty print and syntax highlight any Python objects you print, and display the file/line where the print function was called.

Strings may contain :ref:`console_markup` which can be used to easily insert color and styles in to the output.

The following demonstrates both console markup and pretty formatting of Python objects::

    >>> print("[italic red]Hello[/italic red] World!", locals())

This writes the following output to the terminal (including all the colors and styles):

.. raw:: html

    <pre style="font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="color: #800000; font-style: italic">Hello</span> World!                                                 <span style="color: #7f7f7f">&lt;stdin&gt;:1</span>
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


If you would rather not shadow Python's builtin print, you can import ``rich.print`` as ``rprint`` (for example)::

    from rich import print as rprint

Continue reading to learn about the more advanced features of Rich.