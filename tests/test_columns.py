# encoding=utf-8

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
]


def render():
    console = Console(file=io.StringIO(), width=100, legacy_windows=False)

    console.rule("empty")
    empty_columns = Columns([])
    console.print(empty_columns)
    columns = Columns(COLUMN_DATA)
    columns.add_renderable("Myrmecophaga tridactyla")
    console.rule("optimal")
    console.print(columns)
    console.rule("optimal, expand")
    columns.expand = True
    console.print(columns)
    console.rule("column first, optimal")
    columns.column_first = True
    columns.expand = False
    console.print(columns)
    console.rule("column first, right to left")
    columns.right_to_left = True
    console.print(columns)
    console.rule("equal columns, expand")
    columns.equal = True
    columns.expand = True
    console.print(columns)
    console.rule("fixed width")
    columns.width = 16
    columns.expand = False
    console.print(columns)
    console.print()
    render_result = console.file.getvalue()
    return render_result


def test_render():
    expected = "────────────────────────────────────────────── empty ───────────────────────────────────────────────\n───────────────────────────────────────────── optimal ──────────────────────────────────────────────\nUrsus americanus           American buffalo       Bison bison            American crow          \nCorvus brachyrhynchos      American marten        Martes americana       American racer         \nColuber constrictor        American woodcock      Scolopax minor         Anaconda (unidentified)\nEunectes sp.               Andean goose           Chloephaga melanoptera Ant                    \nAnteater, australian spiny Tachyglossus aculeatus Anteater, giant        Myrmecophaga tridactyla\n───────────────────────────────────────── optimal, expand ──────────────────────────────────────────\nUrsus americanus             American buffalo        Bison bison             American crow          \nCorvus brachyrhynchos        American marten         Martes americana        American racer         \nColuber constrictor          American woodcock       Scolopax minor          Anaconda (unidentified)\nEunectes sp.                 Andean goose            Chloephaga melanoptera  Ant                    \nAnteater, australian spiny   Tachyglossus aculeatus  Anteater, giant         Myrmecophaga tridactyla\n────────────────────────────────────── column first, optimal ───────────────────────────────────────\nUrsus americanus      American marten     Scolopax minor          Ant                       \nAmerican buffalo      Martes americana    Anaconda (unidentified) Anteater, australian spiny\nBison bison           American racer      Eunectes sp.            Tachyglossus aculeatus    \nAmerican crow         Coluber constrictor Andean goose            Anteater, giant           \nCorvus brachyrhynchos American woodcock   Chloephaga melanoptera  Myrmecophaga tridactyla   \n─────────────────────────────────── column first, right to left ────────────────────────────────────\nAnt                        Scolopax minor          American marten     Ursus americanus     \nAnteater, australian spiny Anaconda (unidentified) Martes americana    American buffalo     \nTachyglossus aculeatus     Eunectes sp.            American racer      Bison bison          \nAnteater, giant            Andean goose            Coluber constrictor American crow        \nMyrmecophaga tridactyla    Chloephaga melanoptera  American woodcock   Corvus brachyrhynchos\n────────────────────────────────────── equal columns, expand ───────────────────────────────────────\nChloephaga melanoptera                American racer                    Ursus americanus            \nAnt                                   Coluber constrictor               American buffalo            \nAnteater, australian spiny            American woodcock                 Bison bison                 \nTachyglossus aculeatus                Scolopax minor                    American crow               \nAnteater, giant                       Anaconda (unidentified)           Corvus brachyrhynchos       \nMyrmecophaga tridactyla               Eunectes sp.                      American marten             \n                                      Andean goose                      Martes americana            \n─────────────────────────────────────────── fixed width ────────────────────────────────────────────\nAnteater,         Eunectes sp.     Coluber          Corvus           Ursus americanus \naustralian spiny                   constrictor      brachyrhynchos                    \nTachyglossus      Andean goose     American         American marten  American buffalo \naculeatus                          woodcock                                           \nAnteater, giant   Chloephaga       Scolopax minor   Martes americana Bison bison      \n                  melanoptera                                                         \nMyrmecophaga      Ant              Anaconda         American racer   American crow    \ntridactyla                         (unidentified)                                     \n\n"
    assert render() == expected


if __name__ == "__main__":
    result = render()
    print(result)
    print(repr(result))
