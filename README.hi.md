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

Rich टर्मिनल में _समृद्ध_ पाठ और सुंदर स्वरूपण के लिए एक Python संग्रह है।


[Rich API](https://rich.readthedocs.io/en/latest/) टर्मिनल उत्पादन में रंग और शैली डालना आसान बनाता है। Rich सुंदर सारणियाँ, प्रगति सूचक डंडे, markdown, रचनाक्रम चिन्हांकित स्त्रोत कोड, ट्रेसबैक आदि प्रस्तुत कर सकता है - बिना कुछ बदले।

![Features](https://github.com/textualize/rich/raw/main/imgs/features.png)

Rich के वीडियो परिचय के लिए देखें [@fishnets88](https://twitter.com/fishnets88) द्वारा बनाई गई [calmcode.io](https://calmcode.io/rich/introduction.html)।


देखें [लोग रिच के बारे में क्या कह रहे हैं](https://www.willmcgugan.com/blog/pages/post/rich-tweets/)।

## अनुकूलता

Rich Linux, OSX, और Windows के साथ चल सकता है। सच्चा रंग/इमोजी नए Windows टर्मिनल के साथ काम करता है, पुराना टर्मिनल १६ रंगों तक ही सीमित है। Rich के लिए Python ३.६.१ या बाद का होना आवश्यक है।

Rich बिना किसी अतिरिक्त विन्यास के [Jupyter नोटबुक](https://jupyter.org/) के साथ काम करता है।

## स्थापना करना

`pip` या अपने पसंदीदा PyPI संकुल प्रबंधक (package manager) के द्वारा आप इसे स्थापित कर सकते हैं।

```sh
python -m pip install rich
```

आपके टर्मिनल पर Rich उत्पादन का परीक्षण करने के लिए यह चलाएं:
```sh
python -m rich
```

## Rich Print

अपने अनुप्रयोग में सरलता से समृद्ध उत्पादन जोड़ने के लिए, आप [rich print](https://rich.readthedocs.io/en/latest/introduction.html#quick-start) क्रिया को आयात कर सकते हैं, जिसका हस्ताक्षर अंतर्निहित Python क्रिया के समान है। यह चलाने की कोशिश करें:

```python
from rich import print

print("Hello, [bold magenta]World[/bold magenta]!", ":vampire:", locals())
```

![Hello World](https://github.com/textualize/rich/raw/main/imgs/print.png)

## Rich REPL

Rich को Python REPL में स्थापित किया जा सकता है, ताकि कोई भी डेटा संरचनाएं सुंदरता से छपे तथा चिह्नांकित हों।
```python
>>> from rich import pretty
>>> pretty.install()
```

![REPL](https://github.com/textualize/rich/raw/main/imgs/repl.png)

## कॉनसोल (Console) का इस्तेमाल करना

समृद्ध टर्मिनल वस्तुओं पर अधिक नियंत्रण के लिए, आयात और निर्मित करें एक [Console](https://rich.readthedocs.io/en/latest/reference/console.html#rich.console.Console) वस्तु को।

```python
from rich.console import Console

console = Console()
```

Console वस्तु के पास एक `print` क्रिया है जिसका अंतरापृष्ठ जानबूझ कर अंतर्निहित `print` क्रिया के सामान है। इसके इस्तेमाल का एक उदाहरण :
```python
console.print("Hello", "World!")
```


जैसा आप उम्मीद कर रहे होंगे, यह टर्मिनल पर `"Hello World!"` छाप देगा। ध्यान दें की अंतर्निहित `print` क्रिया के भिन्न, Rich आपके पाठ को "वर्ड-रैप" कर देगा ताकि वह टर्मिनल की चौड़ाई में फस सके।

अपने उत्पादन में रंग और शैली डालने के लिए एक से अधिक तरीके हैं। `style` कीवर्ड तर्क जोड़कर आप सम्पूर्ण उत्पादन के लिए शैली निर्धारित कर सकते हैं। इसका एक उदाहरण:
```python
console.print("Hello", "World!", style="bold red")
```

उत्पादन कुछ इस प्रकार का होगा:
![Hello World](https://github.com/textualize/rich/raw/main/imgs/hello_world.png)


ये एक बारी में एक पंक्ति का शैलीकरण करने के लिए तो ठीक है। अधिक बारीकी से शैलीकरण करने के लिए, Rich एक विशेष मार्कअप को प्रदर्शित करता है जो रचनाक्रम में [bbcode](https://en.wikipedia.org/wiki/BBCode) से मिलता-जुलता है। इसका एक उदाहरण:

```python
console.print("Where there is a [bold cyan]Will[/bold cyan] there [u]is[/u] a [i]way[/i].")
```

![Console Markup](https://github.com/textualize/rich/raw/main/imgs/where_there_is_a_will.png)

कम-से-कम मेहनत में परिष्कृत उत्पादन उत्पन्न करने के लिए आप एक Console वस्तु का उपयोग कर सकते हैं। अधिक जानकारी के लिए आप [Console API](https://rich.readthedocs.io/en/latest/console.html) का प्रलेख पढ़ सकते हैं।

## Rich Inspect

Rich में एक [inspect](https://rich.readthedocs.io/en/latest/reference/init.html?highlight=inspect#rich.inspect) फलन उपलब्ध है जो किसी भी Python वस्तु, जैसे की क्लास, इन्स्टैन्स या अंतर्निहित पर प्रतिवेदन उत्पादित कर सकता है।
```python
>>> my_list = ["foo", "bar"]
>>> from rich import inspect
>>> inspect(my_list, methods=True)
```

![Log](https://github.com/textualize/rich/raw/main/imgs/inspect.png)

अधिक जानकारी के लिए [inspect का प्रलेखन](https://rich.readthedocs.io/en/latest/reference/init.html#rich.inspect) पढ़ें।

# Rich संग्रह

Rich में कई अंतर्निहित _प्रतिपाद्य_ मौजूद हैं जिनका इस्तेमाल करके आप अपने CLI में सुंदर उत्पादन उत्पन्न कर सकते हैं तथा अपने कोड का दोषमार्जन (डीबग) करने में सहायता प सकते हैं।


जानकारी के लिए निम्न शीर्षकों पर क्लिक करें:

<details>
<summary>लॉग (Log)</summary>

Console वस्तु के पास एक `log()` फलन होता है जिसका अंतरापृष्ठ `print()` से मिलता है, पर साथ में वर्तमान समय और आवाहन करने वाली पंक्ति के लिए एक खाना प्रस्तुत करता है। व्यक्तिक्रम तौर पर Rich Python संरचनाएं एवं repr मालाओं (स्ट्रिंगों) पर रचनाक्रम चिह्नांकन करेगा। यदि आप एक संग्रह (यानि एक डिक्शनेरी या एक सूची) को लॉग करते हैं तो Rich उसे सुंदरता से छापेगा ताकि वह उपलब्ध जगह में फस सके। इनमें से कुछ विशेषताओं का उदहरण प्रस्तुत है:

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

उपर्युक्त कोड से निम्न उत्पादन उत्पन्न होता है:

![Log](https://github.com/textualize/rich/raw/main/imgs/log.png)

ध्यान दें `log_levels` तर्क की तरफ, जो एक सारणी उत्पादित करता है जिसमे लॉग फलन के आवाहन के स्थान के स्थानिये चर युक्त हैं।

लॉग फलन का इस्तेमाल परिसेवकों (सर्वर) जैसे लंबे समय के लिये चलने वाले अनुप्रयोगों के लिए टर्मिनल पर प्रचालेखन के लिए किया जा सकता है, पर यह एक बहुत अच्छा दोषमार्जन सहायक भी है।

</details>
<details>
<summary>प्रचालेखन संचालक</summary>

Python के `logging` मापांक से आए हुए उत्पादन का संरूपण एवं रंगीकरण करने के लिए आप अंतर्निहित [Handler वर्ग](https://rich.readthedocs.io/en/latest/logging.html) का भी इस्तेमाल कर सकते हैं। उत्पादन का एक उपहरण प्रस्तुत है:

![Logging](https://github.com/textualize/rich/raw/main/imgs/logging.png)

</details>

<details>
<summary>इमोजी</summary>

Console उत्पादन में इमोजी डालने के लिए नाम को दो अपूर्ण विरामों (:) के बीच रखें। इसका एक उदाहरण:
```python
>>> console.print(":smiley: :vampire: :pile_of_poo: :thumbs_up: :raccoon:")
😃 🧛 💩 👍 🦝
```

कृपया इसका इस्तेमाल समझदारी से करें।
</details>

<details>
<summary>सारणियाँ</summary>

Rich यूनिकोड डिब्बा अक्षरों की सहायता से लचीली [सारणियाँ](https://rich.readthedocs.io/en/latest/tables.html) प्रदर्शित कर सकता है। सीमाएँ, शैलियाँ, कक्ष संरेखण आदि के लिए कई सारे स्वरूपण विकल्प उपलब्ध हैं।

![table movie](https://github.com/textualize/rich/raw/main/imgs/table_movie.gif)

उपर्युक्त अनुप्राणन examples डायरेक्टरी के [table_movie.py](https://github.com/textualize/rich/blob/main/examples/table_movie.py) से बनाया गया है।

इससे सरल संचिका का उदाहरण:
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

इससे निम्नलिखित उत्पादन उत्पन्न होता है:

![table](https://github.com/textualize/rich/raw/main/imgs/table.png)

ध्यान दें की कॉनसोल मार्कअप `print()` और `log()` की तरह ही प्रदर्शित होते हैं। वास्तव में, कोई भी वस्तु जो Rich के द्वारा प्रदर्शनीय है वह शीर्षकों / पंक्तियों (दूसरी संचिकाओं में भी) में युक्त किया जा सकता है।

`Table` वर्ग इतनी बुद्धिमान है की वह टर्मिनल की उपलब्ध चौड़ाई में फ़साने के लिए स्तंभों का आकार बदल सकता है, आवश्यकता के अनुसार पाठ को लपेटते हुए। यह वही उदाहरण है, टर्मिनल को उपर्युक्त संचिका से छोटा रखते हुए:

![table2](https://github.com/textualize/rich/raw/main/imgs/table2.png)

</details>

<details>
<summary>प्रगति सूचक डंडे</summary>

लंबे समय तक चलने वाले कार्यों पर नज़र रखने के लिए Rich अनेक झिलमिलाहट-मुक्त [प्रगति सूचक](https://rich.readthedocs.io/en/latest/progress.html) डंडे प्रदर्शित कर सकता है।

बुनियादी उपयोग के लिए, किसी भी क्रम को `track` फलन में लपेटें और परिणाम पर पुनरावर्तन करें। इसका एक उदाहरण:
```python
from rich.progress import track

for step in track(range(100)):
    do_step(step)
```

अनेक प्रगति सूचक डंडे जोड़ने इससे अधिक कठिन नहीं है। ये रहा एक उदाहरण जो प्रलेखन से उठाया गया है:
![progress](https://github.com/textualize/rich/raw/main/imgs/progress.gif)

स्तंभों का विन्यास इस प्रकार किया जा सकता है की आपकी इच्छानुसार विवरण दिखाए जाएँ। अंतर्निहित स्तंभ में प्रतिशत पूरा, संचिका आकार, संचिका गति तथा शेष समय युक्त होते हैं। ये रहा एक और उदाहरण एक चालू डाउनलोड को दर्शाते हुए।
![progress](https://github.com/textualize/rich/raw/main/imgs/downloader.gif)

इसे स्वयं आजमाने के लिए, देखें [examples/downloader.py](https://github.com/textualize/rich/blob/main/examples/downloader.py) जो अनेक URL एक साथ डाउनलोड करते हुए प्रगति दर्शाता है।
</details>

<details>
<summary>स्थिति</summary>

ऐसी परिस्थितियों में जहां प्रगति की गणना करना कठिन हों, आप [status](https://rich.readthedocs.io/en/latest/reference/console.html#rich.console.Console.status) (स्थिति) फलन का उपयोग कर सकते हैं जो एक 'स्पिनर' अनुप्राणन और संदेश दर्शाएगा। अनुप्राणन आपको सामान्य तरीके से कॉनसोल को इस्तेमाल करने से नहीं रोकेगा। ये एक उदाहरण:
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

इससे टर्मिनल में निम्नलिखित उत्पादन उत्पन्न होता है:
![status](https://github.com/textualize/rich/raw/main/imgs/status.gif)

स्पिनर अनुप्राणन [cli-spinners](https://www.npmjs.com/package/cli-spinners) से उधारे गए थे। आप `spinner` प्राचल को उल्लिखित करके स्पिनर चुन सकते हैं। उपलब्ध विकल्प देखने के लिए निम्नलिखित आदेश चलकर देखें:
```
python -m rich.spinner
```

उपर्युक्त आदेश टर्मिनल में निम्नलिखित उत्पादन उतपन्न करता है:
![spinners](https://github.com/textualize/rich/raw/main/imgs/spinners.gif)

</details>

<details>
<summary>वृक्ष</summary>

Rich मरकदर्शक रेखाओं से [tree](https://rich.readthedocs.io/en/latest/tree.html) (वृक्ष) प्रदर्शित कर सकता है। संचिता संरचना, अथवा कोई भी और पदानुक्रमित डेटा दर्शाने के लिए वृक्ष एक आदर्श विकल्प है।

वृक्ष के नाम सरल पाठ्यांश या कुछ भी और जो Rich प्रदर्शित कर सके। इसके एक प्रदर्शन के लिए निम्नलिखित को चलाएं:
```
python -m rich.tree
```

इससे निम्न उत्पादन उत्पन्न होता है:

![markdown](https://github.com/textualize/rich/raw/main/imgs/tree.png)

देखें उदाहरण [tree.py](https://github.com/textualize/rich/blob/main/examples/tree.py) एक क्रमादेश के लिए जो किसी भी डायरेक्टरी का वृक्ष दृश्य (ट्री व्यू) दर्शाएगा, लिनक्स के `tree` आदेश के समान।

</details>

<details>
<summary>स्तंभ</summary>


Rich सामग्री को समान अथवा श्रेष्ट चौड़ाई के साथ स्पष्ट [स्तंभ](https://rich.readthedocs.io/en/latest/columns.html) प्रदर्शित कार सकता है। यही (MacOS / Linux) `ls` आदेश का बहुत बुनियादी प्रतिरूप प्रस्तुत किया गया है जो स्तंभों में डायरेक्टरी सूची को दर्शाता है।

```python
import os
import sys

from rich import print
from rich.columns import Columns

directory = os.listdir(sys.argv[1])
print(Columns(directory))
```

निम्न स्क्रीनशॉट [स्तंभों के उदाहरण](https://github.com/textualize/rich/blob/main/examples/columns.py) का उत्पादन है जो एक API से खींचे गए डेटा को स्तंभों में प्रदर्शित करता है:
![columns](https://github.com/textualize/rich/raw/main/imgs/columns.png)

</details>

<details>
<summary>Markdown</summary>

Rich [markdown](https://rich.readthedocs.io/en/latest/markdown.html) को प्रदर्शित कार सकता है और स्वरूपण का अनुवाद टर्मिनल पर करने में उचित कार्य करता है।


Markdown प्रदर्शित करने के लिए आप `Markdown` वर्ग को आयात कार सकते हैं और उसे markdown कोड युक्त अक्षरमाला के साथ निर्मित कर सकते हैं। फिर उसे कॉनसोल पर छापें। एक उदाहरण प्रस्तुत है:
```python
from rich.console import Console
from rich.markdown import Markdown

console = Console()
with open("README.md") as readme:
    markdown = Markdown(readme.read())
console.print(markdown)
```

इससे कुछ इस प्रकार का उत्पादन उत्पन्न होगा:

![markdown](https://github.com/textualize/rich/raw/main/imgs/markdown.png)

</details>

<details>
<summary>रचनाक्रम चिह्नांकन</summary>

Rich [रचनाक्रम चिह्नांकन](https://rich.readthedocs.io/en/latest/syntax.html) के लिए [pygments](https://pygments.org/) संग्रह का उपयोग करता है। उपयोग markdown को प्रदर्शित करने से मिलता-जुलता है; एक `Syntax` वस्तु निर्मित करें और उसे कॉनसोल पर छापें। एक उदाहरण:
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

This will produce the following output:
इससे निम्न उत्पादन उत्पन्न होता है:

![syntax](https://github.com/textualize/rich/raw/main/imgs/syntax.png)

</details>

<details>
<summary>ट्रेसबैक</summary>

Rich [खूबसूरत ट्रेसबैक](https://rich.readthedocs.io/en/latest/traceback.html) दर्शा सकता है जो पढ़ने में आसान तथा मानक Python ट्रेसबैकों से अधिक कोड दिखाता है। आप Rich को व्यक्तीक्रम ट्रेसबैक संचालक भी निर्धारित कार सकते हैं ताकि सभी बेपकड़ अपवाद Rich के द्वारा प्रदर्शित हों।

OSX (Linux पर समान) पर यह कुछ इस प्रकार दिखता है:
![traceback](https://github.com/textualize/rich/raw/main/imgs/traceback.png)

</details>

सभी Rich प्रतिपाद्य [कॉनसोल प्रोटोकॉल](https://rich.readthedocs.io/en/latest/protocol.html) का उपयोग करते हैं, जिसे आप स्वयं की Rich सामग्री बनाने के लिए भी इस्तेमाल कार सकते हैं।

# उद्यम के लिए Rich

Tidelift Subscription के हिस्से के तौर पर उपलब्ध।

Rich एवं सहस्त्रों और संग्रहों के पालक आपके अनुप्रयोगों को बनाने के लिए इस्तेमाल किए जाने वाले खुले स्त्रोत संग्रहों के लिए व्यावसायिक सहायता तथा रखरखाव देने के लिए Tidelift के साथ काम कार रहे हैं। समय बचाइए, जोखिम काम कीजिए, और कोड स्वास्थ सुधारें, और साथ में जिन संग्रहों को आप इस्तेमाल करते हैं उनके पालकों को भुगतान करें। [अधिक जानें।](https://tidelift.com/subscription/pkg/pypi-rich?utm_source=pypi-rich&utm_medium=referral&utm_campaign=enterprise&utm_term=repo)

# Rich का उपयोग करने वाली परियोजनाएँ

ये रहे कुछ परियोजनाएँ जो Rich इस्तेमाल करते हैं।
- [BrancoLab/BrainRender](https://github.com/BrancoLab/BrainRender)
  त्रिविम न्यूरो-संरचनात्मक डेटा का चित्रण करने के लिए एक Python संग्रह
- [Ciphey/Ciphey](https://github.com/Ciphey/Ciphey)
  स्वचालित विकोडन उपकरण
- [emeryberger/scalene](https://github.com/emeryberger/scalene)
  Python के लिए एक उच्च-प्रदर्शन, उच्च-सूक्ष्मता CPU एवं स्मृति प्रोफाइलर
- [hedythedev/StarCli](https://github.com/hedythedev/starcli)
  अपनी आदेश पंक्ति (कमांड लाइन) से GitHub रुझानि परियोजिनाएं ब्राउज़ करें
- [intel/cve-bin-tool](https://github.com/intel/cve-bin-tool)
  यह उपकरण कई साधारण, भेद्य घटकों (openssl, libpng, libxml2, expat और कुछ और) के लिए जांच करता है ताकि आपको बता सके की क्या आपके तंत्र में जानी हुई कमज़ोरियों वाले संग्रह युक्त हैं।
- [nf-core/tools](https://github.com/nf-core/tools)
  nf-core समुदाय के लिए सहायक उपकरणों युक्त Python संग्रह
- [cansarigol/pdbr](https://github.com/cansarigol/pdbr)
  उन्नत दोषमार्जन के लिए pdb + Rich संग्रह
- [plant99/felicette](https://github.com/plant99/felicette)
  पुतलों के लिए उपग्रह चित्र
- [seleniumbase/SeleniumBase](https://github.com/seleniumbase/SeleniumBase)
  Selenium और pytest के साथ १० गुना तेज़ स्वचालन एवं परीक्षण करें। बैटरी शामिल।
- [smacke/ffsubsync](https://github.com/smacke/ffsubsync)
  स्वतः उपशीर्षकों को वीडियो के साथ समकालित करें।
- [tryolabs/norfair](https://github.com/tryolabs/norfair)
  किसी भी संसूचक में सद्य-अनुक्रिया द्विविम वस्तु ट्रैकिंग जोड़ने के लिए एक हल्का Python संग्रह।
- [ansible/ansible-lint](https://github.com/ansible/ansible-lint)
  Ansible-lint उन आचरणों और व्यवहारों के लिए प्लेबुकों में जाँच करता है जिन्हे संभावित रूप से सुधारा जा सकता है
- [ansible-community/molecule](https://github.com/ansible-community/molecule) Ansible Molecule testing framework
  Ansible Molecule परीक्षण ढांचा
- +[कई और](https://github.com/textualize/rich/network/dependents)!

<!-- This is a test, no need to translate -->
