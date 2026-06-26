[![Supported Python Versions](https://img.shields.io/pypi/pyversions/rich)](https://pypi.org/project/rich/) [![PyPI version](https://badge.fury.io/py/rich.svg)](https://badge.fury.io/py/rich)

[![Downloads](https://pepy.tech/badge/rich/month)](https://pepy.tech/project/rich)
[![codecov](https://img.shields.io/codecov/c/github/Textualize/rich?label=codecov&logo=codecov)](https://codecov.io/gh/Textualize/rich)
[![Rich blog](https://img.shields.io/badge/blog-rich%20news-yellowgreen)](https://www.willmcgugan.com/tag/rich/)
[![Twitter Follow](https://img.shields.io/twitter/follow/willmcgugan.svg?style=social)](https://twitter.com/willmcgugan)

![Logo](https://github.com/textualize/rich/raw/main/imgs/logo.svg)

[English readme](https://github.com/textualize/rich/blob/main/README.md)
 • [简体中文 readme](https://github.com/textualize/rich/blob/main/README.cn.md)
 • [正體中文 readme](https://github.com/textualize/rich/blob/main/README.zh-tw.md)
 • [Lengua española readme](https://github.com/textualize/rich/blob/main/README.es.md)
 • [Deutsche readme](https://github.com/textualize/rich/blob/main/README.de.md)
 • [Läs på svenska](https://github.com/textualize/rich/blob/main/README.sv.md)
 • [日本語 readme](https://github.com/textualize/rich/blob/main/README.ja.md)
 • [한국어 readme](https://github.com/textualize/rich/blob/main/README.kr.md)
 • [Français readme](https://github.com/textualize/rich/blob/main/README.fr.md)
 • [Schwizerdütsch readme](https://github.com/textualize/rich/blob/main/README.de-ch.md)
 • [हिन्दी readme](https://github.com/textualize/rich/blob/main/README.hi.md)
 • [Português brasileiro readme](https://github.com/textualize/rich/blob/main/README.pt-br.md)
 • [Italian readme](https://github.com/textualize/rich/blob/main/README.it.md)
 • [Русский readme](https://github.com/textualize/rich/blob/main/README.ru.md)
  • [فارسی readme](https://github.com/textualize/rich/blob/main/README.fa.md)
 • [Türkçe readme](https://github.com/textualize/rich/blob/main/README.tr.md)
 • [Polskie readme](https://github.com/textualize/rich/blob/main/README.pl.md)

Richは、 _リッチ_ なテキストや美しい書式設定をターミナルで行うためのPythonライブラリです。

[Rich API](https://rich.readthedocs.io/en/latest/)を使用すると、ターミナルの出力に色やスタイルを簡単に追加することができます。 Richはきれいなテーブル、プログレスバー、マークダウン、シンタックスハイライトされたソースコード、トレースバックなどをすぐに生成・表示することもできます。

![機能](https://github.com/textualize/rich/raw/main/imgs/features.png)

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

![Hello World](https://github.com/textualize/rich/raw/main/imgs/print.png)

## Rich REPL

RichはPythonのREPLでインストールすることができ、データ構造がきれいに表示され、ハイライトされます。

```python
>>> from rich import pretty
>>> pretty.install()
```

![REPL](https://github.com/textualize/rich/raw/main/imgs/repl.png)

## Rich Inspect

RichにはPythonオブジェクトやクラス、インスタンス、組み込み関数などに関するレポートを作成することができる、[inspect関数](https://rich.readthedocs.io/en/latest/reference/init.html?highlight=inspect#rich.inspect)があります。

```python
>>> from rich import inspect
>>> inspect(str, methods=True)
```

## Consoleの使い方

リッチなターミナルコンテンツをより制御していくには、[Console](https://rich.readthedocs.io/en/latest/reference/console.html#rich.console.Console) オブジェクトをインポートして構築していきます。


```python
from rich.console import Console

console = Console()
```

Console オブジェクトには `print` メソッドがあり、これは組み込み関数の `print` と意図的に似たインターフェイスを持っています。
以下に使用例を示します:

```python
console.print("Hello", "World!")
```

あなたが予想した通り、これは `"Hello World!"` をターミナルに表示します。組み込み関数の `print` とは異なり、Rich はターミナルの幅に合わせてテキストをワードラップすることに注意してください。

出力結果に色やスタイルを追加する方法はいくつかあります。キーワード引数に `style` を追加することで、出力結果全体のスタイルを設定することができます。以下に例を示します:

```python
console.print("Hello", "World!", style="bold red")
```

以下のように出力されます:

![Hello World](https://github.com/textualize/rich/raw/main/imgs/hello_world.png)

この方法は一行のテキストを一度にスタイリングするのに適しています。
より細かくスタイリングを行うために、Richは[bbcode](https://en.wikipedia.org/wiki/BBCode)に似た構文の特別なマークアップを表示することができます。
これはその例です:

```python
console.print("Where there is a [bold cyan]Will[/bold cyan] there [u]is[/u] a [i]way[/i].")
```

![Console Markup](https://github.com/textualize/rich/raw/main/imgs/where_there_is_a_will.png)

### Console logging

Consoleオブジェクトには `log()` メソッドがあり、これは `print()` と同じインターフェイスを持ちますが、現在の時刻と呼び出しを行ったファイルと行数についてもカラムに表示します。デフォルトでは、RichはPythonの構造体とrepr文字列のシンタックスハイライトを行います。もしコレクション(例: dictやlist)をログに記録した場合、Richはそれを利用可能なスペースに収まるようにきれいに表示します。以下に、これらの機能のいくつかの例を示します。

```python
from rich.console import Console
console = Console()

test_data = [
    {"jsonrpc": "2.0", "method": "sum", "params": [None, 1, 2, 4, False, True], "id": "1",},
    {"jsonrpc": "2.0", "method": "notify_hello", "params": [7]},
    {"jsonrpc": "2.0", "method": "subtract", "params": [42, 23], "id": "2"},
]

def test_log():
    enabled = False
    context = {
        "foo": "bar",
    }
    movies = ["Deadpool", "Rise of the Skywalker"]
    console.log("Hello from", console, "!")
    console.log(test_data, log_locals=True)


test_log()
```

上の例では以下のような出力が得られます:

![Log](https://github.com/textualize/rich/raw/main/imgs/log.png)

`log_locals`という引数についてですが、これは、logメソッドが呼び出されたローカル変数を含むテーブルを出力します。

logメソッドはサーバのような長時間稼働しているアプリケーションのターミナルへのloggingとして使用できますが、デバッグ時に非常に役に立つ手段でもあります。

### Logging Handler

また、内蔵されている[Handler class](https://rich.readthedocs.io/en/latest/logging.html)を用いて、Pythonのloggingモジュールからの出力をフォーマットしたり、色付けしたりすることもできます。以下に出力の例を示します。

![Logging](https://github.com/textualize/rich/raw/main/imgs/logging.png)

## 絵文字(Emoji)

コンソールの出力に絵文字を挿入するには、2つのコロンの間に名前を入れます。例を示します:

```python
>>> console.print(":smiley: :vampire: :pile_of_poo: :thumbs_up: :raccoon:")
😃 🧛 💩 👍 🦝
```

この機能をうまく活用してみてください。

## テーブル

Richはユニコードの枠を用いて柔軟に[テーブル](https://rich.readthedocs.io/en/latest/tables.html)を表示することができます。 罫線、スタイル、セルの配置などの書式設定のためのオプションが豊富にあります。

![table movie](https://github.com/textualize/rich/raw/main/imgs/table_movie.gif)

上のアニメーションは、examplesディレクトリの[table_movie.py](https://github.com/textualize/rich/blob/main/examples/table_movie.py)で生成したものです。

もう少し簡単な表の例を示します:

```python
from rich.console import Console
from rich.table import Table

console = Console()

table = Table(show_header=True, header_style="bold magenta")
table.add_column("Date", style="dim", width=12)
table.add_column("Title")
table.add_column("Production Budget", justify="right")
table.add_column("Box Office", justify="right")
table.add_row(
    "Dec 20, 2019", "Star Wars: The Rise of Skywalker", "$275,000,000", "$375,126,118"
)
table.add_row(
    "May 25, 2018",
    "[red]Solo[/red]: A Star Wars Story",
    "$275,000,000",
    "$393,151,347",
)
table.add_row(
    "Dec 15, 2017",
    "Star Wars Ep. VIII: The Last Jedi",
    "$262,000,000",
    "[bold]$1,332,539,889[/bold]",
)

console.print(table)
```

これにより、以下のような出力が得られます:

![table](https://github.com/textualize/rich/raw/main/imgs/table.png)

コンソール上でのマークアップは`print()` や `log()` と同じように表示されることに注意してください。実際には、Rich が表示可能なものはすべてヘッダや行に含めることができます (それが他のテーブルであっても、です)。

`Table`クラスは、ターミナルの利用可能な幅に合わせてカラムのサイズを変更したり、必要に応じてテキストを折り返したりするのに十分なスマートさを持っています。
これは先ほどと同じ例で、ターミナルを上のテーブルよりも小さくしたものです。

![table2](https://github.com/textualize/rich/raw/main/imgs/table2.png)

## プログレスバー

Richでは複数のちらつきのないの[プログレスバー](https://rich.readthedocs.io/en/latest/progress.html)を表示して、長時間のタスクを追跡することができます。

基本的な使い方としては、任意のシーケンスを `track` 関数でラップし、その結果を繰り返し処理します。以下に例を示します:

```python
from rich.progress import track

for step in track(range(100)):
    do_step(step)
```

複数のプログレスバーを追加するのはそれほど大変ではありません。以下はドキュメントから抜粋した例です:

![progress](https://github.com/textualize/rich/raw/main/imgs/progress.gif)

カラムには任意の詳細を表示するように設定することができます。組み込まれているカラムには、完了率、ファイルサイズ、ファイル速度、残り時間が含まれています。ここでは、進行中のダウンロードを表示する別の例を示します:

![progress](https://github.com/textualize/rich/raw/main/imgs/downloader.gif)

こちらを自分で試して見るには、進捗状況を表示しながら複数のURLを同時にダウンロードできる [examples/downloader.py](https://github.com/textualize/rich/blob/main/examples/downloader.py) を参照してみてください。

## ステータス

進捗状況を計算するのが難しい場合は、[status](https://rich.readthedocs.io/en/latest/reference/console.html#rich.console.Console.status)メソッドを使用して、「スピナー」アニメーションとメッセージを表示させることができます。通常、アニメーションはコンソールの使用を妨げることはありません。ここに例を示します:

```python
from time import sleep
from rich.console import Console

console = Console()
tasks = [f"task {n}" for n in range(1, 11)]

with console.status("[bold green]Working on tasks...") as status:
    while tasks:
        task = tasks.pop(0)
        sleep(1)
        console.log(f"{task} complete")
```

これにより、ターミナルには以下のような出力が生成されます。

![status](https://github.com/textualize/rich/raw/main/imgs/status.gif)

スピナーのアニメーションは [cli-spinners](https://www.npmjs.com/package/cli-spinners) から拝借しました。`spinner`パラメータを指定することでスピナーを選択することができます。以下のコマンドを実行して、利用可能な値を確認してください:

```
python -m rich.spinner
```

上記コマンドは、ターミナルで以下のような出力を生成します:

![spinners](https://github.com/textualize/rich/raw/main/imgs/spinners.gif)

## ツリー

Richはガイドライン付きの[ツリー](https://rich.readthedocs.io/en/latest/tree.html)を表示することができます。ツリーはファイル構造などの階層データを表示するのに適しています。

ツリーのラベルは、シンプルなテキストや、Richが表示できるものであれば何でも表示することができます。以下を実行してデモを行います:

```
python -m rich.tree
```

これにより、次のような出力が生成されます:

![markdown](https://github.com/textualize/rich/raw/main/imgs/tree.png)

linuxの `tree` コマンドと同様に、任意のディレクトリのツリー表示を行うスクリプトについては、[tree.py](https://github.com/textualize/rich/blob/main/examples/tree.py)の例を参照してください。

## カラム

Rich は、コンテンツをきれいな [カラム](https://rich.readthedocs.io/en/latest/columns.html) で等幅、または最適な幅で表示することができます。これは(MacOS / Linux) の `ls` コマンドのとても基本的なクローンで、ディレクトリ一覧をカラムで表示します。

```python
import os
import sys

from rich import print
from rich.columns import Columns

directory = os.listdir(sys.argv[1])
print(Columns(directory))
```

以下のスクリーンショットは、APIから引っ張ってきたデータをカラムで表示する[columns example](https://github.com/textualize/rich/blob/main/examples/columns.py)による出力です:

![columns](https://github.com/textualize/rich/raw/main/imgs/columns.png)

## マークダウン

Richは[マークダウン](https://rich.readthedocs.io/en/latest/markdown.html)を使用することができ、フォーマットをターミナル向けに変換するための良い仕事をしてくれます。

マークダウンを使用するには、`Markdown`クラスをインポートし、マークダウンコードを含む文字列で構成します。そしてそれをコンソールに表示します。これは例です:

```python
from rich.console import Console
from rich.markdown import Markdown

console = Console()
with open("README.md") as readme:
    markdown = Markdown(readme.read())
console.print(markdown)
```

これにより、以下のような出力が得られます:

![markdown](https://github.com/textualize/rich/raw/main/imgs/markdown.png)

## シンタックスハイライト

Richは [シンタックスハイライト](https://rich.readthedocs.io/en/latest/syntax.html) を実装するために [pygments](https://pygments.org/) ライブラリを使用しています。使い方はマークダウンを使用するのと似ています。 `Syntax` オブジェクトを構築してコンソールに表示します。以下にその例を示します:

```python
from rich.console import Console
from rich.syntax import Syntax

my_code = '''
def iter_first_last(values: Iterable[T]) -> Iterable[Tuple[bool, bool, T]]:
    """Iterate and generate a tuple with a flag for first and last value."""
    iter_values = iter(values)
    try:
        previous_value = next(iter_values)
    except StopIteration:
        return
    first = True
    for value in iter_values:
        yield first, False, previous_value
        first = False
        previous_value = value
    yield first, True, previous_value
'''
syntax = Syntax(my_code, "python", theme="monokai", line_numbers=True)
console = Console()
console.print(syntax)
```

これにより、以下のような出力が得られます:

![syntax](https://github.com/textualize/rich/raw/main/imgs/syntax.png)

## トレースバック

Rich は [美しいトレースバック](https://rich.readthedocs.io/en/latest/traceback.html) を表示することができ、通常のPythonのトレースバックよりも読みやすく、より多くのコードを表示することができます。Richをデフォルトのトレースバックハンドラとして設定することで、捕捉されなかった例外はすべてRichによって表示されるようになります。

OSXではこのような表示となります（Linuxでも似たような表示になります）:

![traceback](https://github.com/textualize/rich/raw/main/imgs/traceback.png)

## Richを使用したプロジェクト

ここでは、Richを使用したいくつかのプロジェクトを紹介します:

- [BrancoLab/BrainRender](https://github.com/BrancoLab/BrainRender)
  3次元の神経解剖学的データを可視化するpythonパッケージ
- [Ciphey/Ciphey](https://github.com/Ciphey/Ciphey)
  自動化された復号化ツール
- [emeryberger/scalene](https://github.com/emeryberger/scalene)
  Python用の高性能・高精度 CPU/メモリプロファイラ
- [hedythedev/StarCli](https://github.com/hedythedev/starcli)
  コマンドラインから GitHub のトレンドプロジェクトを閲覧できます
- [intel/cve-bin-tool](https://github.com/intel/cve-bin-tool)
  このツールは、一般的な脆弱性のあるコンポーネント(openssl, libpng, libxml2, expat, その他いくつか)をスキャンし、お使いのシステムに既知の脆弱性のある一般的なライブラリが含まれているかどうかを知らせてくれます。
- [nf-core/tools](https://github.com/nf-core/tools)
  nf-core コミュニティのためのヘルパーツールを含む Python パッケージ。
- [cansarigol/pdbr](https://github.com/cansarigol/pdbr)
  pdb + Richライブラリによる、強化されたデバッグツール。
- [plant99/felicette](https://github.com/plant99/felicette)
  ダミーのための衛星画像。
- [seleniumbase/SeleniumBase](https://github.com/seleniumbase/SeleniumBase)
  Seleniumとpytestで10倍速の自動化とテスト。バッテリーも含まれています。
- [smacke/ffsubsync](https://github.com/smacke/ffsubsync)
  字幕を自動的にビデオと同期させます。
- [tryolabs/norfair](https://github.com/tryolabs/norfair)
  あらゆる検出器にリアルタイムの2Dオブジェクトトラッキングを追加するための軽量なPythonライブラリ。
- [ansible/ansible-lint](https://github.com/ansible/ansible-lint)
  Ansible-lint がplaybooksをチェックして、改善できる可能性のあるプラクティスや動作を確認します。
- [ansible-community/molecule](https://github.com/ansible-community/molecule)
  Ansible Moleculeのテストフレームワーク
- +[Many more](https://github.com/textualize/rich/network/dependents)!
