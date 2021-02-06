.. _live:

Live Display
============

Rich can display continiuously updated information for any renderable.

To see some live display examples, try this from the command line::

    python -m rich.live

.. note::

    If you see ellipsis "...", this indicates that the terminal is not tall enough to show the full table.

Basic Usage
-----------

The basic usage can be split into two use cases.

1. Same Renderable
~~~~~~~~~~~~~~~~~~

When keeping the same renderable, you simply pass the :class:`~rich.console.RenderableType` you would like to see updating and provide
a ``refresh_per_second`` parameter. The Live :class:`~rich.live.Live` will automatically update the console at the provided refresh rate.


**Example**::

    import time

    from rich.live import Live
    from rich.table import Table

    table = Table()
    table.add_column("Row ID")
    table.add_column("Description")
    table.add_column("Level")

    with Live(table, refresh_per_second=4):  # update 4 times a second to feel fluid
        for row in range(12):
            time.sleep(0.4)  # arbitrary delay
            # update the renderable internally
            table.add_row(f"{row}", f"description {row}", "[red]ERROR")


2. New Renderable
~~~~~~~~~~~~~~~~~

You can also provide constant new renderable to :class:`~rich.live.Live` using the :meth:`~rich.live.Live.update` function. This allows you to
completely change what is rendered live.

**Example**::

    import random
    import time

    from rich.live import Live
    from rich.table import Table


    def generate_table() -> Table:

        table = Table()
        table.add_column("ID")
        table.add_column("Value")
        table.add_column("Status")

        for row in range(random.randint(2, 6)):
            value = random.random() * 100
            table.add_row(
                f"{row}", f"{value:3.2f}", "[red]ERROR" if value < 50 else "[green]SUCCESS"
            )
        return table


    with Live(refresh_per_second=4) as live:
        for _ in range(40):
            time.sleep(0.4)
            live.update(generate_table())

Advanced Usage
--------------

Transient Display
~~~~~~~~~~~~~~~~~

Normally when you exit live context manager (or call :meth:`~rich.live.Live.stop`) the last refreshed item remains in the terminal with the cursor on the following line.
You can also make the live display disappear on exit by setting ``transient=True`` on the Live constructor. Here's an example::

    with Live(transient=True) as live:
        ...

Auto refresh
~~~~~~~~~~~~

By default, the live display will refresh 4 times a second. You can set the refresh rate with the ``refresh_per_second`` argument on the :class:`~rich.live.Live` constructor.
You should set this to something lower than 4 if you know your updates will not be that frequent or higher for a smoother feeling.

You might want to disable auto-refresh entirely if your updates are not very frequent, which you can do by setting ``auto_refresh=False`` on the constructor.
If you disable auto-refresh you will need to call :meth:`~rich.live.Live.refresh` manually or :meth:`~rich.live.Live.update` with ``refresh=True``.

Vertical Overflow
~~~~~~~~~~~~~~~~~

By default, the live display will display ellipsis if the renderable is too large for the terminal. You can adjust this by setting the
``vertical_overflow`` argument on the :class:`~rich.live.Live` constructor.

- crop: Show renderable up to the terminal height. The rest is hidden.
- ellipsis: Similar to crop except last line of the terminal is replaced with "...". This is the default behavior.
- visible: Will allow the whole renderable to be shown. Note that the display cannot be properly cleared in this mode.

.. note::

    Once the live display stops on a non-transient renderable, the last frame will render as **visible** since it doesn't have to be cleared.

Complex Renders
~~~~~~~~~~~~~~~

Refer to the :ref:`Render Groups` about combining multiple :class:`RenderableType` together so that it may be passed into the :class:`~rich.live.Live` constructor
or :meth:`~rich.live.Live.update` method.

For more powerful structuring it is also possible to use nested tables.


Print / log
~~~~~~~~~~~

The Live class will create an internal Console object which you can access via ``live.console``. If you print or log to this console, the output will be displayed *above* the live display. Here's an example::

    import time

    from rich.live import Live
    from rich.table import Table

    table = Table()
    table.add_column("Row ID")
    table.add_column("Description")
    table.add_column("Level")

    with Live(table, refresh_per_second=4) as live:  # update 4 times a second to feel fluid
        for row in range(12):
            live.console.print("Working on row #{row}")
            time.sleep(0.4)
            table.add_row(f"{row}", f"description {row}", "[red]ERROR")


If you have another Console object you want to use, pass it in to the :class:`~rich.live.Live` constructor. Here's an example::

    from my_project import my_console

    with Live(console=my_console) as live:
        my_console.print("[bold blue]Starting work!")
        ...

.. note::

    If you are passing in a file console, the live display only show the last item once the live context is left.

Redirecting stdout / stderr
~~~~~~~~~~~~~~~~~~~~~~~~~~~

To avoid breaking the live display visuals, Rich will redirect ``stdout`` and ``stderr`` so that you can use the builtin ``print`` statement.
This feature is enabled by default, but you can disable by setting ``redirect_stdout`` or ``redirect_stderr`` to ``False``.


Examples
--------

See `table_movie.py <https://github.com/willmcgugan/rich/blob/master/examples/table_movie.py>`_ and
`top_lite_simulator.py <https://github.com/willmcgugan/rich/blob/master/examples/top_lite_simulator.py>`_
for deeper examples of live displaying.
