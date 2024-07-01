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

    import this


1. List item

       Code block
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
    print(repr(output))
    return output


def test_markdown_render():
    markdown = Markdown(MARKDOWN)
    rendered_markdown = render(markdown)
    expected = "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n┃                                             \x1b[1mHeading\x1b[0m                                              ┃\n┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n\n\n                                            \x1b[1;4mSub-heading\x1b[0m                                             \n\n                                              \x1b[1mHeading\x1b[0m                                               \n\n                                             \x1b[1;2mH4 Heading\x1b[0m                                             \n\n                                             \x1b[4mH5 Heading\x1b[0m                                             \n\n                                             \x1b[3mH6 Heading\x1b[0m                                             \n\nParagraphs are separated by a blank line.                                                           \n\nTwo spaces at the end of a line                                                                     \nproduces a line break.                                                                              \n\nText attributes \x1b[3mitalic\x1b[0m, \x1b[1mbold\x1b[0m, \x1b[1;36;40mmonospace\x1b[0m.                                                            \n\nHorizontal rule:                                                                                    \n\n\x1b[33m────────────────────────────────────────────────────────────────────────────────────────────────────\x1b[0m\nBullet list:                                                                                        \n\n\x1b[1;33m • \x1b[0mapples                                                                                           \n\x1b[1;33m • \x1b[0moranges                                                                                          \n\x1b[1;33m • \x1b[0mpears                                                                                            \n\nNumbered list:                                                                                      \n\n\x1b[1;33m 1 \x1b[0mlather                                                                                           \n\x1b[1;33m 2 \x1b[0mrinse                                                                                            \n\x1b[1;33m 3 \x1b[0mrepeat                                                                                           \n\nAn \x1b]8;id=0;foo\x1b\\\x1b[4;34mexample\x1b[0m\x1b]8;;\x1b\\.                                                                                         \n\n\x1b[35m▌ \x1b[0m\x1b[35mMarkdown uses email-style > characters for blockquoting.\x1b[0m\x1b[35m                                        \x1b[0m\n\x1b[35m▌ \x1b[0m\x1b[35mLorem ipsum\x1b[0m\x1b[35m                                                                                     \x1b[0m\n\n🌆 \x1b]8;id=0;foo\x1b\\progress\x1b]8;;\x1b\\                                                                                         \n\n\x1b[48;2;39;40;34m                                                                                                    \x1b[0m\n\x1b[48;2;39;40;34m \x1b[0m\x1b[38;2;248;248;242;48;2;39;40;34ma=1\x1b[0m\x1b[48;2;39;40;34m                                                                                               \x1b[0m\x1b[48;2;39;40;34m \x1b[0m\n\x1b[48;2;39;40;34m                                                                                                    \x1b[0m\n\n\x1b[48;2;39;40;34m                                                                                                    \x1b[0m\n\x1b[48;2;39;40;34m \x1b[0m\x1b[38;2;255;70;137;48;2;39;40;34mimport\x1b[0m\x1b[38;2;248;248;242;48;2;39;40;34m \x1b[0m\x1b[38;2;248;248;242;48;2;39;40;34mthis\x1b[0m\x1b[48;2;39;40;34m                                                                                       \x1b[0m\x1b[48;2;39;40;34m \x1b[0m\n\x1b[48;2;39;40;34m                                                                                                    \x1b[0m\n\n\x1b[48;2;39;40;34m                                                                                                    \x1b[0m\n\x1b[48;2;39;40;34m \x1b[0m\x1b[38;2;248;248;242;48;2;39;40;34mfoobar\x1b[0m\x1b[48;2;39;40;34m                                                                                            \x1b[0m\x1b[48;2;39;40;34m \x1b[0m\n\x1b[48;2;39;40;34m                                                                                                    \x1b[0m\n\n\x1b[48;2;39;40;34m                                                                                                    \x1b[0m\n\x1b[48;2;39;40;34m \x1b[0m\x1b[38;2;248;248;242;48;2;39;40;34mimport this\x1b[0m\x1b[48;2;39;40;34m                                                                                       \x1b[0m\x1b[48;2;39;40;34m \x1b[0m\n\x1b[48;2;39;40;34m                                                                                                    \x1b[0m\n\n\x1b[1;33m 1 \x1b[0mList item                                                                                        \n\x1b[1;33m   \x1b[0m\x1b[48;2;39;40;34m                                                                                                 \x1b[0m\n\x1b[1;33m   \x1b[0m\x1b[48;2;39;40;34m \x1b[0m\x1b[38;2;248;248;242;48;2;39;40;34mCode block\x1b[0m\x1b[48;2;39;40;34m                                                                                     \x1b[0m\x1b[48;2;39;40;34m \x1b[0m\n\x1b[1;33m   \x1b[0m\x1b[48;2;39;40;34m                                                                                                 \x1b[0m\n"
    assert rendered_markdown == expected


def test_inline_code():
    markdown = Markdown(
        "inline `import this` code",
        inline_code_lexer="python",
        inline_code_theme="emacs",
    )
    result = render(markdown)
    expected = "inline \x1b[1;38;2;170;34;255;48;2;248;248;248mimport\x1b[0m\x1b[38;2;0;0;0;48;2;248;248;248m \x1b[0m\x1b[1;38;2;0;0;255;48;2;248;248;248mthis\x1b[0m code                                                                             \n"
    print(result)
    print(repr(result))
    assert result == expected


