Traceback
=========

Rich can render Python tracebacks with syntax highlighting and formatting. Rich tracebacks are easier to read and show more code than standard Python tracebacks.

To see an example of a Rich traceback, running the following command::

    python -m rich.traceback


Printing tracebacks
-------------------

The :meth:`~rich.console.Console.print_exception` method will print a traceback for the current exception being handled. Here's an example::

    from rich.console import Console
    console = Console()

    try:
        do_something()
    except Exception:        
        console.print_exception(show_locals=True)

The ``show_locals=True`` parameter causes Rich to display the value of local variables for each frame of the traceback.
 
See `exception.py <https://github.com/willmcgugan/rich/blob/master/examples/exception.py>`_ for a larger example.


Traceback handler
-----------------

Rich can be installed as the default traceback handler so that all uncaught exceptions will be rendered with highlighting. Here's how::

    from rich.traceback import install
    install(show_locals=True)

There are a few options to configure the traceback handler, see :func:`~rich.traceback.install` for details.


Suppressing Frames
------------------

If you are working with a framework (click, django etc), you may only be interested in seeing the code from your own application within the traceback. You can exclude framework code by setting the `suppress` argument on `Traceback`, `install`, and `Console.print_exception`, which should be a list of modules or str paths.

Here's how you would exclude [click](https://click.palletsprojects.com/en/8.0.x/) from Rich exceptions:: 

    import click
    from rich.traceback import install
    install(suppress=[click])

Suppressed frames will show the line and file only, without any code.

Max Frames
----------

A recursion error can generate very large tracebacks that take a while to render and contain a lot of repetitive frames. Rich guards against this with a `max_frames` argument, which defaults to 100. If a traceback contains more than 100 frames then only the first 50, and last 50 will be shown. You can disable this feature by setting `max_frames` to 0.

Here's an example of printing an recursive error::

    from rich.console import Console


    def foo(n):
        return bar(n)


    def bar(n):
        return foo(n)


    console = Console()

    try:
        foo(1)
    except Exception:
        console.print_exception(max_frames=20)