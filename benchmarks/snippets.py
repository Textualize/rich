PYTHON_SNIPPET = '''
def layout_resolve(total: int, edges: Sequence[EdgeProtocol]) -> List[int]:
    """Divide total space to satisfy size, fraction, and min_size, constraints.

    The returned list of integers should add up to total in most cases, unless it is
    impossible to satisfy all the constraints. For instance, if there are two edges
    with a minimum size of 20 each and `total` is 30 then the returned list will be
    greater than total. In practice, this would mean that a Layout object would
    clip the rows that would overflow the screen height.

    Args:
        total (int): Total number of characters.
        edges (Sequence[Edge]): Edges within total space.

    Returns:
        list[int]: Number of characters for each edge.
    """
    # Size of edge or None for yet to be determined
    sizes = [(edge.size or None) for edge in edges]

    if None not in sizes:
        # No flexible edges
        return cast("list[int]", sizes)

    # Get flexible edges and index to map these back on to sizes list
    flexible_edges = [
        (index, edge)
        for index, (size, edge) in enumerate(zip(sizes, edges))
        if size is None
    ]
    # Remaining space in total
    remaining = total - sum([size or 0 for size in sizes])
    if remaining <= 0:
        # No room for flexible edges
        return [
            ((edge.min_size or 1) if size is None else size)
            for size, edge in zip(sizes, edges)
        ]

    # Get the total fraction value for all flexible edges
    total_flexible = sum([(edge.fraction or 1) for _, edge in flexible_edges])
    while flexible_edges:
        # Calculate number of characters in a ratio portion
        portion = Fraction(remaining, total_flexible)

        # If any edges will be less than their minimum, replace size with the minimum
        for flexible_index, (index, edge) in enumerate(flexible_edges):
            if portion * edge.fraction < edge.min_size:
                # This flexible edge will be smaller than its minimum size
                # We need to fix the size and redistribute the outstanding space
                sizes[index] = edge.min_size
                remaining -= edge.min_size
                total_flexible -= edge.fraction or 1
                del flexible_edges[flexible_index]
                # New fixed size will invalidate calculations, so we need to repeat the process
                break
        else:
            # Distribute flexible space and compensate for rounding error
            # Since edge sizes can only be integers we need to add the remainder
            # to the following line
            remainder = Fraction(0)
            for index, edge in flexible_edges:
                sizes[index], remainder = divmod(portion * edge.fraction + remainder, 1)
            break

    # Sizes now contains integers only
    return cast("list[int]", sizes)
'''

PYTHON_DICT = {
    "glossary": {
        "title": "example glossary",
        "GlossDiv": {
            "title": "S",
            "GlossList": {
                "GlossEntry": {
                    "ID": "SGML",
                    "SortAs": "SGML",
                    "GlossTerm": "Standard Generalized Markup Language",
                    "Acronym": "SGML",
                    "Abbrev": "ISO 8879:1986",
                    "GlossDef": {
                        "para": "A meta-markup language, used to create markup languages such as DocBook.",
                        "GlossSeeAlso": ["GML", "XML"],
                    },
                    "GlossSee": "markup",
                }
            },
        },
    }
}

LOREM_IPSUM = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Laoreet id donec ultrices tincidunt arcu. Eu facilisis sed odio morbi quis commodo odio aenean sed. Amet cursus sit amet dictum. Gravida rutrum quisque non tellus. Semper auctor neque vitae tempus quam pellentesque nec nam. Mauris sit amet massa vitae tortor condimentum lacinia quis. Adipiscing elit ut aliquam purus sit amet luctus venenatis lectus. Consectetur adipiscing elit ut aliquam purus sit amet. Sit amet mauris commodo quis imperdiet massa tincidunt nunc pulvinar. Dui faucibus in ornare quam viverra. Et netus et malesuada fames ac turpis. A lacus vestibulum sed arcu non odio euismod. In massa tempor nec feugiat nisl pretium fusce.

Tellus in hac habitasse platea dictumst vestibulum. Feugiat nibh sed pulvinar proin. In cursus turpis massa tincidunt dui ut. Fermentum posuere urna nec tincidunt praesent semper feugiat. Interdum consectetur libero id faucibus. Habitant morbi tristique senectus et netus et malesuada fames ac. Facilisis leo vel fringilla est ullamcorper eget nulla facilisi. Aliquam faucibus purus in massa tempor. Tellus pellentesque eu tincidunt tortor aliquam nulla. Sem et tortor consequat id porta nibh. Massa id neque aliquam vestibulum morbi blandit cursus risus. Ut placerat orci nulla pellentesque dignissim enim. Nibh tellus molestie nunc non blandit massa enim nec dui. Ipsum a arcu cursus vitae congue mauris rhoncus aenean vel. Egestas congue quisque egestas diam in.

Pulvinar mattis nunc sed blandit libero volutpat sed. Accumsan in nisl nisi scelerisque eu. Eget aliquet nibh praesent tristique. Ipsum suspendisse ultrices gravida dictum fusce ut. Non sodales neque sodales ut etiam sit amet. Velit egestas dui id ornare. Massa ultricies mi quis hendrerit dolor magna. Id volutpat lacus laoreet non curabitur gravida arcu. Nulla facilisi cras fermentum odio eu feugiat pretium. Sed vulputate odio ut enim blandit volutpat. Amet massa vitae tortor condimentum lacinia. Tellus integer feugiat scelerisque varius. Quam nulla porttitor massa id. Facilisi cras fermentum odio eu feugiat pretium nibh ipsum. Eget nunc scelerisque viverra mauris in aliquam sem fringilla. Amet nulla facilisi morbi tempus iaculis urna id volutpat lacus. Facilisi etiam dignissim diam quis enim lobortis.