def test_markdown_table():
    markdown = Markdown(
        """\
| Year |                      Title                       | Director          |  Box Office (USD) |
|------|:------------------------------------------------:|:------------------|------------------:|
| 1982 |            *E.T. the Extra-Terrestrial*          | Steven Spielberg  |    $792.9 million |
| 1980 |  Star Wars: Episode V – The Empire Strikes Back  | Irvin Kershner    |    $538.4 million |
| 1983 |    Star Wars: Episode VI – Return of the Jedi    | Richard Marquand  |    $475.1 million |
| 1981 |             Raiders of the Lost Ark              | Steven Spielberg  |    $389.9 million |
| 1984 |       Indiana Jones and the Temple of Doom       | Steven Spielberg  |    $333.1 million |
"""
    )
    result = render(markdown)
    expected = "\n                                                                                               \n \x1b[1m \x1b[0m\x1b[1mYear\x1b[0m\x1b[1m \x1b[0m \x1b[1m \x1b[0m\x1b[1m                    Title                     \x1b[0m\x1b[1m \x1b[0m \x1b[1m \x1b[0m\x1b[1mDirector        \x1b[0m\x1b[1m \x1b[0m \x1b[1m \x1b[0m\x1b[1mBox Office (USD)\x1b[0m\x1b[1m \x1b[0m \n ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ \n  1982             \x1b[3mE.T. the Extra-Terrestrial\x1b[0m             Steven Spielberg     $792.9 million  \n  1980   Star Wars: Episode V – The Empire Strikes Back   Irvin Kershner       $538.4 million  \n  1983     Star Wars: Episode VI – Return of the Jedi     Richard Marquand     $475.1 million  \n  1981              Raiders of the Lost Ark               Steven Spielberg     $389.9 million  \n  1984        Indiana Jones and the Temple of Doom        Steven Spielberg     $333.1 million  \n                                                                                               \n"
    assert result == expected


def test_inline_styles_in_table():
    """Regression test for https://github.com/Textualize/rich/issues/3115"""
    markdown = Markdown(
        """\
| Year | This **column** displays _the_ movie _title_ ~~description~~ | Director          |  Box Office (USD) |
|------|:----------------------------------------------------------:|:------------------|------------------:|
| 1982 | *E.T. the Extra-Terrestrial* ([Wikipedia article](https://en.wikipedia.org/wiki/E.T._the_Extra-Terrestrial)) | Steven Spielberg  |    $792.9 million |
| 1980 |  Star Wars: Episode V – The *Empire* **Strikes** ~~Back~~  | Irvin Kershner    |    $538.4 million |
"""
    )
    result = render(markdown)
    expected = "\n                                                                                                 \n \x1b[1m \x1b[0m\x1b[1mYear\x1b[0m\x1b[1m \x1b[0m \x1b[1m \x1b[0m\x1b[1mThis \x1b[0m\x1b[1mcolumn\x1b[0m\x1b[1m displays \x1b[0m\x1b[1;3mthe\x1b[0m\x1b[1m movie \x1b[0m\x1b[1;3mtitle\x1b[0m\x1b[1m \x1b[0m\x1b[1;9mdescription\x1b[0m\x1b[1m \x1b[0m \x1b[1m \x1b[0m\x1b[1mDirector        \x1b[0m\x1b[1m \x1b[0m \x1b[1m \x1b[0m\x1b[1mBox Office (USD)\x1b[0m\x1b[1m \x1b[0m \n ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ \n  1982    \x1b[3mE.T. the Extra-Terrestrial\x1b[0m (\x1b]8;id=0;foo\x1b\\\x1b[4;34mWikipedia article\x1b[0m\x1b]8;;\x1b\\)    Steven Spielberg     $792.9 million  \n  1980    Star Wars: Episode V – The \x1b[3mEmpire\x1b[0m \x1b[1mStrikes\x1b[0m \x1b[9mBack\x1b[0m    Irvin Kershner       $538.4 million  \n                                                                                                 \n"
    assert result == expected


def test_inline_styles_with_justification():
    """Regression test for https://github.com/Textualize/rich/issues/3115

    In particular, this tests the interaction between the change that was made to fix
    #3115 and column text justification.
    """
    markdown = Markdown(
        """\
| left | center | right |
| :- | :-: | -: |
| This is a long row | because it contains | a fairly long sentence. |
| a*b* _c_ ~~d~~ e | a*b* _c_ ~~d~~ e | a*b* _c_ ~~d~~ e |"""
    )
    result = render(markdown)
    expected = "\n                                                                      \n \x1b[1m \x1b[0m\x1b[1mleft              \x1b[0m\x1b[1m \x1b[0m \x1b[1m \x1b[0m\x1b[1m      center       \x1b[0m\x1b[1m \x1b[0m \x1b[1m \x1b[0m\x1b[1m                  right\x1b[0m\x1b[1m \x1b[0m \n ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ \n  This is a long row   because it contains   a fairly long sentence.  \n  a\x1b[3mb\x1b[0m \x1b[3mc\x1b[0m \x1b[9md\x1b[0m e                  a\x1b[3mb\x1b[0m \x1b[3mc\x1b[0m \x1b[9md\x1b[0m e                        a\x1b[3mb\x1b[0m \x1b[3mc\x1b[0m \x1b[9md\x1b[0m e  \n                                                                      \n"
    assert result == expected


def test_partial_table():
    markdown = Markdown("| Simple | Table |\n| ------ | ----- ")
    result = render(markdown)
    print(repr(result))
    expected = "\n                  \n \x1b[1m \x1b[0m\x1b[1mSimple\x1b[0m\x1b[1m \x1b[0m \x1b[1m \x1b[0m\x1b[1mTable\x1b[0m\x1b[1m \x1b[0m \n ━━━━━━━━━━━━━━━━ \n                  \n"
    assert result == expected


if __name__ == "__main__":
    markdown = Markdown(MARKDOWN)
    rendered = render(markdown)
    print(rendered)
    print(repr(rendered))
