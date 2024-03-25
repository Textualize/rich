Columns
=======

Rich can render text or other Rich renderables in neat columns with the :class:`~rich.columns.Columns` class. To use, construct a Columns instance with an iterable of renderables and print it to the Console.

The following example is a very basic clone of the ``ls`` command in OSX / Linux to list directory contents::

    import os
    import sys

    from rich import print
    from rich.columns import Columns

    if len(sys.argv) < 2:
        print("Usage: python columns.py DIRECTORY")
    else:
        directory = os.listdir(sys.argv[1])
        columns = Columns(directory, equal=True, expand=True)
        print(columns)


See `columns.py <https://github.com/willmcgugan/rich/blob/master/examples/columns.py>`_ for an example which outputs columns containing more than just text. 

