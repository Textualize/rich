class ConsoleError(Exception):
    """An error in console operation."""


class StyleError(Exception):
    """An error in styles."""


class StyleSyntaxError(ConsoleError):
    """Style was badly formatted."""


class MissingStyle(StyleError):
    """No such style."""


class StyleStackError(ConsoleError):
    """Style stack is invalid."""
