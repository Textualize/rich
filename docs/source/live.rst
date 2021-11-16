.. _live:

Live Display
============

Progress bars and status indicators use a *live* display to animate parts of the terminal. You can build custom live displays with the :class:`~rich.live.Live` class. 

For a demonstration of a live display, run the following command::

    python -m rich.live

.. note::

    If you see ellipsis "...", this indicates that the terminal is not tall enough to show the full table.

Basic usage
~~~~~~~~~~~

To create a live display, construct a :class:`~rich.live.Live` object with a renderable and use it as a context manager. The live display will persist for the duration of the context. You can update the renderable to update the display::


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


Updating the renderable
~~~~~~~~~~~~~~~~~~~~~~~

You can also change the renderable on-the-fly by calling the :meth:`~rich.live.Live.update` method. This may be useful if the information you wish to display is too dynamic to generate by updating a single renderable. Here is an example::

    import random
    import time

    from rich.live import Live
    from rich.table import Table


    def generate_table() -> Table:
        """Make a new table."""
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


    with Live(generate_table(), refresh_per_second=4) as live:
        for _ in range(40):
            time.sleep(0.4)
            live.update(generate_table())


Alternate screen
~~~~~~~~~~~~~~~~

You can opt to show a Live display in the "alternate screen" by setting ``screen=True`` on the constructor. This will allow your live display to go full screen and restore the command prompt on exit. 

You can use this feature in combination with :ref:`Layout` to display sophisticated terminal "applications".

Transient display
~~~~~~~~~~~~~~~~~

Normally when you exit live context manager (or call :meth:`~rich.live.Live.stop`) the last refreshed item remains in the terminal with the cursor on the following line.
You can also make the live display disappear on exit by setting ``transient=True`` on the Live constructor. 

Auto refresh
~~~~~~~~~~~~

By default, the live display will refresh 4 times a second. You can set the refresh rate with the ``refresh_per_second`` argument on the :class:`~rich.live.Live` constructor.
You should set this to something lower than 4 if you know your updates will not be that frequent or higher for a smoother feeling.

You might want to disable auto-refresh entirely if your updates are not very frequent, which you can do by setting ``auto_refresh=False`` on the constructor.
If you disable auto-refresh you will need to call :meth:`~rich.live.Live.refresh` manually or :meth:`~rich.live.Live.update` with ``refresh=True``.

Vertical overflow
~~~~~~~~~~~~~~~~~

By default, the live display will display ellipsis if the renderable is too large for the terminal. You can adjust this by setting the
``vertical_overflow`` argument on the :class:`~rich.live.Live` constructor.

- "crop" Show renderable up to the terminal height. The rest is hidden.
- "ellipsis" Similar to crop except last line of the terminal is replaced with "...". This is the default behavior.
- "visible" Will allow the whole renderable to be shown. Note that the display cannot be properly cleared in this mode.

.. note::

    Once the live display stops on a non-transient renderable, the last frame will render as **visible** since it doesn't have to be cleared.


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
            live.console.print(f"Working on row #{row}")
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

Nesting Lives
-------------

Note that only a single live context may be active at any one time. The following will raise a :class:`~rich.errors.LiveError` because status also uses Live::

    with Live(table, console=console):
        with console.status("working"):  # Will not work
            do_work()

In practice this is rarely a problem because you can display any combination of renderables in a Live context.

Examples
--------

See `table_movie.py <https://github.com/willmcgugan/rich/blob/master/examples/table_movie.py>`_ and
`top_lite_simulator.py <https://github.com/willmcgugan/rich/blob/master/examples/top_lite_simulator.py>`_
for deeper examples of live displaying.
