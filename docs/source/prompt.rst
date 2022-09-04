Prompt
======

Rich has a number of :class:`~rich.prompt.Prompt` classes which ask a user for input and loop until a valid response is received (they all use the :ref:`Console API<Input>` internally). Here's a simple example::

    >>> from rich.prompt import Prompt
    >>> name = Prompt.ask("Enter your name")

The prompt may be given as a string (which may contain :ref:`console_markup` and emoji code) or as a :class:`~rich.text.Text` instance.

You can set a default value which will be returned if the user presses return without entering any text::

    >>> from rich.prompt import Prompt
    >>> name = Prompt.ask("Enter your name", default="Paul Atreides")

If you supply a list of choices, the prompt will loop until the user enters one of the choices::

    >>> from rich.prompt import Prompt
    >>> name = Prompt.ask("Enter your name", choices=["Paul", "Jessica", "Duncan"], default="Paul")

In addition to :class:`~rich.prompt.Prompt` which returns strings, you can also use :class:`~rich.prompt.IntPrompt` which asks the user for an integer, and :class:`~rich.prompt.FloatPrompt` for floats.

The :class:`~rich.prompt.Confirm` class is a specialized prompt which may be used to ask the user a simple yes / no question. Here's an example::

    >>> from rich.prompt import Confirm
    >>> is_rich_great = Confirm.ask("Do you like rich?")
    >>> assert is_rich_great

The Prompt class was designed to be customizable via inheritance. See `prompt.py <https://github.com/willmcgugan/rich/blob/master/rich/prompt.py>`_ for examples.

To see some of the prompts in action, run the following command from the command line::

    python -m rich.prompt
