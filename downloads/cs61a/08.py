# Tree Recursion Review

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

# Lists practice

"""
digits = [1, 8, 2, 8]
digits[0]
digits[3]
len(digits)
digits[4]
digits[-1]
digits[-2]
[digits[0], digits[3]]
[digits[0], digits[3]][1]

for x in digits:
    print(100 * x)
digits

for d in digits:
    d = -d
    print(d)
digits
d

nums = [70, 80, 90]
nums + digits
digits + nums
for x in nums + digits:
    print(-x)
nums
digits

8 in digits
[1, 8] in digits
1 in digits and 8 in digits
"""

# Range practice

"""
range(-2, 2)
my_range = range(-2, 2)
-2 in my_range
2 in my_range
list(my_range)
...
my_range[3]
...
range(4)
list(range(4))
...
range(1, 101)
[1, 2, 3, ...]
range(2, 100000000)
list(range(2, 100000000))
...
type([1, 2, 3])
type(range(1, 4))
"""

# List comprehensions

"""
digits = [1, 8, 2, 8]
for x in digits:
    print(100 * x)
digits
hundreds = [100 * x for x in digits]
hundreds
digits
hundreds[2]
...
digits
[100 * x for x in digits]
[100 * x for x in digits if x < 5]
[100 * x for x in digits if x > 5]
...
digits
[[1], [1, 8], [1, 8, 2], [1, 8, 2, 8]]
[[digits[i] for i in range(0, end)] for end in range(1, 5)]
"""

# List comprehension practice

xs = range(-10, 11)
ys = [x*x - 2*x + 1 for x in xs]
[x for x in xs if x > -5]

xs_where_y_is_below_10 = [x for x in xs if x*x - 2*x + 1 < 10]
i = 13
xs[i]
ys[i]
[xs[i] for i in range(len(xs))]
[x for x in xs]
xs_where_y_is_below_10 = [xs[i] for i in range(len(xs)) if ys[i] < 10]

# Recursion

def sum_list(s):
    """Sum the elements of list s.

    >>> sum([2, 4, 1, 3])
    10
    """
    if len(s) == 0:
        return 0
    else:
        return s[0] + sum_list(s[1:])

def large(s, n):
    """Return the sublist of positive numbers s with the largest sum up to n.

    >>> large([4, 2, 5, 6, 7], 1)
    []
    >>> large([4, 2, 5, 6, 7], 3)
    [2]
    >>> large([4, 2, 5, 6, 7], 8)
    [2, 6]
    >>> large([4, 2, 5, 6, 7], 19)
    [4, 2, 6, 7]
    >>> large([4, 2, 5, 6, 7], 20)
    [2, 5, 6, 7]
    >>> large([4, 2, 5, 6, 7], 24)
    [4, 2, 5, 6, 7]
    """
    if s == []:
        return []
    elif s[0] > n:
        return large(s[1:], n)
    else:
        first = s[0]  # a number
        with_s0 = [first] + large(s[1:], n - first)
        without_s0 = large(s[1:], n)
        if sum_list(with_s0) > sum_list(without_s0):
            return with_s0
        else:
            return without_s0

# More Tree Recursion Practice

# Least Resistance Skeleton

# def least_resistance(m, n, f):
#     """
#     >>> f = lambda x, y: x ** 2 + y ** 2
#     >>> least_resistance(5, 5, f)
#     195
#     >>> g = lambda x, y: y
#     >>> least_resistance(5, 5, g)
#     15
#     """
#     if __________:
#         return __________
#     elif __________:
#         return float('inf')
#     else:
#         r1 = least_resistance(______________________________)
#         r2 = least_resistance(______________________________)
#     return __________(r1, r2) + __________

# Least Resistance Solution:

def least_resistance(m, n, f):
    """
    >>> f = lambda x, y: x ** 2 + y ** 2
    >>> least_resistance(5, 5, f)
    195
    >>> g = lambda x, y: y
    >>> least_resistance(5, 5, g)
    15
    """
    if m == 0 and n == 0:
        return f(0, 0)
    elif m < 0 or n < 0:
        return float('inf')
    else:
        r1 = least_resistance(m - 1, n, f)
        r2 = least_resistance(m, n - 1, f)
    return min(r1, r2) + f(m, n)
