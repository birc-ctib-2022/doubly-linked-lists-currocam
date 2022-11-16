"""List tests."""


from lists import DLList


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