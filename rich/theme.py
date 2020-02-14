import configparser
from typing import Dict, IO

from .style import Style


class Theme:
    def __init__(self, styles: Dict[str, Style] = None):
        self.styles = styles or {}

    @property
    def config(self) -> str:
        """Get contents of a config file for this theme."""
        config_lines = ["[styles]"]
        append = config_lines.append
        for name, style in sorted(self.styles.items()):
            append(f"{name} = {style}")
        config = "\n".join(config_lines)
        return config

    @classmethod
    def from_file(cls, config_file: IO[str], source: str = None) -> "Theme":
        config = configparser.ConfigParser()
        config.read_file(config_file, source=source)
        styles = {name: Style.parse(value) for name, value in config.items("styles")}
        theme = Theme(styles)
        return theme

    @classmethod
    def read(cls, path: str) -> "Theme":
        with open(path, "rt") as config_file:
            return cls.from_file(config_file, source=path)
