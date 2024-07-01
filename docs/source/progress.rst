.. _progress:

Progress Display
================

Rich can display continuously updated information regarding the progress of long running tasks / file copies etc. The information displayed is configurable, the default will display a description of the 'task', a progress bar, percentage complete, and estimated time remaining.

Rich progress display supports multiple tasks, each with a bar and progress information. You can use this to track concurrent tasks where the work is happening in threads or processes.

To see how the progress display looks, try this from the command line::

    python -m rich.progress


.. note::

    Progress works with Jupyter notebooks, with the caveat that auto-refresh is disabled. You will need to explicitly call :meth:`~rich.progress.Progress.refresh` or set ``refresh=True`` when calling :meth:`~rich.progress.Progress.update`. Or use the :func:`~rich.progress.track` function which does a refresh automatically on each loop.

Basic Usage
-----------

For basic usage call the :func:`~rich.progress.track` function, which accepts a sequence (such as a list or range object) and an optional description of the job you are working on. The track function will yield values from the sequence and update the progress information on each iteration. Here's an example::

    import time
    from rich.progress import track

    for i in track(range(20), description="Processing..."):
        time.sleep(1)  # Simulate work being done

Advanced usage
--------------

If you require multiple tasks in the display, or wish to configure the columns in the progress display, you can work directly with the :class:`~rich.progress.Progress` class. Once you have constructed a Progress object, add task(s) with (:meth:`~rich.progress.Progress.add_task`) and update progress with :meth:`~rich.progress.Progress.update`.

The Progress class is designed to be used as a *context manager* which will start and stop the progress display automatically.

Here's a simple example::

    import time

    from rich.progress import Progress

    with Progress() as progress:

        task1 = progress.add_task("[red]Downloading...", total=1000)
        task2 = progress.add_task("[green]Processing...", total=1000)
        task3 = progress.add_task("[cyan]Cooking...", total=1000)

        while not progress.finished:
            progress.update(task1, advance=0.5)
            progress.update(task2, advance=0.3)
            progress.update(task3, advance=0.9)
            time.sleep(0.02)

The ``total`` value associated with a task is the number of steps that must be completed for the progress to reach 100%. A *step* in this context is whatever makes sense for your application; it could be number of bytes of a file read, or number of images processed, etc.


Updating tasks
~~~~~~~~~~~~~~

When you call :meth:`~rich.progress.Progress.add_task` you get back a `Task ID`. Use this ID to call :meth:`~rich.progress.Progress.update` whenever you have completed some work, or any information has changed. Typically you will need to update ``completed`` every time you have completed a step. You can do this by setting ``completed`` directly or by setting ``advance`` which will add to the current ``completed`` value.

The :meth:`~rich.progress.Progress.update` method collects keyword arguments which are also associated with the task. Use this to supply any additional information you would like to render in the progress display. The additional arguments are stored in ``task.fields`` and may be referenced in :ref:`Column classes<Columns>`.

Hiding tasks
~~~~~~~~~~~~

You can show or hide tasks by updating the tasks ``visible`` value. Tasks are visible by default, but you can also add an invisible task by calling :meth:`~rich.progress.Progress.add_task` with ``visible=False``.


Transient progress
~~~~~~~~~~~~~~~~~~

Normally when you exit the progress context manager (or call :meth:`~rich.progress.Progress.stop`) the last refreshed display remains in the terminal with the cursor on the following line. You can also make the progress display disappear on exit by setting ``transient=True`` on the Progress constructor. Here's an example::

    with Progress(transient=True) as progress:
        task = progress.add_task("Working", total=100)
        do_work(task)

Transient progress displays are useful if you want more minimal output in the terminal when tasks are complete.

Indeterminate progress
~~~~~~~~~~~~~~~~~~~~~~

