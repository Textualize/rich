from typing import NamedTuple, Optional

import pytest

from rich._ratio import ratio_reduce, ratio_resolve


class Edge(NamedTuple):
    size: Optional[int] = None
    ratio: int = 1
    minimum_size: int = 1


@pytest.mark.parametrize(
    "total,ratios,maximums,values,result",
    [
        (20, [2, 4], [20, 20], [5, 5], [-2, -8]),
        (20, [2, 4], [1, 1], [5, 5], [4, 4]),
        (20, [2, 4], [1, 1], [2, 2], [1, 1]),
        (3, [2, 4], [3, 3], [2, 2], [1, 0]),
        (3, [2, 4], [3, 3], [0, 0], [-1, -2]),
        (3, [0, 0], [3, 3], [4, 4], [4, 4]),
    ],
)
def test_ratio_reduce(total, ratios, maximums, values, result):
    assert ratio_reduce(total, ratios, maximums, values) == result


def test_ratio_resolve():
    assert ratio_resolve(100, []) == []
    assert ratio_resolve(100, [Edge(size=100), Edge(ratio=1)]) == [100, 1]
    assert ratio_resolve(100, [Edge(ratio=1)]) == [100]
    assert ratio_resolve(100, [Edge(ratio=1), Edge(ratio=1)]) == [50, 50]
    assert ratio_resolve(100, [Edge(size=20), Edge(ratio=1), Edge(ratio=1)]) == [
        20,
        40,
        40,
    ]
    assert ratio_resolve(100, [Edge(size=40), Edge(ratio=2), Edge(ratio=1)]) == [
        40,
        40,
        20,
    ]
    assert ratio_resolve(
        100, [Edge(size=40), Edge(ratio=2), Edge(ratio=1, minimum_size=25)]
    ) == [40, 35, 25]
    assert ratio_resolve(100, [Edge(ratio=1), Edge(ratio=1), Edge(ratio=1)]) == [
        33,
        33,
        34,
    ]
    assert ratio_resolve(
        50, [Edge(size=30), Edge(ratio=1, minimum_size=10), Edge(size=30)]
    ) == [30, 10, 30]
    assert ratio_resolve(110, [Edge(ratio=1), Edge(ratio=1), Edge(ratio=1)]) == [
        36,
        37,
        37,
    ]
