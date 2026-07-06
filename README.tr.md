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
 • [Indonesian readme](https://github.com/textualize/rich/blob/main/README.id.md)
 • [فارسی readme](https://github.com/textualize/rich/blob/main/README.fa.md)
 • [Türkçe readme](https://github.com/textualize/rich/blob/main/README.tr.md)
 • [Polskie readme](https://github.com/textualize/rich/blob/main/README.pl.md)


Bir Python kütüphanesi olan __rich__, terminal üzerinde gösterişli çıktılar almanızı sağlayan bir araçtır.

[Rich API](https://rich.readthedocs.io/en/latest/) kullanarak terminal çıktılarınıza stil ekleyebilir ve renklendirebilirsiniz. Aynı zamanda tabloları, ilerleme çubuklarını, markdown stillerini, kaynak koddaki söz dizimi gösterimlerini ve bir çok şeyi rich kullanarak yapabilirsiniz.

![Features](https://github.com/textualize/rich/raw/main/imgs/features.png)

Rich'e video ile göz atmak için [@fishnets88](https://twitter.com/fishnets88) tarafından oluşturulan [calmcode.io](https://calmcode.io/rich/introduction.html) sitesine bakabilirsiniz.

İnsanların [rich hakkında yazdıkları son yazılar](https://www.willmcgugan.com/blog/pages/post/rich-tweets).

## Uyumluluk

Rich Linux, OSX ve Windows üzerinde çalışabilir. Windows'un yeni terminalinde de doğru bir şekilde çalışabilir, eski terminalde 16 renk olduğu için istenilen sonuçlar elde edilemeyebilir. Aynı zamanda Rich'in çalışabilmesi için ortamda minimum Python 3.6.3 veya daha yeni bir sürüm olması gerekmektedir.

Rich [Jupyter notebook](https://jupyter.org/) üzerinde hiç bir ek yükleme gerektirmeden çalışabilir.

## Yükleme

`pip` üzerinden veya kullanmış olduğunuz PyPI paket yöneticiniz üzerinden indirebilirsiniz.

```sh
python -m pip install rich
```

Aşağıdaki komut satırını çalıştırarak çıktınızı terminal üzerinden görebilirsiniz.


```sh
python -m rich
```

## Rich Print

[rich print](https://rich.readthedocs.io/en/latest/introduction.html#quick-start) methodunu yükleyerek, Rich'i kullanmaya başlayabilirsiniz.

```python
from rich import print

print("Merhaba, [bold magenta]Dünya[/bold magenta]!", ":vampire:", locals())
```

Buradaki yazıyı değiştiremediğim için siz hello world olarak görüyorsunuz. :D
![Hello World](https://github.com/textualize/rich/raw/main/imgs/print.png)

## Rich REPL

Rich Python REPL içerisine yüklenebilir, böylece herhangi bir veri tipini güzelce terminal çıktısı olarak verebilir.

```python
>>> from rich import pretty
>>> pretty.install()
```

![REPL](https://github.com/textualize/rich/raw/main/imgs/repl.png)

## Terminali Nasıl Kullanılır?

Çıktılarınız üzerinde daha fazla hakimiyet kurmak isterseniz, [Console](https://rich.readthedocs.io/en/latest/reference/console.html#rich.console.Console)'u import edip objesini kullanabilirsiniz.

```python
from rich.console import Console

console = Console()
```

Console objesi tıpkı Python içerisinde hazır gelen `print` methoduna benziyor, tabii daha fazlası da var.
Kullanımı aşağıdaki örnek gibi olacaktır:

```python
console.print("Merhaba", "Dünya!")
```

Sizin de tahmin edebileceğiniz gibi terminal çıktımız `"Merhaba Dünya!"` olacaktır. Standart `print` fonksiyonundan farklı olarak Console `print` fonksiyonu terminale sığmayan yazıları kaydırma özelliğine sahiptir.

Yazılarımıza birden fazla şekilde renk ekleyebiliriz. Bunlardan ek basit olan şekli, `style` argümanına rengimizi vermek. Aşağıda nasıl kullanılacağına dair bir örnek bulabilirsiniz.

```python
console.print("Merhaba", "Dünya!", style="bold red")
```

Eğer çıktıyı değiştirmeseydim aşağıdaki gibi bir görüntü ile karşılaşacaktınız:

![Hello World](https://github.com/textualize/rich/raw/main/imgs/hello_world.png)

Tek seferde bir yazıyı renklendirmek için kullanışlı bir yöntem olsa da, eğer çıktımızın sadece belirli bölgelerinde değişiklik yapacaksak [bbcode](https://en.wikipedia.org/wiki/BBCode) söz dizimini kullanmalıyız. Bunun için de bir örnek:

```python
console.print("[bold red]Mustafa Kemal Atatürk[/bold red] [u](1881 - 10 Kasım 1938)[/u], [i]Türk asker ve devlet adamıdır[/i]. [bold cyan]Türk Kurtuluş Savaşı'nın başkomutanı ve Türkiye Cumhuriyeti'nin kurucusudur[/bold cyan].")
```

![Console Markup](https://github.com/textualize/rich/raw/main/imgs/where_there_is_a_will.png)

Console objesini kullanarak sofistike bir çok çıktıyı minimum efor ile oluşturabilirsiniz. [Console API](https://rich.readthedocs.io/en/latest/console.html) dökümanına göz atarak daha fazla bilgi elde edebilirsiniz.

## Rich Inspect

Rich [inspect](https://rich.readthedocs.io/en/latest/reference/init.html?highlight=inspect#rich.inspect) adında bir fonksiyona sahiptir ve bu fonksiyon bize bir Python objesininin özelliklerini gösterir.

```python
>>> my_list = ["foo", "bar"]
>>> from rich import inspect
>>> inspect(my_list, methods=True)
```

![Log](https://github.com/textualize/rich/raw/main/imgs/inspect.png)

[Bu dökümana](https://rich.readthedocs.io/en/latest/reference/init.html#rich.inspect) göz atarak daha fazla bilgi elde edebilirsiniz...

# Rich Kütüphaneleri

Rich içerisinde terminal üzerinde kullandığınızda çıktılarınızı gösterişli kılacak çok fazla yapıya sahiptir.

Bu yapıların detayları için ilgili başlıklara tıklayın:

<details>
<summary>Log</summary>

Console objesi içerisinde `log()` methodunu barındırır, bu tıpkı `print()` methodu gibi davranır fakat buna ek olarak bastırıldığı zamanı da ekrana yansıtır. Bu duruma ek olarak Rich Syntax Highlighting'de gerçekleştirir.
Aşağıda örnek kod parçası:

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

Ve bu kod parçasının çıktısı:

![Log](https://github.com/textualize/rich/raw/main/imgs/log.png)

`log_locals` argümanı, local olarak bulunan değişkenleri tablo olarak ekrana bastırır.

</details>
<details>
<summary>Logging Handler</summary>

Python'un logging modülünü de [Handler sınıfı](https://rich.readthedocs.io/en/latest/logging.html) ile formatlayıp renklendirebiliriz.

![Logging](https://github.com/textualize/rich/raw/main/imgs/logging.png)

</details>

<details>
<summary>Emoji</summary>

Emojileri de kullanabilirsiniz, kullanımı markdown emojileri ile aynı.

```python
>>> console.print(":smiley: :vampire: :pile_of_poo: :thumbs_up: :raccoon:")
😃 🧛 💩 👍 🦝
```

Bu özelliği doğru yerlerde kullanmakta fayda var tabii.

</details>

<details>
<summary>Tables</summary>

Rich kullanıcılarına esnek bir [tablo](https://rich.readthedocs.io/en/latest/tables.html) imkanı sunar, birden fazla şekilde formatlayıp, stillendirip kullanabilirsiniz.

![table movie](https://github.com/textualize/rich/raw/main/imgs/table_movie.gif)

Yukarıdaki tablo örneği [table_movie.py](https://github.com/textualize/rich/blob/main/examples/table_movie.py) örnek kodu ile oluşturulmuştur.

Basit bir tablo örneği:

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

Kodun çıktısı aşağıdaki gibi olmaktadır:

![table](https://github.com/textualize/rich/raw/main/imgs/table.png)

Note that console markup is rendered in the same way as `print()` and `log()`. In fact, anything that is renderable by Rich may be included in the headers / rows (even other tables).

`Table` sınıfı kendini terminal ekranına göre ayarlayabilir, genişletip, küçültebilir. Burada bunun ile alakalı bir örnek görüyorsunuz.

![table2](https://github.com/textualize/rich/raw/main/imgs/table2.png)

</details>

<details>
<summary>Progress Bars</summary>

Uzun işlerinizi göstermek için Rich size birden fazla [progress](https://rich.readthedocs.io/en/latest/progress.html) bar sunuyor.

Basit bir kullanım için, herhangi bir adımınızı `track` fonksiyonu ile kapsayıp döngüye alın.

```python
from rich.progress import track

for step in track(range(100)):
    do_step(step)
```

Aşağıdaki görsellerde de görüleceği üzere birden fazla kez progress bar kullanabilirsiniz, ve dökümandan da anlaşılacağı üzere bu hiç de zor bir iş değil.

![progress](https://github.com/textualize/rich/raw/main/imgs/progress.gif)

Kolonlar kullanıcı tarafından ayarlanabilir, indirme hızını, dosya boyutunu yüzdesel olarak gösterimi gibi bir çok şekilde gösterim sağlayabilir.

![progress](https://github.com/textualize/rich/raw/main/imgs/downloader.gif)

Eğer siz de denemek isterseniz [examples/downloader.py](https://github.com/textualize/rich/blob/main/examples/downloader.py) koduna bakarak ve çalıştırarak indirme yapabilirsiniz.

</details>

<details>
<summary>Status</summary>

Eğer hesaplamanız gereken uzun işler varsa ve bunu progress bar ile gösteremiyorsanız yardımınıza [status](https://rich.readthedocs.io/en/latest/reference/console.html#rich.console.Console.status) methodu yetişecektir.

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

Yukarıdaki kod parçacığı aşağıdaki gibi bir çıktı üretecektir.

![status](https://github.com/textualize/rich/raw/main/imgs/status.gif)

Spin animasyonu [cli-spinners](https://www.npmjs.com/package/cli-spinners) kütüphanesinden alınmıştır. `spinner` parametresi ile seçeceğiniz spin şekilini kullanabilirsiniz. 

```
python -m rich.spinner
```

Çıktısı aşağıdaki gibi bir sonuç üretecektir:

![spinners](https://github.com/textualize/rich/raw/main/imgs/spinners.gif)

</details>

<details>
<summary>Tree</summary>

Rich bir [tree](https://rich.readthedocs.io/en/latest/tree.html) yapısını yardımcı çizgiler ile bastırabilir. Bu yapı bir dosya yapısını göstermek için veya hiyerarşik veri yapılarını göstermek için kullanılabilir.

Label yapısı ise basit bir text veya Rich üzerinde bastırılabilen her hangi bir yapı olabilir.

```
python -m rich.tree
```

Kodun çıkartacağı görüntü şu olacaktır:

![markdown](https://github.com/textualize/rich/raw/main/imgs/tree.png)

[tree.py](https://github.com/textualize/rich/blob/main/examples/tree.py) örnek dosyası ile linux'da bulunan `tree` kodunu rich üzerinden simüle edebilirsiniz.

</details>

<details>
<summary>Columns</summary>

Rich içerikleri [kolon](https://rich.readthedocs.io/en/latest/columns.html) olarak eşit veya optimal aralıklarla gösterebilir.

Burada basit bir `ls` klonunu görüyorsunz.

```python
import os
import sys

from rich import print
from rich.columns import Columns

directory = os.listdir(sys.argv[1])
print(Columns(directory))
```

Yukarıdaki yapıya [columns example](https://github.com/textualize/rich/blob/main/examples/columns.py) bağlantısı üzerinden ulaşabilirsiniz.

![columns](https://github.com/textualize/rich/raw/main/imgs/columns.png)

</details>

<details>
<summary>Markdown</summary>

Rich [markdown](https://rich.readthedocs.io/en/latest/markdown.html) stillerini ve çevirme işlemlerini de ekranda gösterebilir.

Sadece yapılması gereken `Markdown` sınıfını import edip, içeriğini doldurup ekrana bastırmak.

```python
from rich.console import Console
from rich.markdown import Markdown

console = Console()
with open("README.md") as readme:
    markdown = Markdown(readme.read())
console.print(markdown)
```

Aşağıdaki gibi bir çıktıya ulaşacağız.

![markdown](https://github.com/textualize/rich/raw/main/imgs/markdown.png)

</details>

<details>
<summary>Syntax Highlighting</summary>

Rich içerisinde [syntax highlighting](https://rich.readthedocs.io/en/latest/syntax.html) için [pygments](https://pygments.org/) kütüphanesini kullanıyor. Tıpkı markdown'da olduğu gibi, bir tane `Syntax` objesi oluşturup bu objeyi terminale bastırıyoruz.
Örnek:

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

Yukarıdaki kod parçası aşağıdaki gibi bir çıktı üretecektir.

![syntax](https://github.com/textualize/rich/raw/main/imgs/syntax.png)

</details>

<details>
<summary>Tracebacks</summary>

Rich sahip olduğu güzel [traceback](https://rich.readthedocs.io/en/latest/traceback.html)'ler yaratabilir. Böylece daha okunabilir ve daha kolay anlaşılabilen bir yapıya sahip olursunuz.

Burada OSX üzerinde (tıpkı Linux gibi) bir traceback çıktısı görüyorsunuz.

![traceback](https://github.com/textualize/rich/raw/main/imgs/traceback.png)

</details>

Tüm rich yapıları [Console Protocol](https://rich.readthedocs.io/en/latest/protocol.html) kullanılarak gerçekleştirilmiştir, siz de kendi içeriğinizi Rich'e aktarabilirsiniz.

# Rich CLI

Aynı zamanda [Rich CLI](https://github.com/textualize/rich-cli) uygulamasını da kontrol edin. Bu uygulama ile konsol çıktılarınızı renklendirebilir, kod çıktılarınıza syntax uygulayabilir, markdown gösterebilir, CSV dosyasını görüntüleyebilir ve daha bir çok şey yapabilirsiniz.


![Rich CLI](https://raw.githubusercontent.com/Textualize/rich-cli/main/imgs/rich-cli-splash.jpg)

# Textual

Rich'in kardeş projesi olan [Textual](https://github.com/Textualize/textual)'a da bir göz atın. Textual ile konsol çıktılarınıza bir UI oluşturup, gruplayıp görselleştirebilirsiniz.

![Textual screenshot](https://raw.githubusercontent.com/Textualize/textual/main/imgs/textual.png)

# Rich kullanılan Projeler

[Rich Galeri](https://www.textualize.io/rich/gallery)si üzerinden, rich kullanılan son uygulamalara [Textualize.io](https://www.textualize.io) üzerinden göz atabiirsiniz.

Eğer siz de projenizi galeriye eklemek istiyorsanız [bu adımları](https://www.textualize.io/gallery-instructions) takip ederek ekleyebilirsiniz.

<!-- This is a test, no need to translate -->
