"""List tests."""


from lists import DLList, keep, reverse, sort


def test_into_generator() -> None:
    """Test generator."""
    x = [1, 2, 3, 4, 5]
    for obs, exp in zip(DLList(x).into_generator(), x):
        assert obs == exp
def test_into_reverse_generator() -> None:
    """Test generator reverse."""
    x = [1, 2, 3, 4, 5]
    observed= DLList(x).into_reverse_generator()
    x.reverse()
    for obs, exp in zip(observed, x):
        assert obs == exp

def test_equality() -> None:
    assert DLList([1, 2, 3, 4, 5]) == DLList([1, 2, 3, 4, 5])
    assert DLList([1, 2, 3, 4, 5]) != DLList([1, 2, 4, 4, 5])
    assert DLList([1, 2, 3, 4, 5]) != DLList([1, 4, 5])


def test_keep() -> None:
    x = DLList([1, 2, 3, 4, 5])
    assert keep(x, lambda a: a % 2 == 0) == DLList([2, 4])

def test_reverse() -> None:
    x, expected = DLList([1, 2, 3, 4, 5]), DLList([5, 4, 3, 2, 1])
    assert reverse(x) == expected

def test_sort() -> None:
    x, expected = DLList([1, 3, 12, 6, 4, 5]), DLList([1, 3, 4, 5, 6, 12])
    sort(x) 
    assert x == expected
    x, expected = DLList([5, 4, 3, 2, 1, 0]), DLList([0, 1, 2, 3, 4, 5])
    sort(x) 
    assert x == expected