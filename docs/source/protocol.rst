
.. _protocol:

Console Protocol
================

Rich supports a simple protocol to add rich formatting capabilities to custom objects, so you can  :meth:`~rich.console.Console.print` your object with color, styles and formatting.

You can use this for presentation or to display additional debugging information that might be hard to parse from a typical ``__repr__`` string.


Console Str
-----------

The easiest way to add console output to your custom object is to implement a ``__console_str__`` method. This method accepts no arguments, and should return a :class:`~rich.text.Text` instance. Here's an example::

    class MyObject:
        def __console_str__(self) -> Text:
            return Text.from_markup("[bold]MyObject()[/bold]")

If you were to print or log an instance of ``MyObject`` it would render as ``MyObject()`` in bold. Naturally, you would want to put this to better use, perhaps by adding specialized syntax highlighting.


Console Render
--------------

The ``__console_str__`` method is limited to styled text. For more advanced rendering, Rich supports a ``__console__`` method which you can use to generate custom output with other renderable objects. For instance, a complex data type might be best represented as a :class:`~rich.table.Table`.

The ``__console__`` method should accept a :class:`~rich.console.Console` and a :class:`~rich.console.ConsoleOptions` instance. It should return an iterable of other renderable objects. Although that means it *could* return a container such as a list, it is customary to ``yield`` output (making the method a generator)

Here's an example of a ``__console__`` method::

    @dataclass
    class Student:
        name: str
        age: int
        def __console__(self, console: Console, options: ConsoleOptions) -> Iterable[Table]:
            my_table = Table("Attribute, "Value")
            my_table.add_row("name", self.name)
            my_table.add_row("age", str(self.age))
            yield my_table

If you were to print a ``Student`` instance, it would render a simple table to the terminal.


Low Level Render
~~~~~~~~~~~~~~~~

For complete control over how a custom object is rendered to the terminal, you can yield :class:`~rich.segment.Segment` objects. A Segment consists of a piece of text and an optional Style. The following example, writes multi-colored text when rendering a ``MyObject`` instance::


    class MyObject:
        def __console__(self, console: Console, options: ConsoleOptions) -> Iterable[Table]:
            yield Segment("My", "magenta")
            yield Segment("Object", green")
            yield Segment("()", "cyan")


Console Width
~~~~~~~~~~~~~

Sometimes Rich needs to know how many characters an object will take up when rendering. The :class:`~rich.table.Table` class for instance, will use this information to calculate the optimal dimensions for the columns. If you aren't using one of the standard classes, you will need to supply a ``__console_width__`` method which accepts the maximum width as an integer and returns a :class:`~rich.render_width.RenderWidth` object. The RenderWidth object should contain the *minimum* and *maximum* number of characters required to render.

For example, if we are rendering a chess board, it would require a minimum of 8 characters to render. The maximum can be left as the maximum available width (assuming a centered board):: 

    class ChessBoard:
        def __console_width__(self, max_width: int) -> RenderWidth:
            return RenderWidth(8, max_width)
