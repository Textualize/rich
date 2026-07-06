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

Rich는 터미널에서 _풍부한(rich)_ 텍스트와 아름다운 서식을 지원하기 위한 파이썬 라이브러리입니다.

[Rich API](https://rich.readthedocs.io/en/latest/)는 터미널 출력에 색깔과 스타일을 입히기 쉽게 도와줍니다. 또한 Rich는 별다른 설정 없이 표, 진행 바, 마크다운, 소스코드 구문 강조, tracebacks 등을 예쁘게 보여줄 수 있습니다.

![Features](https://github.com/textualize/rich/raw/main/imgs/features.png)

Rich에 대한 동영상 설명을 보시려면 [@fishnets88](https://twitter.com/fishnets88)의 [calmcode.io](https://calmcode.io/rich/introduction.html)를 확인 바랍니다.

[사람들의 Rich에 대한 의견](https://www.willmcgugan.com/blog/pages/post/rich-tweets/)을 확인해보세요.

## 호환성

Rich는 리눅스, OSX, 윈도우에서 동작합니다. 트루 컬러 / 이모지는 새로운 윈도우 터미널에서 동작하지만 구형 터미널에서는 16가지 색으로 제한됩니다. Rich는 파이썬 3.6.3 버전 혹은 그 이후 버전이 필요합니다.

Rich는 [Jupyter notebooks](https://jupyter.org/)에서 별도의 설정없이 바로 동작합니다.

## 설치

`pip` 또는 좋아하는 PyPI 패키지 매니저로 설치하세요.

```sh
python -m pip install rich
```

아래 명령어를 통해 터미널에서 Rich 출력을 테스트해보세요.

```sh
python -m rich
```

## Rich Print

간단하게 당신의 어플리케이션에 rich한 출력을 추가하려면, 파이썬 내장 함수와 signature가 같은 [rich print](https://rich.readthedocs.io/en/latest/introduction.html#quick-start) 메서드를 import 할 수 있습니다.
따라해보세요:

```python
from rich import print

print("Hello, [bold magenta]World[/bold magenta]!", ":vampire:", locals())
```

![Hello World](https://github.com/textualize/rich/raw/main/imgs/print.png)

## Rich REPL

Rich는 파이썬 REPL에도 설치할 수 있습니다. 어떤 데이터 구조라도 예쁘게 출력하거나 강조할 수 있습니다.

```python
>>> from rich import pretty
>>> pretty.install()
```

![REPL](https://github.com/textualize/rich/raw/main/imgs/repl.png)

## 콘솔 사용하기

rich 터미널을 더욱 잘 활용하려면, import 한 뒤 [Console](https://rich.readthedocs.io/en/latest/reference/console.html#rich.console.Console) 객체를 생성해주세요.

```python
from rich.console import Console

console = Console()
```

콘솔 객체에는 `print` 메서드가 있는데, 내부적으로 내장 `print` 함수와 유사한 인터페이스를 가지고 있습니다. 아래는 예제입니다:

```python
console.print("Hello", "World!")
```

예상대로 `"Hello World!"`이 터미널에 출력될 것입니다. 내장 `print` 함수와 달리, Rich는 터미널 폭에 맞춰 자동 줄바꿈(word-wrap)을 적용하는 것에 유의하세요.

출력에 색깔과 스타일을 입히는 방법은 몇가지가 있습니다. `style` 키워드 전달인자를 추가해 전체 출력에 대해 스타일을 변경할 수 있습니다. 예제는 다음과 같습니다:

```python
console.print("Hello", "World!", style="bold red")
```

다음과 같이 출력됩니다:

![Hello World](https://github.com/textualize/rich/raw/main/imgs/hello_world.png)

텍스트 한 줄을 한 번에 수정하는 것도 좋습니다. 더욱 세세하게 스타일을 변경하기 위해, Rich는 [bbcode](https://en.wikipedia.org/wiki/BBCode)와 구문이 비슷한 별도의 마크업을 렌더링 할 수 있습니다. 예제는 다음과 같습니다.

```python
console.print("Where there is a [bold cyan]Will[/bold cyan] there [u]is[/u] a [i]way[/i].")
```

![Console Markup](https://github.com/textualize/rich/raw/main/imgs/where_there_is_a_will.png)

Console 객체를 활용해 적은 노력으로 복잡한 출력을 손쉽게 만들 수 있습니다. 자세한 내용은 [Console API](https://rich.readthedocs.io/en/latest/console.html) 문서를 확인해주세요.

## Rich Inspect

Rich는 class나 instance, builtin 같은 파이썬 객체의 레포트를 생성하는 [inspect](https://rich.readthedocs.io/en/latest/reference/init.html?highlight=inspect#rich.inspect) 함수를 포함합니다

```python
>>> my_list = ["foo", "bar"]
>>> from rich import inspect
>>> inspect(my_list, methods=True)
```

![Log](https://github.com/textualize/rich/raw/main/imgs/inspect.png)

자세한 내용은 [inspect docs](https://rich.readthedocs.io/en/latest/reference/init.html#rich.inspect) 문서를 확인해주세요.

# Rich Library

Rich는 CLI에서 우아하게 출력하거나 코드 디버깅을 돕도록 다양한 빌트인 _렌더링을_ 포함하고 있습니다.

자세한 내용을 확인하려면 제목을 눌러주세요:

<details>
<summary>Log</summary>

Console 객체는 `print()`와 인터페이스가 유사한 `log()` 메서드를 가지고 있습니다. `Log()`는 호출이 이루어진 파일과 라인, 현재 시간도 같이 출력합니다. 기본적으로 Rich는 파이썬 구조체와 repr string에 대해 신택스 하이라이팅을 지원합니다. 만약 당신이 collection(예를 들어 dict나 list)을 로깅한다면, Rich는 표현 가능한 공간에 맞춰 예쁘게 출력해줍니다. 이러한 기능들에 대한 예시입니다:

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

위 코드의 실행 결과는 다음과 같습니다:

![Log](https://github.com/textualize/rich/raw/main/imgs/log.png)

`log_locals` 인자를 사용하면 log 메서드가 호출된 곳의 로컬 변수들을 표로 보여준다는 것도 알아두세요.

로그 메서드는 서버처럼 오랫동안 실행되는 어플리케이션을 터미널로 로깅할때 사용할 수 있지만 디버깅 할 때도 매우 좋습니다.

</details>
<details>
<summary>Logging Handler</summary>

또한 내장된 [Handler class](https://rich.readthedocs.io/en/latest/logging.html)를 사용해 파이썬의 로깅 모듈의 출력을 형태를 꾸미거나 색을 입힐 수 있습니다. 다음은 예제입니다:

![Logging](https://github.com/textualize/rich/raw/main/imgs/logging.png)

</details>

<details>
<summary>Emoji(이모지)</summary>

콘솔 출력에 이모지를 넣으려면 두 콜론(:) 사이에 이모지 이름을 넣어주세요. 다음은 예제입니다:

```python
>>> console.print(":smiley: :vampire: :pile_of_poo: :thumbs_up: :raccoon:")
😃 🧛 💩 👍 🦝
```

부디 이 기능을 잘 사용해주세요.

</details>

<details>
<summary>Tables(표)</summary>

Rich는 유니코드 박스 문자와 함께 [표](https://rich.readthedocs.io/en/latest/tables.html)를 자유롭게 렌더링할 수 있습니다. 가장자리, 스타일, 셀 정렬 등을 정말 다양하게 구성할 수 있습니다.

![table movie](https://github.com/textualize/rich/raw/main/imgs/table_movie.gif)

위의 애니메이션은 example 디렉토리의 [table_movie.py](https://github.com/textualize/rich/blob/main/examples/table_movie.py)로 생성되었습니다.

더 간단한 표 예제입니다:

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

이는 다음과 같이 출력됩니다:

![table](https://github.com/textualize/rich/raw/main/imgs/table.png)

콘솔 출력은 `print()`나 `log()`와 같은 방식으로 렌더링 된다는 것을 주의하세요. 사실, Rich로 표현할 수 있는 것은 무엇이든 headers / rows (심지어 다른 표들도)에 포함할 수 있습니다.

`Table` 클래스는 터미널의 폭에 맞춰 필요한 만큼 줄을 내리고 열 길이를 스스로 조절합니다. 위의 표보다 작은 터미널에서 만들어진 표 예시입니다:

![table2](https://github.com/textualize/rich/raw/main/imgs/table2.png)

</details>

<details>
<summary>Progress Bars(진행 바)</summary>

Rich는 오래 걸리는 작업들을 위해 깜빡임 없는 [진행](https://rich.readthedocs.io/en/latest/progress.html) 바를 여러개 표현할 수 있습니다.

기본적인 사용을 위해선 아무 sequence나 `track` 함수로 감싸고 결과를 반복해주세요. 다음은 예제입니다:

```python
from rich.progress import track

for step in track(range(100)):
    do_step(step)
```

여러개의 진행 바를 추가하는 것도 어렵지 않습니다. 아래는 공식문서에서 따온 예시입니다:

![progress](https://github.com/textualize/rich/raw/main/imgs/progress.gif)

칼럼들은 수정해 원하는 세부정보를 보여줄 수도 있습니다. 기본으로 내장된 칼럼들은 완료 퍼센티지, 파일 크기, 파일 속도, 남은 시간입니다. 다운로드 진행을 보여주는 다른 예제입니다:

![progress](https://github.com/textualize/rich/raw/main/imgs/downloader.gif)

직접 해보시려면, 진행 바와 함께 여러개의 URL들을 동시에 다운로드 받는 예제인 [examples/downloader.py](https://github.com/textualize/rich/blob/main/examples/downloader.py)를 확인해주세요.

</details>

<details>
<summary>Status(상태)</summary>

진행 상황을 계산하기 어려운 경우, [상태](https://rich.readthedocs.io/en/latest/reference/console.html#rich.console.Console.status) 메서드를 사용할 수 있습니다. 이 메서드는 '스피너' 애니메이션과 메세지를 표시합니다. 애니메이션은 당신이 콘솔을 정상적으로 사용하는 것을 막지 못합니다. 다음은 예제입니다:

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

이 예제는 터미널에 아래와 같이 출력합니다.

![status](https://github.com/textualize/rich/raw/main/imgs/status.gif)

스피너 애니메이션은 [cli-spinners](https://www.npmjs.com/package/cli-spinners)에서 빌려왔습니다. `spinner` 파라미터를 선택해서 특정 스피너를 선택할 수도 있습니다. 어떤 값을 선택할 수 있는지는 아래 명령어를 통해 확인할 수 있습니다:

```
python -m rich.spinner
```

위의 명령어를 입력하면 아래와 같은 출력됩니다:

![spinners](https://github.com/textualize/rich/raw/main/imgs/spinners.gif)

</details>

<details>
<summary>Tree(트리)</summary>

Rich는 가이드라인과 함께 [트리](https://rich.readthedocs.io/en/latest/tree.html)를 표현할 수 있습니다. 파일 구조나, 계층적 데이터를 보여주는데 적합합니다.

트리의 라벨은 간단한 텍스트나 Rich로 표현할 수 있는 것은 모든지 가능합니다. 아래의 예시를 따라해보세요:

```
python -m rich.tree
```

이는 아래와 같이 출력됩니다:

![markdown](https://github.com/textualize/rich/raw/main/imgs/tree.png)

리눅스의 `tree` 명령어처럼 아무 디렉토리의 트리를 보여주는 스크립트 예제를 보시려면 [tree.py](https://github.com/textualize/rich/blob/main/examples/tree.py)를 확인해주세요.

</details>

<details>
<summary>Columns(칼럼)</summary>

Rich는 내용을 같거나 적절한 폭으로 깔끔하게 [칼럼](https://rich.readthedocs.io/en/latest/columns.html)을 표현할 수 있습니다. 아래 예제는 종렬로 디렉토리 리스트를 보여주는 (MacOS / Linux)의 `ls` 명령어의 기본적인 클론입니다:

```python
import os
import sys

from rich import print
from rich.columns import Columns

directory = os.listdir(sys.argv[1])
print(Columns(directory))
```

아래 스크린샷은 API에서 뽑은 데이터를 종렬로 표현하는 [칼럼 예제](https://github.com/textualize/rich/blob/main/examples/columns.py)의 출력 결과입니다:

![columns](https://github.com/textualize/rich/raw/main/imgs/columns.png)

</details>

<details>
<summary>Markdown(마크다운)</summary>

Rich는 [마크다운](https://rich.readthedocs.io/en/latest/markdown.html)을 표현하거나 형태를 터미널에 맞추어 적절히 변환할 수 있습니다.

마크다운을 표현하기 위해서는 `Markdown` 클래스를 import하고 마크다운을 포함하고 있는 문자열을 통해 객체를 생성해주세요. 다음은 예제입니다:

```python
from rich.console import Console
from rich.markdown import Markdown

console = Console()
with open("README.md") as readme:
    markdown = Markdown(readme.read())
console.print(markdown)
```

위 코드는 아래와 같은 출력 결과를 만들 것입니다:

![markdown](https://github.com/textualize/rich/raw/main/imgs/markdown.png)

</details>

<details>
<summary>Syntax Highlighting(구문 강조)</summary>

Rich는 [구문 강조](https://rich.readthedocs.io/en/latest/syntax.html) 기능을 수행하기 위해 [pygments](https://pygments.org/) 라이브러리를 사용합니다. 사용법은 마크다운과 유사합니다. `Syntax` 객체를 생성하고 콘솔에 출력하세요. 예제는 다음과 같습니다:

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

위 코드는 아래와 같은 출력 결과를 만들 것입니다:

![syntax](https://github.com/textualize/rich/raw/main/imgs/syntax.png)

</details>

<details>
<summary>Tracebacks</summary>

Rich는 [예쁜 tracebacks](https://rich.readthedocs.io/en/latest/traceback.html)을 표현할 수 있습니다. 이것은 읽기도 더 쉽고 일반적인 파이썬 tracebacks 보다 더 많은 코드를 보여줍니다. uncaught exceptions가 Rich로 출력되도록 Rich를 기본 Traceback 핸들러로 설정할 수도 있습니다.

OSX에서는 이렇게 출력됩니다 (리눅스도 유사함):

![traceback](https://github.com/textualize/rich/raw/main/imgs/traceback.png)

</details>

모든 Rich로 표현 가능한 것들은 [Console Protocol](https://rich.readthedocs.io/en/latest/protocol.html)를 사용합니다. 이것을 사용해서 자신의 Rich 컨텐츠를 렌더링할 수도 있습니다.

# 엔터프라이즈를 위한 Rich

Tidelift 구독의 일환으로 가능합니다.

Rich를 포함한 수천가지 다른 패키지들의 메인테이너들은 당신이 앱을 만들기 위해 사용하는 오픈소스 패키지의 상업적인 지원과 유지보수를 위해 Tidelift와 함께 일하고 있습니다. 당신이 사용하는 패키지의 메인테이너에게 비용을 지불하는 대신 시간을 절약하고, 리스크를 줄이고, 코드의 품질을 향상시킬 수 있습니다. [더 자세한 정보는 여기를 참고바랍니다.](https://tidelift.com/subscription/pkg/pypi-rich?utm_source=pypi-rich&utm_medium=referral&utm_campaign=enterprise&utm_term=repo)

# Rich를 사용하는 프로젝트들

Rich를 사용하는 몇가지 프로젝트들입니다:

- [BrancoLab/BrainRender](https://github.com/BrancoLab/BrainRender)
  신경해부학 데이터의 3차원 시각화를 위한 파이썬 패키지
- [Ciphey/Ciphey](https://github.com/Ciphey/Ciphey)
  자동 암호해독 툴
- [emeryberger/scalene](https://github.com/emeryberger/scalene)
  파이썬을 위한 고성능, 높은 정밀도의 CPU / Memory 프로파일러
- [hedythedev/StarCli](https://github.com/hedythedev/starcli)
  당신의 커맨드라인에서 GitHub 트렌딩 프로젝트들을 검색해보세요
- [intel/cve-bin-tool](https://github.com/intel/cve-bin-tool)
  이 툴은 여러 공통적이고 취약한 컴포넨트들(openssl, libpng, libxml2, expat 과 몇가지 더)을 스캔해, 이미 알려진 취약점을 가진 일반 라이브러리가 당신의 시스템에 있는지 알려줍니다.
- [nf-core/tools](https://github.com/nf-core/tools)
  nf-core 커뮤니티를 위한 도우미 도구를 포함한 파이썬 패키지.
- [cansarigol/pdbr](https://github.com/cansarigol/pdbr)
  개선된 디버깅을 위한 pdb + Rich 라이브러리
- [plant99/felicette](https://github.com/plant99/felicette)
  더미 위성 이미지
- [seleniumbase/SeleniumBase](https://github.com/seleniumbase/SeleniumBase)
  Selenium & pytest로 10배 더 빠르게 자동화 & 테스트하세요. 배터리도 포함되어 있습니다.
- [smacke/ffsubsync](https://github.com/smacke/ffsubsync)
  자동으로 자막과 영상의 싱크를 맞추세요.
- [tryolabs/norfair](https://github.com/tryolabs/norfair)
  모든 탐지된 것에 실시간으로 2D 오브젝트 트래킹을 추가하는 경량화된 파이썬 라이브러리.
- [ansible/ansible-lint](https://github.com/ansible/ansible-lint)
  Ansible-lint가 playbooks를 확인해 잠재적으로 개선될 수 있는 practices나 동작을 확인합니다.
- [ansible-community/molecule](https://github.com/ansible-community/molecule)
  Ansible Molecule의 테스트 프레임워크
- +[Many more](https://github.com/textualize/rich/network/dependents)!

<!-- This is a test, no need to translate -->
