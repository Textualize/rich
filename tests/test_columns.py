import io

from rich.columns import Columns
from rich.console import Console

COLUMN_DATA = [
    "Ursus americanus",
    "American buffalo",
    "Bison bison",
    "American crow",
    "Corvus brachyrhynchos",
    "American marten",
    "Martes americana",
    "American racer",
    "Coluber constrictor",
    "American woodcock",
    "Scolopax minor",
    "Anaconda (unidentified)",
    "Eunectes sp.",
    "Andean goose",
    "Chloephaga melanoptera",
    "Ant",
    "Anteater, australian spiny",
    "Tachyglossus aculeatus",
    "Anteater, giant",
    "Myrmecophaga tridactyla",
]


def render():
    console = Console(file=io.StringIO(), width=100)
    columns = Columns(COLUMN_DATA)
    console.print(columns)
    console.print()
    columns.column_first = True
    console.print(columns)
    console.print()
    columns.right_to_left = True
    console.print(columns)
    console.print()
    columns.equal = True
    columns.expand = True
    console.print(columns)
    console.print()
    columns.width = 16
    console.print(columns)
    console.print()

    render_result = console.file.getvalue()
    return render_result


def test_render():
    expected = "Ursus americanus           American buffalo       Bison bison            American crow          \nCorvus brachyrhynchos      American marten        Martes americana       American racer         \nColuber constrictor        American woodcock      Scolopax minor         Anaconda (unidentified)\nEunectes sp.               Andean goose           Chloephaga melanoptera Ant                    \nAnteater, australian spiny Tachyglossus aculeatus Anteater, giant        Myrmecophaga tridactyla\n\nUrsus americanus      American marten     Scolopax minor          Ant                       \nAmerican buffalo      Martes americana    Anaconda (unidentified) Anteater, australian spiny\nBison bison           American racer      Eunectes sp.            Tachyglossus aculeatus    \nAmerican crow         Coluber constrictor Andean goose            Anteater, giant           \nCorvus brachyrhynchos American woodcock   Chloephaga melanoptera  Myrmecophaga tridactyla   \n\nAnt                        Scolopax minor          American marten     Ursus americanus     \nAnteater, australian spiny Anaconda (unidentified) Martes americana    American buffalo     \nTachyglossus aculeatus     Eunectes sp.            American racer      Bison bison          \nAnteater, giant            Andean goose            Coluber constrictor American crow        \nMyrmecophaga tridactyla    Chloephaga melanoptera  American woodcock   Corvus brachyrhynchos\n\nChloephaga melanoptera           American racer                    Ursus americanus                 \nAnt                              Coluber constrictor               American buffalo                 \nAnteater, australian spiny       American woodcock                 Bison bison                      \nTachyglossus aculeatus           Scolopax minor                    American crow                    \nAnteater, giant                  Anaconda (unidentified)           Corvus brachyrhynchos            \nMyrmecophaga tridactyla          Eunectes sp.                      American marten                  \n                                 Andean goose                      Martes americana                 \n\nTachyglossus     Chloephaga       Anaconda         Coluber         Corvus           Ursus americanus\naculeatus        melanoptera      (unidentified)   constrictor     brachyrhynchos                   \nAnteater, giant  Ant              Eunectes sp.     American        American marten  American buffalo\n                                                   woodcock                                         \nMyrmecophaga     Anteater,        Andean goose     Scolopax minor  Martes americana Bison bison     \ntridactyla       australian spiny                                                                   \n                                                                   American racer   American crow   \n\n"
    assert render() == expected


if __name__ == "__main__":
    result = render()
    print(result)
    print(repr(result))
