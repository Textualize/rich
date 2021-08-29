from json import loads, dumps
from typing import Any

from .text import Text
from .highlighter import JSONHighlighter, NullHighlighter


class JSON:
    """A renderable which pretty prints JSON.

    Args:
        json (str): JSON encoded data.
        indent (int, optional): Number of characters to indent by. Defaults to True.
        highlight (bool, optional): Enable highlighting. Defaults to 2.
    """

    def __init__(
        self, json: str, indent: int = 2, highlight: bool = True, key: Any = None
    ) -> None:
        data = loads(json)
        if key and isinstance(data, dict):
            data = data.get(key)
        json = dumps(data, indent=indent)
        highlighter = JSONHighlighter() if highlight else NullHighlighter()
        self.text = highlighter(json)
        self.text.no_wrap = True
        self.text.overflow = None

    @classmethod
    def from_data(
        cls, data: Any, indent: int = 2, highlight: bool = True, key: Any = None
    ) -> "JSON":
        """Encodes a JSON object from arbitrary data.

        Returns:
            Args:
                data (Any): An object that may be encoded in to JSON
                indent (int, optional): Number of characters to indent by. Defaults to 2.
                highlight (bool, optional): Enable highlighting. Defaults to True.
        """
        json_instance: "JSON" = cls.__new__(cls)
        if key and isinstance(data, dict):
            data = data.get(key)
        json = dumps(data, indent=indent)
        highlighter = JSONHighlighter() if highlight else NullHighlighter()
        json_instance.text = highlighter(json)
        json_instance.text.no_wrap = True
        json_instance.text.overflow = None
        return json_instance

    def __rich__(self) -> Text:
        return self.text


if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Pretty print json")
    parser.add_argument(
        "path",
        metavar="PATH",
        help="path to file, or - for stdin",
    )
    parser.add_argument(
        "-i",
        "--indent",
        metavar="SPACES",
        type=int,
        help="Number of spaces in an indent",
        default=2,
    )
    parser.add_argument(
        "-k",
        "--key",
        metavar="SPACES",
        type=str,
        help="print value(s) of a key from the json",
        default=None,
    )
    args = parser.parse_args()
    from rich.console import Console

    console = Console()
    error_console = Console(stderr=True)

    try:
        with open(args.path, "rt") as json_file:
            json_data = json_file.read()
    except Exception as error:
        error_console.print(f"Unable to read {args.path!r}; {error}")
        sys.exit(-1)

    console.print(JSON(json_data, indent=args.indent, key=args.key), soft_wrap=True)
