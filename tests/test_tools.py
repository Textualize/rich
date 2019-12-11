from rich._tools import iter_first, iter_last, iter_first_last, ratio_divide


def test_iter_first():
    assert list(iter_first([])) == []
    iterable = iter_first(["apples", "oranges", "pears", "lemons"])
    assert next(iterable) == (True, "apples")
    assert next(iterable) == (False, "oranges")
    assert next(iterable) == (False, "pears")
    assert next(iterable) == (False, "lemons")


def test_iter_last():
    assert list(iter_last([])) == []
    iterable = iter_last(["apples", "oranges", "pears", "lemons"])
    assert next(iterable) == (False, "apples")
    assert next(iterable) == (False, "oranges")
    assert next(iterable) == (False, "pears")
    assert next(iterable) == (True, "lemons")


def test_iter_first_last():
    assert list(iter_first_last([])) == []
    iterable = iter_first_last(["apples", "oranges", "pears", "lemons"])
    assert next(iterable) == (True, False, "apples")
    assert next(iterable) == (False, False, "oranges")
    assert next(iterable) == (False, False, "pears")
    assert next(iterable) == (False, True, "lemons")


def test_ratio_divide():
    assert ratio_divide(10, [1]) == [10]
    assert ratio_divide(10, [1, 1]) == [5, 5]
    assert ratio_divide(12, [1, 3]) == [3, 9]
    assert ratio_divide(0, [1, 3]) == [0, 0]
    assert ratio_divide(0, [1, 3], [1, 1]) == [1, 1]
