"""Doubly-linked lists."""

from __future__ import annotations
from typing import (
    Generic, TypeVar, Iterable,
    Callable, Protocol
)


class Comparable(Protocol):
    """Type info for specifying that objects can be compared with <."""

    def __lt__(self, other: Comparable) -> bool:
        """Less than, <, operator."""
        ...


T = TypeVar('T')
S = TypeVar('S', bound=Comparable)


class Link(Generic[T]):
    """Doubly linked link."""

    val: T
    prev: Link[T]
    next: Link[T]

    def __init__(self, val: T, p: Link[T], n: Link[T]):
        """Create a new link and link up prev and next."""
        self.val = val
        self.prev = p
        self.next = n


def insert_after(link: Link[T], val: T) -> None:
    """Add a new link containing avl after link."""
    new_link = Link(val, link, link.next)
    new_link.prev.next = new_link
    new_link.next.prev = new_link


def remove_link(link: Link[T]) -> None:
    """Remove link from the list."""
    link.prev.next = link.next
    link.next.prev = link.prev


class DLList(Generic[T]):
    """
    Wrapper around a doubly-linked list.

    This is a circular doubly-linked list where we have a
    dummy link that function as both the beginning and end
    of the list. By having it, we remove multiple special
    cases when we manipulate the list.

    >>> x = DLList([1, 2, 3, 4])
    >>> print(x)
    [1, 2, 3, 4]
    """

    head: Link[T]  # Dummy head link

    def __init__(self, seq: Iterable[T] = ()):
        """Create a new circular list from a sequence."""
        # Configure the head link.
        # We are violating the type invariants this one place,
        # but only here, so we ask the checker to just ignore it.
        # Once the head element is configured we promise not to do
        # it again.
        self.head = Link(None, None, None)  # type: ignore
        self.head.prev = self.head
        self.head.next = self.head

        # Add elements to the list, exploiting that self.head.prev
        # is the last element in the list, so appending means inserting
        # after that link.
        for val in seq:
            insert_after(self.head.prev, val)
    def __eq__(self, other: DLList):
        x, y = self.head.next, other.head.next
        while x != self.head and y != other.head:
            if x.val != y.val:
                return False
            x, y = x.next, y.next
        return x == self.head and y == other.head
    def into_generator(self):
        link = self.head.next
        while link and link is not self.head:
            yield(link.val)
            link = link.next
    def into_reverse_generator(self):
        link = self.head.prev
        while link and link is not self.head:
            yield(link.val)
            link = link.prev
    def __str__(self) -> str:
        """Get string with the elements going in the next direction."""
        elms: list[str] = []
        
        return f"[{', '.join(str(el) for el in self.into_generator())}]"
    __repr__ = __str__  # because why not?


# Exercises

def keep(x: DLList[T], p: Callable[[T], bool]) -> None:
    """
    Remove all elements from x that do not satisfy the predicate p.

    >>> x = DLList([1, 2, 3, 4, 5])
    >>> keep(x, lambda a: a % 2 == 0)
    >>> print(x)
    [2, 4]
    """
    link = x.head.next
    while link is not x.head:
        if not p(link.val): 
            remove_link(link)
        link = link.next 

def swap_dir(x: Link) -> None:
    x.next, x.prev = x.prev, x.next

def reverse(x: DLList[T]) -> None:
    """
    Reverse the list x.

    >>> x = DLList([1, 2, 3, 4, 5])
    >>> reverse(x)
    >>> print(x)
    [5, 4, 3, 2, 1]
    """
    link = x.head.next
    while link is not x.head:
        swap_dir(link)
        link = link.prev
    swap_dir(x.head)

def swap_link(actual: Link) -> None:
    insert_after(actual.next, actual.val)
    remove_link(actual) 


def sort(x: DLList[S]) -> None:
    """
    Sort the list x.

    >>> x = DLList([1, 3, 12, 6, 4, 5])
    >>> sort(x)
    >>> print(x)
    [1, 3, 4, 5, 6, 12]
    """
    def inner(x) -> bool:
        link, is_sorted = x.head.next, True
        while link.next.val is not None:
            if link.val > link.next.val:
                is_sorted, _ = False, swap_link(link)   
            link = link.next  
        return is_sorted
    while not inner(x):
        pass