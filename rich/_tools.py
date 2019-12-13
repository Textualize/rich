from typing import Iterable, List, Tuple, TypeVar

T = TypeVar("T")


def iter_first(values: Iterable[T]) -> Iterable[Tuple[bool, T]]:
    """Iterate and generate a tuple with a flag for first value."""
    iter_values = iter(values)
    try:
        value = next(iter_values)
    except StopIteration:
        return
    yield True, value
    for value in iter_values:
        yield False, value


def iter_last(values: Iterable[T]) -> Iterable[Tuple[bool, T]]:
    """Iterate and generate a tuple with a flag for last value."""
    iter_values = iter(values)
    try:
        previous_value = next(iter_values)
    except StopIteration:
        return
    for value in iter_values:
        yield False, previous_value
        previous_value = value
    yield True, previous_value


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


def ratio_divide(
    total: int, ratios: List[int], minimums: List[int] = None
) -> List[int]:
    """Divide an integer total in to parts based on ratios.
    
    Args:
        total (int): The total to divide.
        ratios (List[int]): A list of integer rations.
        minimums (List[int]): List of minimum values for each slot. 
    
    Returns:
        List[int]: A list of integers garanteed to sum to total.
    """
    total_ratio = sum(ratios)
    assert total_ratio > 0, "Sum of ratios must be > 0"

    total_remaining = total
    distributed_total: List[int] = []
    append = distributed_total.append
    if minimums is None:
        _minimums = [0] * len(ratios)
    else:
        _minimums = minimums
    for ratio, minimum in zip(ratios, _minimums):
        if total_ratio > 0:
            distributed = max(minimum, round(ratio * total_remaining / total_ratio))
        else:
            distributed = total_remaining
        append(distributed)
        total_ratio -= ratio
        total_remaining -= distributed
    return distributed_total


if __name__ == "__main__":  # pragma: no coverage

    n = ["foo", "bar", "egg", "baz"]
    for first, last, t in iter_first_last(n):
        print(first, last, t)

    print(ratio_divide(7, [1]))
    print(ratio_divide(10, [1, 2, 1]))
    print(ratio_divide(3, [1, 2, 1]))
    print(ratio_divide(20, [1, 2]))
    print(ratio_divide(7, [1, 0, 0]))
