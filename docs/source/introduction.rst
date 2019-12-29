Introduction
============

Rich is a Python library for rendering *rich* text and formatting to the terminal. Use Rich to create slick command line applications and as a handy debugging aid.


Installation
------------

You may install Rich with your favorite PyPi package manager::

    pip install rich

Add the ``-U`` switch to update to the current version, if rich is already installed.


Quick Start
-----------

The quickest way to get up and running with Rich is to use the alternative ``print`` function, which can be used as a drop-in replacement for Python's built in function. Here's how you would do that::

    from rich import print

You can then print content to the terminal in the same way as usual. Rich will add the time and file/line number where print was called. It will also format and syntax highlight any Python objects you print. 

If you would rather not shadow Python's builtin print, you can import rich.print as ``rprint`` (for example)::

    from rich import print as rprint

For more control over formatting, create a :ref:`rich.console.Console` object::

    from rich.console import Console
    console = Console()
    console.print("Hello, **World**! :smiley:")