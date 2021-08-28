from json import loads, dumps

from .text import Text
from .highlighter import JSONHighlighter, NullHighlighter


class JSON:
    """A rebderable which pretty prints JSON.

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
    j = """
{ "atomic": [false, true, null],
    "widget": {
    "debug": true,
    "window": {
        "title": "Sample Konfabulator Widget",
        "name": "main_window",
        "width": 500,
        "height": 500
    },
    "image": { 
        "src": "Images/Sun.png",
        "name": "sun1",
        "hOffset": 250,
        "vOffset": 250,
        "alignment": "center"
    },
    "text": {
        "data": "Click Here",
        "size": 36,
        "style": "bold",
        "name": "text1",
        "hOffset": 250,
        "vOffset": 100,
        "alignment": "center",
        "onMouseUp": "sun1.opacity = (sun1.opacity / 100) * 90;"
    }
}} 
    """
    from rich.console import Console

    console = Console()

    print(dumps(loads(j)))

    console.print(JSON(j), soft_wrap=True)