When you add a task it is automatically *started*, which means it will show a progress bar at 0% and the time remaining will be calculated from the current time. This may not work well if there is a long delay before you can start updating progress; you may need to wait for a response from a server or count files in a directory (for example). In these cases you can call :meth:`~rich.progress.Progress.add_task` with ``start=False`` or ``total=None`` which will display a pulsing animation that lets the user know something is working. This is known as an *indeterminate* progress bar. When you have the number of steps you can call :meth:`~rich.progress.Progress.start_task` which will display the progress bar at 0%, then :meth:`~rich.progress.Progress.update` as normal.

Auto refresh
~~~~~~~~~~~~

By default, the progress information will refresh 10 times a second. You can set the refresh rate with the ``refresh_per_second`` argument on the :class:`~rich.progress.Progress` constructor. You should set this to something lower than 10 if you know your updates will not be that frequent.

You might want to disable auto-refresh entirely if your updates are not very frequent, which you can do by setting ``auto_refresh=False`` on the constructor. If you disable auto-refresh you will need to call :meth:`~rich.progress.Progress.refresh` manually after updating your task(s).


Expand
~~~~~~

The progress bar(s) will use only as much of the width of the terminal as required to show the task information. If you set the ``expand`` argument on the Progress constructor, then Rich will stretch the progress display to the full available width.


Columns
~~~~~~~

You may customize the columns in the progress display with the positional arguments to the :class:`~rich.progress.Progress` constructor. The columns are specified as either a `format string <https://docs.python.org/3/library/string.html#formatspec>`_ or a :class:`~rich.progress.ProgressColumn` object.

Format strings will be rendered with a single value `"task"` which will be a :class:`~rich.progress.Task` instance. For example ``"{task.description}"`` would display the task description in the column, and ``"{task.completed} of {task.total}"`` would display how many of the total steps have been completed. Additional fields passed via keyword arguments to `~rich.progress.Progress.update` are store in ``task.fields``. You can add them to a format string with the following syntax: ``"extra info: {task.fields[extra]}"``.

The default columns are equivalent to the following::

    progress = Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TimeRemainingColumn(),
    )

To create a Progress with your own columns in addition to the defaults, use :meth:`~rich.progress.Progress.get_default_columns`::

    progress = Progress(
        SpinnerColumn(),
        *Progress.get_default_columns(),
        TimeElapsedColumn(),
    )

The following column objects are available:

- :class:`~rich.progress.BarColumn` Displays the bar.
- :class:`~rich.progress.TextColumn` Displays text.
- :class:`~rich.progress.TimeElapsedColumn` Displays the time elapsed.
- :class:`~rich.progress.TimeRemainingColumn` Displays the estimated time remaining.
- :class:`~rich.progress.MofNCompleteColumn` Displays completion progress as ``"{task.completed}/{task.total}"`` (works best if completed and total are ints).
- :class:`~rich.progress.FileSizeColumn` Displays progress as file size (assumes the steps are bytes).
- :class:`~rich.progress.TotalFileSizeColumn` Displays total file size (assumes the steps are bytes).
- :class:`~rich.progress.DownloadColumn` Displays download progress (assumes the steps are bytes).
- :class:`~rich.progress.TransferSpeedColumn` Displays transfer speed (assumes the steps are bytes).
- :class:`~rich.progress.SpinnerColumn` Displays a "spinner" animation.
- :class:`~rich.progress.RenderableColumn` Displays an arbitrary Rich renderable in the column.

To implement your own columns, extend the :class:`~rich.progress.ProgressColumn` class and use it as you would the other columns.


Table Columns
~~~~~~~~~~~~~

Rich builds a :class:`~rich.table.Table` for the tasks in the Progress instance. You can customize how the columns of this *tasks table* are created by specifying the ``table_column`` argument in the Column constructor, which should be a :class:`~rich.table.Column` instance.

