# coding=utf-8

MARKDOWN = """Heading
=======

Sub-heading
-----------

### Heading

#### H4 Heading

##### H5 Heading

###### H6 Heading


Paragraphs are separated
by a blank line.

Two spaces at the end of a line  
produces a line break.

Text attributes _italic_, 
**bold**, `monospace`.

Horizontal rule:

---

Bullet list:

  * apples
  * oranges
  * pears

Numbered list:

  1. lather
  2. rinse
  3. repeat

An [example](http://example.com).

> Markdown uses email-style > characters for blockquoting.
>
> Lorem ipsum

![progress](https://github.com/textualize/rich/raw/master/imgs/progress.gif)


```
a=1
```

```python
import this
```

```somelang
foobar
```

"""

import io
import re

from rich.console import Console, RenderableType
from rich.markdown import Markdown

re_link_ids = re.compile(r"id=[\d\.\-]*?;.*?\x1b")


def replace_link_ids(render: str) -> str:
    """Link IDs have a random ID and system path which is a problem for
    reproducible tests.

    """
    return re_link_ids.sub("id=0;foo\x1b", render)


def render(renderable: RenderableType) -> str:
    console = Console(
        width=100, file=io.StringIO(), color_system="truecolor", legacy_windows=False
    )
    console.print(renderable)
    output = replace_link_ids(console.file.getvalue())
    return output


def test_markdown_render():
    markdown = Markdown(MARKDOWN, hyperlinks=False)
    rendered_markdown = render(markdown)
    print(repr(rendered_markdown))
    expected = "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n┃                                             \x1b[1mHeading\x1b[0m                                              ┃\n┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n\n\n                                            \x1b[1;4mSub-heading\x1b[0m                                             \n\n                                              \x1b[1mHeading\x1b[0m                                               \n\n                                             \x1b[1;2mH4 Heading\x1b[0m                                             \n\n                                             \x1b[4mH5 Heading\x1b[0m                                             \n\n                                             \x1b[3mH6 Heading\x1b[0m                                             \n\nParagraphs are separated by a blank line.                                                           \n\nTwo spaces at the end of a line                                                                     \nproduces a line break.                                                                              \n\nText attributes \x1b[3mitalic\x1b[0m, \x1b[1mbold\x1b[0m, \x1b[1;36;40mmonospace\x1b[0m.                                                            \n\nHorizontal rule:                                                                                    \n\n\x1b[33m────────────────────────────────────────────────────────────────────────────────────────────────────\x1b[0m\nBullet list:                                                                                        \n\n\x1b[1;33m • \x1b[0mapples                                                                                           \n\x1b[1;33m • \x1b[0moranges                                                                                          \n\x1b[1;33m • \x1b[0mpears                                                                                            \n\nNumbered list:                                                                                      \n\n\x1b[1;33m 1 \x1b[0mlather                                                                                           \n\x1b[1;33m 2 \x1b[0mrinse                                                                                            \n\x1b[1;33m 3 \x1b[0mrepeat                                                                                           \n\nAn \x1b[94mexample\x1b[0m (\x1b[4;34mhttp://example.com\x1b[0m).                                                                    \n\n\x1b[35m▌ \x1b[0m\x1b[35mMarkdown uses email-style > characters for blockquoting.\x1b[0m\x1b[35m                                        \x1b[0m\n\x1b[35m▌ \x1b[0m\x1b[35mLorem ipsum\x1b[0m\x1b[35m                                                                                     \x1b[0m\n\n🌆 progress                                                                                         \n\n\x1b[48;2;39;40;34m                                                                                                    \x1b[0m\n\x1b[48;2;39;40;34m \x1b[0m\x1b[38;2;248;248;242;48;2;39;40;34ma=1\x1b[0m\x1b[48;2;39;40;34m                                                                                               \x1b[0m\x1b[48;2;39;40;34m \x1b[0m\n\x1b[48;2;39;40;34m                                                                                                    \x1b[0m\n\n\x1b[48;2;39;40;34m                                                                                                    \x1b[0m\n\x1b[48;2;39;40;34m \x1b[0m\x1b[38;2;255;70;137;48;2;39;40;34mimport\x1b[0m\x1b[38;2;248;248;242;48;2;39;40;34m \x1b[0m\x1b[38;2;248;248;242;48;2;39;40;34mthis\x1b[0m\x1b[48;2;39;40;34m                                                                                       \x1b[0m\x1b[48;2;39;40;34m \x1b[0m\n\x1b[48;2;39;40;34m                                                                                                    \x1b[0m\n\n\x1b[48;2;39;40;34m                                                                                                    \x1b[0m\n\x1b[48;2;39;40;34m \x1b[0m\x1b[38;2;248;248;242;48;2;39;40;34mfoobar\x1b[0m\x1b[48;2;39;40;34m                                                                                            \x1b[0m\x1b[48;2;39;40;34m \x1b[0m\n\x1b[48;2;39;40;34m                                                                                                    \x1b[0m\n"
    assert rendered_markdown == expected


if __name__ == "__main__":
    markdown = Markdown(MARKDOWN, hyperlinks=False)
    rendered = render(markdown)
    print(rendered)
    print(repr(rendered))
