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
    table.add_row("Dec 16, 2016", "Rogue One: A Star Wars Story", "$1,332,439,889")

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
    │<span style="color: #008080"> Dec 16, 2016 </span>│<span style="color: #800080"> Rogue One: A Star Wars Story      </span>│<span style="color: #008000"> $1,332,439,889 </span>│
    └──────────────┴───────────────────────────────────┴────────────────┘
    </pre>


Rich will calculate the optimal column sizes to fit your content, and will wrap text to fit if the terminal is not wide enough to fit the contents.

.. note::
    You are not limited to adding text in the ``add_row`` method. You can add anything that Rich knows how to render (including another table).

Table Options
~~~~~~~~~~~~~

There are a number of keyword arguments on the Table constructor you can use to define how a table should look.

- ``title`` Sets the title of the table (text shown above the table).
- ``caption`` Sets the table caption (text shown below the table).
- ``width`` Sets the desired width of the table (disables automatic width calculation).
- ``min_width`` Sets a minimum width for the table.
- ``box`` Sets one of the :ref:`appendix_box` styles for the table grid, or ``None`` for no grid.
- ``safe_box`` Set to ``True`` to force the table to generate ASCII characters rather than unicode.
- ``padding`` An integer, or tuple of 1, 2, or 4 values to set the padding on cells (see :ref:`Padding`).
- ``collapse_padding`` If True the padding of neighboring cells will be merged.
- ``pad_edge`` Set to False to remove padding around the edge of the table.
- ``expand`` Set to True to expand the table to the full available size.
- ``show_header`` Set to True to show a header, False to disable it.
- ``show_footer`` Set to True to show a footer, False to disable it.
- ``show_edge`` Set to False to disable the edge line around the table.
- ``show_lines`` Set to True to show lines between rows as well as header / footer.
- ``leading`` Additional space between rows.
- ``style`` A Style to apply to the entire table, e.g. "on blue"
- ``row_styles`` Set to a list of styles to style alternating rows. e.g. ``["dim", ""]`` to create *zebra stripes*
- ``header_style`` Set the default style for the header.
- ``footer_style`` Set the default style for the footer.
- ``border_style`` Set a style for border characters.
- ``title_style`` Set a style for the title.
- ``caption_style`` Set a style for the caption.
- ``title_justify`` Set the title justify method ("left", "right", "center", or "full")
- ``caption_justify`` Set the caption justify method ("left", "right", "center", or "full")
- ``highlight`` Set to True to enable automatic highlighting of cell contents.

Border Styles
~~~~~~~~~~~~~

You can set the border style by importing one of the preset :class:`~rich.box.Box` objects and setting the ``box`` argument in the table constructor. Here's an example that modifies the look of the Star Wars table::

    from rich import box
    table = Table(title="Star Wars Movies", box=box.MINIMAL_DOUBLE_HEAD)

See :ref:`appendix_box` for other box styles.

You can also set ``box=None`` to remove borders entirely.

The :class:`~rich.table.Table` class offers a number of configuration options to set the look and feel of the table, including how borders are rendered and the style and alignment of the columns.


Lines
~~~~~

By default, Tables will show a line under the header only. If you want to show lines between all rows add ``show_lines=True`` to the constructor.

You can also force a line on the next row by setting ``end_section=True`` on the call to :meth:`~rich.table.Table.add_row`, or by calling the :meth:`~rich.table.Table.add_section` to add a line between the current and subsequent rows.


Empty Tables
~~~~~~~~~~~~

Printing a table with no columns results in a blank line. If you are building a table dynamically and the data source has no columns, you might want to print something different. Here's how you might do that::

    if table.columns:
        print(table)
    else:
        print("[i]No data...[/i]")


Adding Columns
~~~~~~~~~~~~~~

You may also add columns by specifying them in the positional arguments of the :class:`~rich.table.Table` constructor. For example, we could construct a table with three columns like this::

    table = Table("Released", "Title", "Box Office", title="Star Wars Movies")

This allows you to specify the text of the column only. If you want to set other attributes, such as width and style, you can add a :class:`~rich.table.Column` class. Here's an example::

    from rich.table import Column, Table
    table = Table(
        "Released",
        "Title",
        Column(header="Box Office", justify="right"),
        title="Star Wars Movies"
    )

Column Options
~~~~~~~~~~~~~~

There are a number of options you can set on a column to modify how it will look.

- ``header_style`` Sets the style of the header, e.g. "bold magenta".
- ``footer_style`` Sets the style of the footer.
- ``style`` Sets a style that applies to the column. You could use this to highlight a column by setting the background with "on green" for example.
- ``justify`` Sets the text justify to one of "left", "center", "right", or "full".
- ``vertical`` Sets the vertical alignment of the cells in a column, to one of "top", "middle", or "bottom".
- ``width`` Explicitly set the width of a row to a given number of characters (disables automatic calculation).
- ``min_width`` When set to an integer will prevent the column from shrinking below this amount.
- ``max_width`` When set to an integer will prevent the column from growing beyond this amount.
- ``ratio`` Defines a ratio to set the column width. For instance, if there are 3 columns with a total of 6 ratio, and ``ratio=2`` then the column will be a third of the available size.
- ``no_wrap`` Set to True to prevent this column from wrapping.

Vertical Alignment
~~~~~~~~~~~~~~~~~~

You can define the vertical alignment of a column by setting the ``vertical`` parameter of the column. You can also do this per-cell by wrapping your text or renderable with a :class:`~rich.align.Align` class::


    table.add_row(Align("Title", vertical="middle"))

Grids
~~~~~

The Table class can also make a great layout tool. If you disable headers and borders you can use it to position content within the terminal. The alternative constructor :meth:`~rich.table.Table.grid` can create such a table for you.

For instance, the following code displays two pieces of text aligned to both the left and right edges of the terminal on a single line::


    from rich import print
    from rich.table import Table

    grid = Table.grid(expand=True)
    grid.add_column()
    grid.add_column(justify="right")
    grid.add_row("Raising shields", "[bold magenta]COMPLETED [green]:heavy_check_mark:")

    print(grid)
