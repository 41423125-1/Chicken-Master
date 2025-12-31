def tuple_demos():
    s = (2, 3, 4)
    s
    s[0]
    s[1]
    s[1:]
    s + s
    (1, s)
    s.append(3)
    s.extend((4, 5))
    s[0] = 8

def iterator_demos():
    s = [3, 4, 5]
    next(s)
    t = iter(s)
    next(t)
    next(t)
    next(t)
    next(t)

    u = iter(s)
    next(u)
    sum(u)
    sum(s)
    
    v = iter(s)
    next(v)
    list(v)
    s
    list(v)
    next(v)

def map_demo():
    s = [3, 4, 5, 6]
    sum(s)
    sum(map(lambda x: x - 1, s))
    list(map(lambda x: x - 1, s))    

def average(s):
    """Return the average of values in a list.

    >>> average([3, 4, 5, 6])
    4.5
    >>> average(map(lambda x: x - 1, [3, 4, 5, 6]))
    Traceback (most recent call last):
        ...
    ZeroDivisionError: division by zero
    """
    return sum(s) / len(list(s))

"""
s = [3, 4, 5, 6]
m = map(lambda x: x - 1, s)
sum(m)
sum(m)

r = range(1, 10000000000000)
m = map(lambda x: x * x, r)
next(m)
next(m)
next(m)
next(m)
next(m)
"""

# Generators

def cycle(s):
    """Iterate over the elements of s repeatedly."""
    while True:
        for x in s:
            yield x

# Count Park

def count_park(n):
    """Count the ways to park cars and motorcycles in n adjacent spots.
    >>> count_park(1)  # '.' or '%'
    2
    >>> count_park(2)  # '..', '.%', '%.', '%%', or '<>'
    5
    >>> count_park(4)  # some examples: '<><>', '.%%.', '%<>%', '%.<>'
    29
    """
    if n < 0:
        return 0
    elif n == 0:
        return 1
    else:
        return 2 * count_park(n-1) + count_park(n-2)

# Yield Park

def park(n):
    """Return the ways to park cars and motorcycles in n adjacent spots.

    >>> sorted(park(1))
    ['%', '.']
    >>> sorted(park(2))
    ['%%', '%.', '.%', '..', '<>']
    >>> sorted(park(3))
    ['%%%', '%%.', '%.%', '%..', '%<>', '.%%', '.%.', '..%', '...', '.<>', '<>%', '<>.']
    >>> len(list(park(4)))
    29
    """
    if n == 0:
        yield ''
    elif n > 0:
        for s in park(n-1):
            yield '%'  + s
            yield '.'  + s
        for s in park(n-2):
            yield '<>' + s
