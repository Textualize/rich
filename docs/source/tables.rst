Tables
======

Rich's :class:`~rich.table.Table` class offers a variety of ways to render tabular data to the terminal.

To render a table, construct a :class:`~rich.table.Table` object, add columns with :meth:`~rich.table.Table.add_column`, and rows with :meth:`~rich.table.Table.add_row` -- then print it to the console.

Here's an example::

    from rich.console import Console
    from rich.table import Table

    table = Table(title="Star Wars Movies")

    table.add_column("Released", justify="right", style="cyan", no_wrap=True)
    table.add_column("Title", style="magenta")
    table.add_column("Box Office", justify="right", style="green")

    table.add_row("Dec 20, 2019", "Star Wars: The Rise of Skywalker", "$952,110,690")
    table.add_row("May 25, 2018", "Solo: A Star Wars Story", "$393,151,347")
    table.add_row("Dec 15, 2017", "Star Wars Ep. V111: The Last Jedi", "$1,332,539,889")
    table.add_row("Dec 16, 2016", "Rouge One: A Star Wars Story", "$1,332,439,889")

    console = Console()
    console.print(table)

This produces the following output:

.. raw:: html

    <pre style="font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><span style="font-style: italic">                           Star Wars Movies                           </span>
    ┏━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┓
    ┃<span style="font-weight: bold">     Released </span>┃<span style="font-weight: bold"> Title                             </span>┃<span style="font-weight: bold">     Box Office </span>┃
    ┡━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━┩
    │<span style="color: #008080"> Dec 20, 2019 </span>│<span style="color: #800080"> Star Wars: The Rise of Skywalker  </span>│<span style="color: #008000">   $952,110,690 </span>│
    │<span style="color: #008080"> May 25, 2018 </span>│<span style="color: #800080"> Solo: A Star Wars Story           </span>│<span style="color: #008000">   $393,151,347 </span>│
    │<span style="color: #008080"> Dec 15, 2017 </span>│<span style="color: #800080"> Star Wars Ep. V111: The Last Jedi </span>│<span style="color: #008000"> $1,332,539,889 </span>│
    │<span style="color: #008080"> Dec 16, 2016 </span>│<span style="color: #800080"> Rouge One: A Star Wars Story      </span>│<span style="color: #008000"> $1,332,439,889 </span>│
    └──────────────┴───────────────────────────────────┴────────────────┘
    </pre>


Rich is quite smart about rendering the table. It will adjust the column widths to fit the contents and will wrap text if it doesn't fit. You can also add anything that Rich knows how to render as a title or row cell (even another table)!

You can set the border style by importing one of the preset :class:`~rich.box.Box` objects and setting the ``box`` argument in the table constructor. Here's an example that modifies the look of the Star Wars table::

    from rich import box
    table = Table(title="Star Wars Movies", box=box.MINIMAL_DOUBLE_HEAD)

See :ref:`appendix-box` for other box styles.

The :class:`~rich.table.Table` class offers a number of configuration options to set the look and feel of the table, including how borders are rendered and the style and alignment of the columns.
