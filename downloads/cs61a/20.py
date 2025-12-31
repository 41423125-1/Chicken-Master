# Reduce

from operator import add, mul, truediv
def reduce(f, s, initial):
    """Combine elements of s pairwise using f, starting with initial.

    >>> reduce(mul, [2, 4, 8], 1)
    64
    >>> reduce(pow, [1, 2, 3, 4], 2)
    16777216
    """

def divide_all(n, ds):
    """Divide n by every d in ds.

    >>> divide_all(1024, [2, 4, 8])
    16.0
    >>> divide_all(1024, [2, 4, 0, 8])
    inf
    """

def reduce(f, s, initial):
    """Combine elements of s pairwise using f, starting with initial.

    >>> reduce(mul, [2, 4, 8], 1)
    64
    >>> reduce(pow, [1, 2, 3, 4], 2)
    16777216
    """
    for x in s:
        initial = f(initial, x)
    return initial

def divide_all(n, ds):
    """Divide n by every d in ds.

    >>> divide_all(1024, [2, 4, 8])
    16.0
    >>> divide_all(1024, [2, 4, 0, 8])
    inf
    """
    try:
        return reduce(truediv, ds, n)
    except ZeroDivisionError:
        return float('inf')

def sum_squares(s):
    """Return the sum of squares of the numbers in s.

    >>> sum_squares([3, 4, 5])  # 3*3 + 4*4 + 5*5
    50
    """
    return reduce(lambda x, y: x + y * y, s, 0)

# Calculator

def calculator_demo():
    """
    scm> (+ 2 (* 3 4))
    14
    
    read> (+ 2 (* 3 4))
    Scheme: (+ 2 (* 3 4))
    Python: Pair('+', Pair(2, Pair(Pair('*', Pair(3, Pair(4, nil))), nil)))
    
    scm> (+ 2 (* 3 4))
    14
    
    read> (     +      2 ( *      3 4))
    Scheme: (+ 2 (* 3 4))
    Python: Pair('+', Pair(2, Pair(Pair('*', Pair(3, Pair(4, nil))), nil)))
    """

def pair_demos():
    """
    >>> s = Pair(2, Pair(3, Pair(4, nil)))
    >>> s
    Pair(2, Pair(3, Pair(4, nil)))
    >>> s.first
    2
    >>> s.rest
    Pair(3, Pair(4, nil))
    >>> print(s)
    (2 3 4)
    >>> print(s.rest)
    (3 4)
    >>> s
    Pair(2, Pair(3, Pair(4, nil)))
    >>> s.rest
    Pair(3, Pair(4, nil))
    >>> s.map(lambda x: x * x)
    Pair(4, Pair(9, Pair(16, nil)))
    >>> print(s.map(lambda x: x * x))
    (4 9 16)
    """

# Applying Built-in Operators

def more_calculator_demos():
    """
    # Add @trace to calc_eval
    scm> (+ 2 (* 3 4))
    
    # Add @trace to calc_apply
    scm> (+ 2 (* 3 4))
    """

def exception_in_repl_demo():
    """
    scm> (+ 2 (~ 3 4))
    """

# Scheme
def scheme_demo():
    """
    # CAREFULLY Add @trace to scheme_eval
    scm> (+ 3 4)
    7
    scm> (define f +)
    f
    scm> (f 3 4)
    7
    
    scm> (if (> (f 3 4) 10) (- 5) (* 6 7))
    """
