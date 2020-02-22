Traceback
=========

Rich can render Python tracebacks with syntax highlighting and formatting. Rich tracebacks are easier to read, and show more code, than standard Python tracebacks.


Printing tracebacks
-------------------

The :meth:`~rich.console.Console.print_exception` method will print a traceback for the current exception being handled. Here's an example::

    try:
        do_something()
    except:
        console.print_exception()


Traceback handler
-----------------

Rich can be installed as the default traceback handler so that all uncaught exceptions will be rendered with highlighting. Here's how::

    from rich.traceback import install
    install()