from json import loads, dumps

from .text import Text
from .highlighter import JSONHighlighter, NullHighlighter


class JSON:
    """A renderable which pretty prints JSON.

    Args:
        json (str): JSON encoded data.
        indent (int, optional): Number of characters to indent by. Defaults to True.
        highlight (bool, optional): Enable highlighting. Defaults to True.
    """

    def __init__(self, json: str, indent: int = 4, highlight: bool = True) -> None:
        data = loads(json)
        json = dumps(data, indent=indent)
        highlighter = JSONHighlighter() if highlight else NullHighlighter()
        self.text = highlighter(json)
        self.text.no_wrap = True
        self.text.overflow = None

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

    console.print(JSON(json_data), soft_wrap=True)
