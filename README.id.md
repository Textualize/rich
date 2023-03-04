[![Supported Python Versions](https://img.shields.io/pypi/pyversions/rich/13.2.0)](https://pypi.org/project/rich/) [![PyPI version](https://badge.fury.io/py/rich.svg)](https://badge.fury.io/py/rich)

[![Downloads](https://pepy.tech/badge/rich/month)](https://pepy.tech/project/rich)
[![codecov](https://img.shields.io/codecov/c/github/Textualize/rich?label=codecov&logo=codecov)](https://codecov.io/gh/textualize/rich)
[![Rich blog](https://img.shields.io/badge/blog-rich%20news-yellowgreen)](https://www.willmcgugan.com/tag/rich/)
[![Twitter Follow](https://img.shields.io/twitter/follow/willmcgugan.svg?style=social)](https://twitter.com/willmcgugan)

![Logo](https://github.com/textualize/rich/raw/master/imgs/logo.svg)

[English readme](https://github.com/textualize/rich/blob/master/README.md)
 • [简体中文 readme](https://github.com/textualize/rich/blob/master/README.cn.md)
 • [正體中文 readme](https://github.com/textualize/rich/blob/master/README.zh-tw.md)
 • [Lengua española readme](https://github.com/textualize/rich/blob/master/README.es.md)
 • [Deutsche readme](https://github.com/textualize/rich/blob/master/README.de.md)
 • [Läs på svenska](https://github.com/textualize/rich/blob/master/README.sv.md)
 • [日本語 readme](https://github.com/textualize/rich/blob/master/README.ja.md)
 • [한국어 readme](https://github.com/textualize/rich/blob/master/README.kr.md)
 • [Français readme](https://github.com/textualize/rich/blob/master/README.fr.md)
 • [Schwizerdütsch readme](https://github.com/textualize/rich/blob/master/README.de-ch.md)
 • [हिन्दी readme](https://github.com/textualize/rich/blob/master/README.hi.md)
 • [Português brasileiro readme](https://github.com/textualize/rich/blob/master/README.pt-br.md)
 • [Italian readme](https://github.com/textualize/rich/blob/master/README.it.md)
 • [Русский readme](https://github.com/textualize/rich/blob/master/README.ru.md)
 • [Indonesian readme](https://github.com/textualize/rich/blob/master/README.id.md)
  • [فارسی readme](https://github.com/textualize/rich/blob/master/README.fa.md)
 • [Türkçe readme](https://github.com/textualize/rich/blob/master/README.tr.md)
 • [Polskie readme](https://github.com/textualize/rich/blob/master/README.pl.md)

Rich adalah library Python yang membantu _memperindah_ tampilan output suatu program di terminal.

[Rich API](https://rich.readthedocs.io/en/latest/) dapat digunakan untuk mempermudah dalam penambahan gaya dan pewarnaan output di terminal. Rich juga mendukung fitur lain seperti pembuatan tabel, bar progress, penulisan markdown, penghilightan syntax source code, tracebacks, dan masih banyak lagi.

![Features](https://github.com/textualize/rich/raw/master/imgs/features.png)

Sebagai pengenalan Rich saksikan video berikut [calmcode.io](https://calmcode.io/rich/introduction.html) oleh [@fishnets88](https://twitter.com/fishnets88).

Lihat pendapat [pengguna yang telah menggunakan Rich](https://www.willmcgugan.com/blog/pages/post/rich-tweets/).

## Kompabilitas

Rich dapat berjalan di Linux, OSX, dan Windows. Warna tambahan / emoji dapat berjalan di Windows Terminal baru, untuk terminal lama pewarnaan terbatas ke dalam 16 warna. Rich memerlukan versi Python 3.6.3 atau ke atas.

Rich dapat berjalan di [Jupyter notebooks](https://jupyter.org/) tanpa memerlukan konfigurasi tambahan.

## Instalasi

Install dengan `pip` atau paket manager favorit anda.

```sh
python -m pip install rich
```

Jalankan perintah berikut untuk menguji Rich di terminal anda:

```sh
python -m rich
```

## Rich Print

Untuk menambahkan rich sebagai output program anda, lakukan import method [rich print](https://rich.readthedocs.io/en/latest/introduction.html#quick-start), yang memiliki signature sama dengan fungsi built-in Python. Coba jalankan program berikut:

```python
from rich import print

print("Hello, [bold magenta]World[/bold magenta]!", ":vampire:", locals())
```

![Hello World](https://github.com/textualize/rich/raw/master/imgs/print.png)

## Rich REPL

Rich dapat diinstal ke dalam Python REPL sehingga setiap struktur data akan ditampilkan dengan indah dan terhighlight.

```python
>>> from rich import pretty
>>> pretty.install()
```

![REPL](https://github.com/textualize/rich/raw/master/imgs/repl.png)

## Penggunaan Console

Untuk kontrol lebih terhadap konten terminal, lakukan import dan susun suatu [Console](https://rich.readthedocs.io/en/latest/reference/console.html#rich.console.Console) object.

```python
from rich.console import Console

console = Console()
```

Console object memiliki method `print` yang berfungsi serupa dengan built-in `print`. Berikut adalah contoh penggunaannya:

```python
console.print("Hello", "World!")
```

Seperti yang anda perkirakan, perintah tersebut akan menampilkan `"Hello World!"` sebagai output di terminal. Catatan, perbedaan dengan fungsi built-in `print`, Rich membuat teks termampatkan disesuaikan dengan lebar terminal.

Terdapat beberapa cara untuk melakukan penambahan warna dan gaya output dari program anda. Anda dapat mengatur keseluruhan output dengan menambahkan keyword argumen `style`. Berikut adalah contoh penerapannya:

```python
console.print("Hello", "World!", style="bold red")
```

Output dari perintah tersebut akan tampak sebagai berikut:

![Hello World](https://github.com/textualize/rich/raw/master/imgs/hello_world.png)

Melakukan perubahan tampilan teks output dalam satu waktu mungkin sudah baik. Tetapi untuk membuat tampilan lebih rapi, Rich mendukung fitur rendering menggunakan pemformatan spesial dimana syntaxnya serupa dengan [bbcode](https://en.wikipedia.org/wiki/BBCode). Berikut adalah contoh penerapannya:

```python
console.print("Where there is a [bold cyan]Will[/bold cyan] there [u]is[/u] a [i]way[/i].")
```

![Console Markup](https://github.com/textualize/rich/raw/master/imgs/where_there_is_a_will.png)

Anda dapat menggunakan console object untuk menciptakan keluaran yang indah dengan usaha yang sedikit. Kunjungi [Console API](https://rich.readthedocs.io/en/latest/console.html) untuk informasi lebih lengkap.

## Rich Inspect

Rich memiliki fungsi [inspect](https://rich.readthedocs.io/en/latest/reference/init.html?highlight=inspect#rich.inspect) yang dapat membuat laporan untuk setiap Python object, seperti class, instance, atau built-in.

```python
>>> my_list = ["foo", "bar"]
>>> from rich import inspect
>>> inspect(my_list, methods=True)
```

![Log](https://github.com/textualize/rich/raw/master/imgs/inspect.png)

Kunjungi [dokumentasi inspect](https://rich.readthedocs.io/en/latest/reference/init.html#rich.inspect) untuk detail lebih lanjut.

# Rich Library

Rich mengandung sejumlah built-in yang bersifat _renderables_, artinya anda dapat menciptakan output yang elegant pda program CLI anda serta dapat membantu dalam proses debugging program anda.

Klik pilihan berikut untuk detail lebih lanjut:

<details>
<summary>Log</summary>

Console object mempunyai method bernama `log()` yang serupa dengan `print()`, tetapi juga mendukung fitur perenderan kolom waktu terkini serta baris file yang melakukan pemanggilan fungsi tertentu. Secara default Rich akan menghilight syntax untuk struktur python dan REPR strings. Jika anda melakukan log pada sekumpulan data (misal dictionary atau list) Rich akan memperindah output yang ditampilkan serta disesuaikan dengan ukuran terminal yang tersedia. Berikut adalah contoh penerapan dari beberapa fitur ini.

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

Perintah di atas akan menampilkan output sebagai berikut:

![Log](https://github.com/textualize/rich/raw/master/imgs/log.png)

Sebagai catatan, argumen `log_locals` berupa tabel yang berisikan variabel lokal yang menunjukkan lokasi dimana log tersebut dipanggil.

Method log ini dapat digunakan untuk mencatat aktivitas terminal yang berjalan lama seperti servers, tetapi method ini juga sangat baik untuk membantu dalam proses debugging.

</details>
<details>
<summary>Penanganan Logging</summary>

Anda dapat juga menggunakan builtin [Handler class](https://rich.readthedocs.io/en/latest/logging.html) untuk memformat dan mewarnai output dari module logging Python. Berikut adalah contoh penerapannya:

![Logging](https://github.com/textualize/rich/raw/master/imgs/logging.png)

</details>

<details>
<summary>Emoji</summary>

Untuk menambahkan emoji sebagai output di console, tuliskan nama emoji diantara dua buah titik dua (:). Berikut adalah contoh penerapannya:

```python
>>> console.print(":smiley: :vampire: :pile_of_poo: :thumbs_up: :raccoon:")
😃 🧛 💩 👍 🦝
```

Mohon gunakan fitur ini dengan bijak.

</details>

<details>
<summary>Tabel</summary>

Rich mendukung perenderan [tabel](https://rich.readthedocs.io/en/latest/tables.html) secara fleksibel dengan karakter unicode. Terdapat variasi sangat besar untuk opsi pemformatan seperti pengaturan border, gaya tabel, perataan teks di dalam cell, dan lain sebagainya.

![table movie](https://github.com/textualize/rich/raw/master/imgs/table_movie.gif)

Animasi di atas dibuat dengan program [table_movie.py](https://github.com/textualize/rich/blob/master/examples/table_movie.py) pada direktori examples.

Berikut adalah contoh tabel sederhana:

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

Program di atas akan menghasilkan output sebagai berikut:

![tabel](https://github.com/textualize/rich/raw/master/imgs/table.png)

Sebagai catatan console markup dirender sama seperti `print()` dan `log()`. Faktanya, untuk segala bentuk hal yang dapat dirender menggunakan Rich dapat disisipkan ke dalam header / baris (bahkan tabel lain).

Class `Table` memiliki kemampuan yang baik untuk mengatur ukuran kolom supaya sesuai dengan lebar yang disediakan oleh terminal. Berikut adalah contoh penerapannya, dengan terminal memiliki ukuran yang lebih kecil dibandingkan tabel di atas:

![table2](https://github.com/textualize/rich/raw/master/imgs/table2.png)

</details>

<details>
<summary>Bar Progress</summary>

Rich dapat merender beragam bar [progress](https://rich.readthedocs.io/en/latest/progress.html) interaktif untuk memantau kemajuan yang telah dicapai oleh program yang berjalan lama.

Untuk penggunaan dasar, masukan setiap urutan yang hendak dijadikan ke dalam bentuk progress ke dalam fungsi 'track' dan  iterasikan urutan tersebut di atas outputnya. Berikut adalah contoh penerapannya:

```python
from rich.progress import track

for step in track(range(100)):
    do_step(step)
```

Tidaklah sulit untuk menambahkan beberapa bar progress sekaligus. Berikut adalah contoh implementasi yang diambil dari file dokumentasi:

![progress](https://github.com/textualize/rich/raw/master/imgs/progress.gif)

Bagian kolom dapat dikonfigurasikan sesuai dengan kebutuhan. Built-in kolom juga memiliki fitur presentasi seleasi, ukuran file, kecepatan file, dan waktu sisa. Berikut adalah contoh menampilkan bar progress ketika mengunduh suatu file:

![progress](https://github.com/textualize/rich/raw/master/imgs/downloader.gif)

Untuk bereksperimen, periksa [examples/downloader.py](https://github.com/textualize/rich/blob/master/examples/downloader.py) yang dapat menampilkan beberapa progress bar  pengunduhan dari beberapa alamat URL sekaligus.

</details>

<details>
<summary>Status</summary>

Untuk kondisi dimana perhitungan sulit dilakukan dengan perhitunggan progress, gunakan method [status](https://rich.readthedocs.io/en/latest/reference/console.html#rich.console.Console.status) berikut yang menampilkan animasi 'spinner' dan pesan. Animasi tersebut tidak mencegah penggunaan console seperti keadaan normal. Berikut adalah contoh penerapannya:

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

Program di atas akan menghasilkan output sebagai berikut.

![status](https://github.com/textualize/rich/raw/master/imgs/status.gif)

Animasi spinner tersebut diambil dari [cli-spinners](https://www.npmjs.com/package/cli-spinners). Anda dapat menentukan spinner yang hendak digunakan dengan menspesifikannya di parameter `spinner`. Jalankan perintah berikut untuk melihat parameter yang tersedia:

```
python -m rich.spinner
```

Perintah di atas akan menghasilkan output sebagai berikut:

![spinners](https://github.com/textualize/rich/raw/master/imgs/spinners.gif)

</details>

<details>
<summary>Tree</summary>

Rich dapat merender perintah [tree](https://rich.readthedocs.io/en/latest/tree.html) beserta dengan garis penunjuk. Suatu perintah tree idealnya digunakan untuk menampilkan struktur suatu file atau data hierarki lainnya.

Label dari tree dapat berupa teks sederhana atau apapun yang dapat dirender oleh Rich, untuk contoh, jalankan perintah berikut:

```
python -m rich.tree
```

Program di atas akan menghasilkan output sebagai berikut:

![markdown](https://github.com/textualize/rich/raw/master/imgs/tree.png)

Periksa contoh program [tree.py](https://github.com/textualize/rich/blob/master/examples/tree.py) untuk menampilkan tampilan tree view dari direktori apapun, perintah ini serupa dengan `tree` pada linux.

</details>

<details>
<summary>Kolom</summary>

Rich dapat merender konten [kolom](https://rich.readthedocs.io/en/latest/columns.html) secara rapi dengan ukuran lebar yang sama atau optimal. Berikut adalah hasil kloning perintah dasar dari (MacOS / Linux) yaitu `ls` untuk melakukan listing direktori menggunakan kolom:

```python
import os
import sys

from rich import print
from rich.columns import Columns

directory = os.listdir(sys.argv[1])
print(Columns(directory))
```

Screenshot berikut merupakan output dari [contoh kolom](https://github.com/textualize/rich/blob/master/examples/columns.py) yang menampilkan data yang diambil melalui API ke dalam bentuk kolom:

![columns](https://github.com/textualize/rich/raw/master/imgs/columns.png)

</details>

<details>
<summary>Markdown</summary>

Rich dapat merender [markdown](https://rich.readthedocs.io/en/latest/markdown.html) dan melakukan tugasnya untuk menerjemahkan format tersebut supaya dapat ditampilkan di terminal.

Untuk dapat merender markdown, import class `Markdown` dan inputkan string yang mengandung markdown tersebut. Lalu cetak ke dalam console. Berikut adalah contoh penerapannya:

```python
from rich.console import Console
from rich.markdown import Markdown

console = Console()
with open("README.md") as readme:
    markdown = Markdown(readme.read())
console.print(markdown)
```

Program di atas akan menghasilkan output seperti berikut:

![markdown](https://github.com/textualize/rich/raw/master/imgs/markdown.png)

</details>

<details>
<summary>Penghilightan Syntax</summary>

Rich memanfaatkan library [pygments](https://pygments.org/) supaya dapat melakukan [penghilightan syntax](https://rich.readthedocs.io/en/latest/syntax.html). Penggunaannya serupa dengan merender markdown; susun object `Syntax` dan cetak output pada console. Berikut adalah contoh penerapannya:

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

Program di atas akan menghasilkan output sebagai berikut:

![syntax](https://github.com/textualize/rich/raw/master/imgs/syntax.png)

</details>

<details>
<summary>Tracebacks</summary>

Rich dapat merender [tracebacks dengan indah](https://rich.readthedocs.io/en/latest/traceback.html) yang membuatnya mudah untuk dibaca dan menampilkan program yang dibuat lebih baik dibandingkan fitur standar Python. Anda dapat mengatur Rich sebagai traceback handler secara default sehingga setiap pesan exceptions akan dirender melalui Rich.

Berikut adalah tampilannya pada OSX (serupa dengan Linux):

![traceback](https://github.com/textualize/rich/raw/master/imgs/traceback.png)

</details>

Semua perenderan Rich menggunakan [Console Protocol](https://rich.readthedocs.io/en/latest/protocol.html), anda dapat juga mengimplementasikannya pada konten Rich milik anda.

# Rich CLI


Baca juga [Rich CLI](https://github.com/textualize/rich-cli) sebuah program command line yang dibuat menggunakan Rich. Penghilightan syntax, perenderan markdown, menampilkan CSVs ke dalam tabel, dan masih banyak lagi, secara langsung melalui command prompt.


![Rich CLI](https://raw.githubusercontent.com/Textualize/rich-cli/main/imgs/rich-cli-splash.jpg)


# Projek yang telah menggunakan Rich

Berikut adalah beberpa projek yang menggunakan Rich:

- [BrancoLab/BrainRender](https://github.com/BrancoLab/BrainRender)
  Sebuah package Python untuk visualisasi data neuro-anatomi tiga dimensi.
- [Ciphey/Ciphey](https://github.com/Ciphey/Ciphey)
  Tools yang digunakan untuk melakukan deskripsi otomatis.
- [emeryberger/scalene](https://github.com/emeryberger/scalene)
  profiler memori dan CPU untuk Python yang memiliki nilai performa dan presisi tinggi.
- [hedythedev/StarCli](https://github.com/hedythedev/starcli)
  Melakukan penelusuran projek terkenal GitHub melalui command line.
- [intel/cve-bin-tool](https://github.com/intel/cve-bin-tool)
  Tools ini dapat digunakan untuk melakukan scanning pada komponen yang rentan  (openssl, libpng, libxml2, expat and a few others) untuk membuat anda mengetahui sistem anda mempunyai library yang telah diketahui kerentanannya.
- [nf-core/tools](https://github.com/nf-core/tools)
  package Python dengan tools bantuan untuk komunitas nf-core.
- [cansarigol/pdbr](https://github.com/cansarigol/pdbr)
  gabungan library pdb + Rich library untuk memperindah proses debugging.
- [plant99/felicette](https://github.com/plant99/felicette)
  gambar citra satelit untuk pemula.
- [seleniumbase/SeleniumBase](https://github.com/seleniumbase/SeleniumBase)
  tools otomatisasi dan test testing 10x lebih cepat dibandingkan dengan Selenium & pytest. Termasuk didalamnya baterai.
- [smacke/ffsubsync](https://github.com/smacke/ffsubsync)
  tools sinkronisasi subtitle dengan video.
- [tryolabs/norfair](https://github.com/tryolabs/norfair)
  Library Python ringan untuk menambahkan deteksi objek secara real-time pada objek 2D pada suatu detektor.
- [ansible/ansible-lint](https://github.com/ansible/ansible-lint) Sebuah ansible-lint untuk memeriksa playbooks yang digunakan sebagai practices and behaviour yang secara potensial dapat ditingkatkan.
- [ansible-community/molecule](https://github.com/ansible-community/molecule) Ansible Molecule untuk framework testing
- +[Lebih banyak lagi](https://github.com/textualize/rich/network/dependents)!

<!-- This is a test, no need to translate -->
