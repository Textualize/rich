import pytest

from rich._ratio import ratio_reduce


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
