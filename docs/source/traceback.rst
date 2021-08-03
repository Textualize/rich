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
