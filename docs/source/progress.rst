.. _progress:

Progress Display
================

Rich can display continuously updated information regarding the progress of long running tasks / file copies etc. The information displayed is configurable, the default will display a description of the 'task', a progress bar, percentage complete, and estimated time remaining.

Rich progress display supports multiple tasks, each with a bar and progress information. You can use this to track concurrent tasks where the work is happening in threads or processes.

To see how the progress display looks, try this from the command line::

    python -m rich.progress

Basic Usage
-----------

For basic usage call the :func:`~rich.progress.track` function, which accepts a sequence (such as a list or range object) and an optional description of the job you are working on. The track method will yield values from the sequence and update the progress information on each iteration. Here's an example::

    from rich.progress import track

    for n in track(range(n), description="Processing..."):
        do_work(n)

Advanced usage
--------------

If you require multiple tasks in the display, or wish to configure the columns in the progress display, you can work directly with the :class:`~rich.progress.Progress` class. Once you have constructed a Progress object, add task(s) with (:meth:`~rich.progress.Progress.add_task`) and update progress with :meth:`~rich.progress.Progress.update`.

The Progress class is designed to be used as a *context manager* which will start and stop the progress display automatically.

Here's a simple example::

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

Starting Tasks
~~~~~~~~~~~~~~

When you add a task it is automatically *started* which means it will show a progress bar at 0% and the time remaining will be calculated from the current time. Occasionally this may not work well if there is a long delay before you can start updating progress, you may need to wait for a response from a server, or count files in a directory (for example) before you can begin tracking progress. In these cases you can call :meth:`~rich.progress.Progress.add_task` with ``start=False`` which will display the a pulsing animation that lets the user know something is working. When you have the number of steps you can call :meth:`~rich.progress.Progress.start_task` which will display the progress bar at 0%, then :meth:`~rich.progress.Progress.update` as normal.


Updating Tasks
~~~~~~~~~~~~~~

When you add a task you get back a `Task ID`. Use this ID to call :meth:`~rich.progress.Progress.update` whenever you have completed some work, or any information has changed.

Auto refresh
~~~~~~~~~~~~

By default, the progress information will auto refresh at 10 times a second. Refreshing in a predictable rate can make numbers more readable if they are updating very quickly. Auto refresh can also prevent excessive rendering to the terminal.

You can disable auto-refresh by setting ``auto_refresh=False`` on the constructor and call :meth:`~rich.progress.Progress.refresh` manually when there are updates to display.

Columns
~~~~~~~

You may customize the columns in the progress display with the positional arguments to the :class:`~rich.progress.Progress` constructor. The columns are specified as either a format string or a :class:`~rich.progress.ProgressColumn` object.

Format strings will be rendered with a single value `"task"` which will be a :class:`~rich.progress.Task` instance. For example ``"{task.description}"`` would display the task description in the column, and ``"{task.completed} of {task.total}"`` would display how many of the total steps have been completed.

The defaults are roughly equivalent to the following::

    progress = Progress(
        "[progress.description]{task.description}",
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.0f}%",
        TimeRemainingColumn(),
    )

The following column objects are available:

- :class:`~rich.progress.BarColumn` Displays the bar.
- :class:`~rich.progress.TextColumn` Displays text.
- :class:`~rich.progress.TimeRemainingColumn` Displays the estimated time remaining.
- :class:`~rich.progress.FileSizeColumn` Displays progress as file size (assumes the steps are bytes).
- :class:`~rich.progress.TotalFileSizeColumn` Displays total file size (assumes the steps are bytes).
- :class:`~rich.progress.DownloadColumn` Displays download progress (assumes the steps are bytes).
- :class:`~rich.progress.TransferSpeedColumn` Displays transfer speed (assumes the steps are bytes.

Print / log
~~~~~~~~~~~

When a progress display is running, printing or logging anything directly to the console will break the visuals. To work around this, the Progress class provides :meth:`~rich.progress.Progress.print` and :meth:`~rich.progress.Progress.log` which work the same as their counterparts on :class:`~rich.console.Console` but will move the cursor and refresh automatically -- ensure that everything renders properly.


Extending
~~~~~~~~~

If the progress API doesn't offer exactly what you need in terms of a progress display, you can extend the :class:`~rich.progress.Progress` class by overriding the :class:`~rich.progress.Progress.get_renderables` method. For example, the following class will render a :class:`~rich.panel.Panel` around the progress display::

    from rich.panel import Panel
    from rich.progress import Progress

    class MyProgress(Progress):
        def get_renderables(self):
            yield Panel(self.make_tasks_table(self.tasks))            


Example
-------

See `downloader.py <https://github.com/willmcgugan/rich/blob/master/examples/downloader.py>`_ for a realistic application of a progress display. This script can download multiple concurrent files while displaying progress with transfer speed and file size.
