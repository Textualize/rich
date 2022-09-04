from rich._loop import loop_first, loop_first_last, loop_last
from rich._ratio import ratio_distribute


def test_loop_first():
    assert list(loop_first([])) == []
    iterable = loop_first(["apples", "oranges", "pears", "lemons"])
    assert next(iterable) == (True, "apples")
    assert next(iterable) == (False, "oranges")
    assert next(iterable) == (False, "pears")
    assert next(iterable) == (False, "lemons")


def test_loop_last():
    assert list(loop_last([])) == []
    iterable = loop_last(["apples", "oranges", "pears", "lemons"])
    assert next(iterable) == (False, "apples")
    assert next(iterable) == (False, "oranges")
    assert next(iterable) == (False, "pears")
    assert next(iterable) == (True, "lemons")


def test_loop_first_last():
    assert list(loop_first_last([])) == []
    iterable = loop_first_last(["apples", "oranges", "pears", "lemons"])
    assert next(iterable) == (True, False, "apples")
    assert next(iterable) == (False, False, "oranges")
    assert next(iterable) == (False, False, "pears")
    assert next(iterable) == (False, True, "lemons")


def test_ratio_distribute():
    assert ratio_distribute(10, [1]) == [10]
    assert ratio_distribute(10, [1, 1]) == [5, 5]
    assert ratio_distribute(12, [1, 3]) == [3, 9]
    assert ratio_distribute(0, [1, 3]) == [0, 0]
    assert ratio_distribute(0, [1, 3], [1, 1]) == [1, 1]
    assert ratio_distribute(10, [1, 0]) == [10, 0]
