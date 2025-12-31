# INIT ex.py:
def apply_twice(f, x):
    return f(f(x))

# Iteration Review - Repeating

def repeating(t, n):
    """Return whether t digits repeat to form positive integer n.

    >>> repeating(1, 6161)
    False
    >>> repeating(2, 6161)  # repeats 61 (2 digits)
    True
    >>> repeating(3, 6161)
    False
    >>> repeating(4, 6161)  # repeats 6161 (4 digits)
    True
    >>> repeating(5, 6161)  # there are only 4 digits
    False
    """
    if pow(10, t-1) > n:  # make sure n has at least t digits
        return False
    rest = n
    while rest:
        if rest % pow(10, t) != n % pow(10, t):
            return False
        rest = rest // pow(10, t)
    return True

# Environment Diagrams for higher-order functions

def make_adder(n):
    """Return a function that takes one argument k and returns k + n.

    >>> add_three = make_adder(3)
    >>> add_three(4)
    7
    """
    def adder(k):
        return k + n
    return adder

# Variations on make_adder
## Variation 1: https://pythontutor.com/cp/composingprograms.html#code=def%20make_adder%28n%29%3A%0A%20%20%20%20def%20adder%28k%29%3A%0A%20%20%20%20%20%20%20%20return%20k%20%2B%20n%0A%20%20%20%20return%20adder%285%29%0A%20%20%20%20%0Athree_more_than%20%3D%20make_adder%283%29%0Aresult%20%3D%20three_more_than%284%29&cumulative=false&curInstr=0&mode=display&origin=composingprograms.js&py=3&rawInputLstJSON=%5B%5D

## Variation 2: https://pythontutor.com/cp/composingprograms.html#code=def%20make_adder%28n%29%3A%0A%20%20%20%20def%20adder%28k%29%3A%0A%20%20%20%20%20%20%20%20return%20k%20%2B%20n%0A%20%20%20%20return%20adder%0A%20%20%20%20%0Aresult%20%3D%20make_adder%283%29%284%29&cumulative=false&curInstr=0&mode=display&origin=composingprograms.js&py=3&rawInputLstJSON=%5B%5D

# Lambda Expressions
def double(x):
    return 2 * x

"""
>>> apply_twice(lambda x: 2 * x, 5)
20
>>> apply_twice(double, 5)
20
"""

# Lambda Practice (Fall 2022 Midterm 1)

bear = -1
oski = lambda print: print(bear)
bear = -2
oski(abs)

# Zero-argument Functions
"""
>>> x = 10
>>> y = 2 * x
>>> y
20
>>> x = 5
>>> y
20
>>> exit()
>>> x = 10
>>> y = lambda: 2 * x
>>> y()
20
>>> x = 5
>>> y()
10
"""

# Currying

def curry(f):
    def g(x):
        def h(y):
            return f(x, y)
        return h
    return g
"""
>>> curried_add = curry(add)
>>> add_two = curried_add(2)
>>> # a lot of computation
>>> add_two(5)
7
>>> add_two(6)
8
>>> add_three = curried_add(3)
>>> add_three(6)
9
>>> add_three_v2 = make_adder(3)
>>> add_three_v2(6)
9
"""

## Currying Example Problem
def reverse(f):
    return lambda x, y: f(y, x)

# Currying with Lambdas
"""
>>> curry = lambda f: lambda x: lambda y: f(x, y)
>>> cube = curry(reverse(pow))(3)
>>> cube(2)
8
>>> cube(3)
27
>>> curry = (lambda f: (lambda x: (lambda y: f(x, y))))
"""
