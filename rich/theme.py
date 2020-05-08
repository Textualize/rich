import configparser
from typing import IO, Mapping

from .default_styles import DEFAULT_STYLES
from .style import Style, StyleType


class Theme:
    """A container for style information, used by :class:`~rich.console.Console`.
    
    Args:
        styles (Dict[str, Style], optional): A mapping of style names on to styles. Defaults to None for empty styles.
        inherit (bool, optional): Switch to inherit default styles. Defaults to True.
    """

    def __init__(self, styles: Mapping[str, StyleType] = None, inherit: bool = True):
        self.styles = DEFAULT_STYLES.copy() if inherit else {}
        if styles is not None:
            self.styles.update(
                {
                    name: style if isinstance(style, Style) else Style.parse(style)
                    for name, style in styles.items()
                }
            )

    @property
    def config(self) -> str:
        """Get contents of a config file for this theme."""
        config = "[styles]\n" + "\n".join(
            f"{name} = {style}" for name, style in sorted(self.styles.items())
        )
        return config

    @classmethod
    def from_file(
        cls, config_file: IO[str], source: str = None, inherit: bool = True
    ) -> "Theme":
        """Load a theme from a text mode file.

        Args:
            config_file (IO[str]): An open conf file.
            source (str, optional): The filename of the open file. Defaults to None.
            inherit (bool, optional): Switch to inherit default styles. Defaults to True. 
        
        Returns:
            Theme: A New theme instance.
        """
        config = configparser.ConfigParser()
        config.read_file(config_file, source=source)
        styles = {name: Style.parse(value) for name, value in config.items("styles")}
        theme = Theme(styles, inherit=inherit)
        return theme

    @classmethod
    def read(cls, path: str, inherit: bool = True) -> "Theme":
        """Read a theme from a path.

        Args:
            path (str): Path to a config file readable by Python configparser module.            
            inherit (bool, optional): Switch to inherit default styles. Defaults to True. 
        
        Returns:
            Theme: A new theme instance.
        """
        with open(path, "rt") as config_file:
            return cls.from_file(config_file, source=path, inherit=inherit)


if __name__ == "__main__":  # pragma: no cover
    from .console import Console
    from .markup import escape

    console = Console()
    theme = Theme()
    console.print(escape(theme.config))