Nullam vehicula ipsum a arcu cursus vitae congue mauris rhoncus. Ullamcorper a lacus vestibulum sed arcu non. Suscipit adipiscing bibendum est ultricies integer quis auctor elit. Integer feugiat scelerisque varius morbi enim. Posuere urna nec tincidunt praesent semper feugiat nibh sed pulvinar. Lobortis feugiat vivamus at augue eget. Rhoncus dolor purus non enim praesent. Mi in nulla posuere sollicitudin aliquam ultrices sagittis orci. Mollis aliquam ut porttitor leo. Id cursus metus aliquam eleifend mi in nulla. Integer eget aliquet nibh praesent tristique magna sit amet. Egestas maecenas pharetra convallis posuere morbi.

Blandit massa enim nec dui. Suscipit tellus mauris a diam maecenas. Sed id semper risus in. Purus faucibus ornare suspendisse sed nisi lacus. At in tellus integer feugiat. Egestas diam in arcu cursus euismod quis viverra nibh cras. Enim tortor at auctor urna nunc id. Tristique nulla aliquet enim tortor at auctor urna nunc id. Purus gravida quis blandit turpis cursus in hac habitasse platea. Ac turpis egestas integer eget. Tortor at auctor urna nunc. Neque aliquam vestibulum morbi blandit cursus. Massa tempor nec feugiat nisl pretium fusce id velit. Interdum consectetur libero id faucibus nisl tincidunt. Adipiscing diam donec adipiscing tristique risus nec feugiat in. Egestas integer eget aliquet nibh praesent tristique magna sit.
"""

UNICODE_HEAVY_TEXT = """
Richは、 _リッチ_ なテキストや美しい書式設定をターミナルで行うためのPythonライブラリです。

[Rich API](https://rich.readthedocs.io/en/latest/)を使用すると、ターミナルの出力に色やスタイルを簡単に追加することができます。 Richはきれいなテーブル、プログレスバー、マークダウン、シンタックスハイライトされたソースコード、トレースバックなどをすぐに生成・表示することもできます。

![機能](https://github.com/textualize/rich/raw/master/imgs/features.png)

Richの紹介動画はこちらをご覧ください。 [calmcode.io](https://calmcode.io/rich/introduction.html) by [@fishnets88](https://twitter.com/fishnets88).

[Richについての人々の感想を見る。](https://www.willmcgugan.com/blog/pages/post/rich-tweets/)

## 互換性

RichはLinux、OSX、Windowsに対応しています。True colorと絵文字は新しい Windows ターミナルで動作しますが、古いターミナルでは8色に制限されています。Richを使用するにはPythonのバージョンは3.6.3以降が必要です。

Richは追加の設定を行わずとも、[Jupyter notebooks](https://jupyter.org/)で動作します。

## インストール

`pip` や、あなたのお気に入りのPyPIパッケージマネージャを使ってインストールしてください。

```sh
python -m pip install rich
```

以下のコマンドを実行して、ターミナルでリッチの出力をテストできます:

```sh
python -m rich
```

## Richのprint関数

簡単にリッチな出力をアプリケーションに追加するには、Pythonの組み込み関数と同じ名前を持つ [rich print](https://rich.readthedocs.io/en/latest/introduction.html#quick-start) メソッドをインポートすることで実現できます。こちらを試してみてください:

```python
from rich import print

print("Hello, [bold magenta]World[/bold magenta]!", ":vampire:", locals())
```

![Hello World](https://github.com/textualize/rich/raw/master/imgs/print.png)

## Rich REPL

RichはPythonのREPLでインストールすることができ、データ構造がきれいに表示され、ハイライトされます。

```python
>>> from rich import pretty
>>> pretty.install()
```

![REPL](https://github.com/textualize/rich/raw/master/imgs/repl.png)

## Rich Inspect

RichにはPythonオブジェクトやクラス、インスタンス、組み込み関数などに関するレポートを作成することができる、[inspect関数](https://rich.readthedocs.io/en/latest/reference/init.html?highlight=inspect#rich.inspect)があります。

の使い方

リッチなターミナルコンテンツをより制御していくには、[Console](https://rich.readthedocs.io/en/latest/reference/console.html#rich.console.Console) オブジェクトをインポートして構築していきます。

Console オブジェクトには `print` メソッドがあり、これは組み込み関数の `print` と意図的に似たインターフェイスを持っています。
以下に使用例を示します:

あなたが予想した通り、これは `"Hello World!"` をターミナルに表示します。組み込み関数の `print` とは異なり、Rich はターミナルの幅に合わせてテキストをワードラップすることに注意してください。

出力結果に色やスタイルを追加する方法はいくつかあります。キーワード引数に `style` を追加することで、出力結果全体のスタイルを設定することができます。以下に例を示します:
"""


MARKUP = "\n".join(
    """[bold]Hello [i]World[/i] [bold magenta]foo [i]bar[/i] baz[/] [blue u]https://textualize.io[/]"""
    for _ in range(20)
)
