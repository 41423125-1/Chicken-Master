from link import *

# What is the efficiency of link_comp_recur with respect to the length of `lnk`?
## Assume `map_func` and `filter_func` take constant time.

def link_comp_recur(lnk, map_func, filter_func):
    """
    >>> lnk = Link(1, Link(2, Link(3, Link(4, Link(5)))))
    >>> print(lnk)
    <1 2 3 4 5>
    >>> add_one = lambda x: x + 1
    >>> is_even = lambda x: x % 2 == 0
    >>> print(link_comp_recur(lnk, add_one, is_even))
    <3 5>
    >>> square = lambda x: x ** 2
    >>> greater_than_2 = lambda x: x > 2
    >>> print(link_comp_recur(lnk, square, greater_than_2))
    <9 16 25>
    """
    if lnk is Link.empty:
        return Link.empty
    new_rest = link_comp_recur(lnk.rest, map_func, filter_func)
    if filter_func(lnk.first):
        return Link(map_func(lnk.first), new_rest)
    else:
        return new_rest