The following example demonstrates a progress bar where the description takes one third of the width of the terminal, and the bar takes up the remaining two thirds::

    from time import sleep

    from rich.table import Column
    from rich.progress import Progress, BarColumn, TextColumn

    text_column = TextColumn("{task.description}", table_column=Column(ratio=1))
    bar_column = BarColumn(bar_width=None, table_column=Column(ratio=2))
    progress = Progress(text_column, bar_column, expand=True)

    with progress:
        for n in progress.track(range(100)):
            progress.print(n)
            sleep(0.1)


Print / log
~~~~~~~~~~~

The Progress class will create an internal Console object which you can access via ``progress.console``. If you print or log to this console, the output will be displayed *above* the progress display. Here's an example::

    with Progress() as progress:
        task = progress.add_task("twiddling thumbs", total=10)
        for job in range(10):
            progress.console.print(f"Working on job #{job}")
            run_job(job)
            progress.advance(task)

If you have another Console object you want to use, pass it in to the :class:`~rich.progress.Progress` constructor. Here's an example::

    from my_project import my_console

    with Progress(console=my_console) as progress:
        my_console.print("[bold blue]Starting work!")
        do_work(progress)


Redirecting stdout / stderr
~~~~~~~~~~~~~~~~~~~~~~~~~~~

To avoid breaking the progress display visuals, Rich will redirect ``stdout`` and ``stderr`` so that you can use the built-in ``print`` statement. This feature is enabled by default, but you can disable by setting ``redirect_stdout`` or ``redirect_stderr`` to ``False``


Customizing
~~~~~~~~~~~

If the :class:`~rich.progress.Progress` class doesn't offer exactly what you need in terms of a progress display, you can override the :class:`~rich.progress.Progress.get_renderables` method. For example, the following class will render a :class:`~rich.panel.Panel` around the progress display::

    from rich.panel import Panel
    from rich.progress import Progress

    class MyProgress(Progress):
        def get_renderables(self):
            yield Panel(self.make_tasks_table(self.tasks))

Reading from a file
~~~~~~~~~~~~~~~~~~~

Rich provides an easy way to generate a progress bar while reading a file. If you call :func:`~rich.progress.open` it will return a context manager which displays a progress bar while you read. This is particularly useful when you can't easily modify the code that does the reading.

The following example demonstrates how we might show progress when reading a JSON file::

    import json
    import rich.progress

    with rich.progress.open("data.json", "rb") as file:
        data = json.load(file)
    print(data)

If you already have a file object, you can call :func:`~rich.progress.wrap_file` which returns a context manager that wraps your file so that it displays a progress bar. If you use this function you will need to set the number of bytes or characters you expect to read.

Here's an example that reads a url from the internet::

    from time import sleep
    from urllib.request import urlopen

    from rich.progress import wrap_file

    response = urlopen("https://www.textualize.io")
    size = int(response.headers["Content-Length"])

    with wrap_file(response, size) as file:
        for line in file:
            print(line.decode("utf-8"), end="")
            sleep(0.1)


If you expect to be reading from multiple files, you can use :meth:`~rich.progress.Progress.open` or :meth:`~rich.progress.Progress.wrap_file` to add a file progress to an existing Progress instance.

See `cp_progress.py <https://github.com/willmcgugan/rich/blob/master/examples/cp_progress.py>`_ for a minimal clone of the ``cp`` command which shows a progress bar as the file is copied.


Multiple Progress
-----------------

You can't have different columns per task with a single Progress instance. However, you can have as many Progress instances as you like in a :ref:`live`. See `live_progress.py <https://github.com/willmcgugan/rich/blob/master/examples/live_progress.py>`_ and `dynamic_progress.py <https://github.com/willmcgugan/rich/blob/master/examples/dynamic_progress.py>`_ for examples of using multiple Progress instances.

Example
-------

See `downloader.py <https://github.com/willmcgugan/rich/blob/master/examples/downloader.py>`_ for a realistic application of a progress display. This script can download multiple concurrent files with a progress bar, transfer speed and file size.
