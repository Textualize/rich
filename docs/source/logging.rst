Logging Handler
===============

Rich supplies a :ref:`logging handler<logging>` which will format and colorize text written by Python's logging module.

Here's an example of how to set up a rich logger::

    import logging
    from rich.logging import RichHandler

    FORMAT = "%(message)s"
    logging.basicConfig(
        level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
    )

    log = logging.getLogger("rich")
    log.info("Hello, World!")

Rich logs won't render :ref:`console_markup` in logging by default as most libraries won't be aware of the need to escape literal square brackets, but you can enable it by setting ``markup=True`` on the handler. Alternatively you can enable it per log message by supplying the ``extra`` argument as follows::

    log.error("[bold red blink]Server is shutting down![/]", extra={"markup": True})

Similarly, the highlighter may be overridden per log message::

    log.error("123 will not be highlighted", extra={"highlighter": None})


Handle exceptions
-------------------

The :class:`~rich.logging.RichHandler` class may be configured to use Rich's :class:`~rich.traceback.Traceback` class to format exceptions, which provides more context than a built-in exception. To get beautiful exceptions in your logs set ``rich_tracebacks=True`` on the handler constructor::


    import logging
    from rich.logging import RichHandler

    logging.basicConfig(
        level="NOTSET",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)]
    )

    log = logging.getLogger("rich")
    try:
        print(1 / 0)
    except Exception:
        log.exception("unable print!")


There are a number of other options you can use to configure logging output, see the :class:`~rich.logging.RichHandler` reference for details.

Suppressing Frames
------------------

If you are working with a framework (click, django etc), you may only be interested in seeing the code from your own application within the traceback. You can exclude framework code by setting the `suppress` argument on `Traceback`, `install`, and `Console.print_exception`, which should be a list of modules or str paths.

Here's how you would exclude `click <https://click.palletsprojects.com/en/8.0.x/>`_ from Rich exceptions:: 

    import click
    import logging
    from rich.logging import RichHandler

    logging.basicConfig(
        level="NOTSET",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True, tracebacks_suppress=[click])]
    )

Suppressed frames will show the line and file only, without any code.