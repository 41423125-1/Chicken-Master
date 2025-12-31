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

# Lists & Recursion

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

def add_consecutive(n):
    """
    >>> add_consecutive(123456789)
    [45]
    >>> add_consecutive(567231) # [5 + 6 + 7, 2 + 3, 1]
    [18, 5, 1]
    >>> add_consecutive(111) # repeated digits are not consecutive
    [1, 1, 1]
    >>> add_consecutive(1235689)
    [6, 11, 17]
    >>> add_consecutive(3216598)
    [6, 11, 17]
    >>> add_consecutive(13579)
    [1, 3, 5, 7, 9]
    >>> add_consecutive(12321) # [1 + 2 + 3 + 2 + 1]
    [9]
    >>> add_consecutive(4)
    [4]
    >>> add_consecutive(105)
    [1, 5]
    >>> add_consecutive(135797531)
    [1, 3, 5, 7, 9, 7, 5, 3, 1]
    """
    def helper(n, subtotal):
        rest, last = n // 10, n % 10
        subtotal = subtotal + last
        if rest == 0:
            return [subtotal]
        if abs(rest % 10 - last) == 1:
            return helper(rest, subtotal)
        else:
            return helper(rest, 0) + [subtotal]
    return helper(n, 0)
    # def helper(n, subtotal):
    #     rest, last = n // 10, n % 10
    #     subtotal = __________
    #     if __________:
    #         return __________
    #     if __________:
    #         return helper(__________)
    #     else:
    #         return __________
    # return helper(n, __________)

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
