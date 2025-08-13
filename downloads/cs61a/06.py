# Curry Review

## Partial Curry
def max(a, b, c):
    if a > b and a > c:
        return a
    elif b > a and b > c:
        return b
    else:
        return c

def partial_curry(f):
    def g(x):
        def h(y, z):
            return f(x, y, z)
        return h
    return g

def partial_curry_2(f):
    def g(x, y):
        def h(z):
            return f(x, y, z)
        return h
    return g

## Conditional Curry
def cond_curry(f, cond):
    """
    >>> from operator import add
    >>> curried = cond_curry(add, is_prime) # assume `is_prime` is implemented
    >>> curried(11)(13) # 11 + 13 = 24
    24
    >>> curried(10)(11)(12)(13) # 10 and 12 are not prime, and so are ignored
    24
    >>> curried(7)(4)(4)(4)(4)(4)(4)(4)(4)(7)
    14
    """
    # Lecture skeleton
    # __________:
    #     if __________:
    #         __________:
    #             if __________:
    #                 return __________
    #             else:
    #                 return __________
    #         return __________
    #     else:
    #         return __________
    # return __________

# Recursion

def fact(n):
    """Compute n factorial.

    >>> fact(5)
    120
    >>> fact(0)
    1
    """
    if n == 0 or n == 1:
        return 1
    else:
        return fact(n-1) * n

# Iteration to Recursion

def num_digits_iter(n):
    """
    >>> num_digits_iter(123)
    3
    >>> num_digits_iter(12345)
    5
    >>> num_digits_iter(0)
    0
    """
    n_digits = 0
    while n > 0:
        n = n // 10
        n_digits = n_digits + 1
    return n_digits

def num_digits_rec(n):
    """
    >>> num_digits_rec(123)
    3
    >>> num_digits_rec(12345)
    5
    >>> num_digits_rec(0)
    0
    """
    if n == 0:
        return 0
    return 1 + num_digits_rec(n // 10)

### Appendix ###

# Some alternate solutions for cond_curry (there are many)
def cond_curry_lec(f, cond):
    # Lecture solution
    def g(x):
        if cond(x):
            def h(y):
                if cond(y):
                    return f(x, y)
                else:
                    return h
            return h
        else:
            return g
    return g

def cond_curry_short(f, cond):
    # Lecture solution without else's
    def g(x):
        if cond(x):
            def h(y):
                if cond(y):
                    return f(x, y)
                return h
            return h
        return g
    return g

def cond_curry_alt(f, cond):
    # One alternate solution (using different skeleton)
    def g(x):
        def h(y):
            if cond(y):
                return f(x, y)
            return h
        if cond(x):
            return h
        return g
    return g

# Helper for cond_curry
## https://cs61a.org/disc/sol-disc01/#q3-is-prime
def is_prime(n):
    """
    >>> is_prime(10)
    False
    >>> is_prime(7)
    True
    >>> is_prime(1) # one is not a prime number!!
    False
    """
    if n == 1:
        return False
    k = 2
    while k < n:
        if n % k == 0:
            return False
        k += 1
    return True
