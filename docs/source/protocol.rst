
.. _protocol:

Console Protocol
================

Rich supports a simple protocol to add rich formatting capabilities to custom objects, so you can :meth:`~rich.console.Console.print` your object with color, styles and formatting.

Use this for presentation or to display additional debugging information that might be hard to parse from a typical ``__repr__`` string.


Console Customization
---------------------

The easiest way to customize console output for your object is to implement a ``__rich__`` method. This method accepts no arguments, and should return an object that Rich knows how to render, such as a :class:`~rich.text.Text` or :class:`~rich.table.Table`. If you return a plain string it will be rendered as :ref:`console_markup`. Here's an example::

    class MyObject:
        def __rich__(self) -> str:
            return "[bold cyan]MyObject()"

If you were to print or log an instance of ``MyObject`` it would render as ``MyObject()`` in bold cyan. Naturally, you would want to put this to better use, perhaps by adding specialized syntax highlighting.


Console Render
--------------

The ``__rich__`` method is limited to a single renderable object. For more advanced rendering, add a ``__rich_console__`` method to your class.

The ``__rich_console__`` method should accept a :class:`~rich.console.Console` and a :class:`~rich.console.ConsoleOptions` instance. It should return an iterable of other renderable objects. Although that means it *could* return a container such as a list, it generally easier implemented by using the ``yield`` statement (making the method a generator).

Here's an example of a ``__rich_console__`` method::

    from dataclasses import dataclass
    from rich.console import Console, ConsoleOptions, RenderResult
    from rich.table import Table

    @dataclass
    class Student:
        id: int
        name: str
        age: int
        def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
            yield f"[b]Student:[/b] #{self.id}"
            my_table = Table("Attribute", "Value")
            my_table.add_row("name", self.name)
            my_table.add_row("age", str(self.age))
            yield my_table

If you were to print a ``Student`` instance, it would render a simple table to the terminal.


Low Level Render
~~~~~~~~~~~~~~~~

For complete control over how a custom object is rendered to the terminal, you can yield :class:`~rich.segment.Segment` objects. A Segment consists of a piece of text and an optional Style. The following example writes multi-colored text when rendering a ``MyObject`` instance::

    class MyObject:
        def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
            yield Segment("My", Style(color="magenta"))
            yield Segment("Object", Style(color="green"))
            yield Segment("()", Style(color="cyan"))


Measuring Renderables
~~~~~~~~~~~~~~~~~~~~~

Sometimes Rich needs to know how many characters an object will take up when rendering. The :class:`~rich.table.Table` class, for instance, will use this information to calculate the optimal dimensions for the columns. If you aren't using one of the renderable objects in the Rich module, you will need to supply a ``__rich_measure__`` method which accepts a :class:`~rich.console.Console` and :class:`~rich.console.ConsoleOptions` and returns a :class:`~rich.measure.Measurement` object. The Measurement object should contain the *minimum* and *maximum* number of characters required to render.

For example, if we are rendering a chess board, it would require a minimum of 8 characters to render. The maximum can be left as the maximum available width (assuming a centered board)::

    class ChessBoard:
        def __rich_measure__(self, console: Console, options: ConsoleOptions) -> Measurement:
            return Measurement(8, options.max_width)
