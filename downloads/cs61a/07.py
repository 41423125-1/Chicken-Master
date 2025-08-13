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
    return num_digits_rec(n // 10) + 1

# Streak

def streak(n):
    """Return whether positive n is a dice integer in which all the digits are the same.

    >>> streak(22222)
    True
    >>> streak(4)
    True
    >>> streak(22322)  # 2 and 3 are different digits.
    False
    >>> streak(99999)  # 9 is not allowed in a dice integer.
    False
    >>> streak(505)
    False
    >>> streak(707)
    False
    >>> streak(7070)
    False
    >>> streak(33333333333333)
    True
    """
    return (n >= 1 and n <= 6) or (n > 9 and __________ and streak(__________))
    
# Sevens

def sevens_iter(n, k):
    """Return the (clockwise) position of who says n among k players.

    >>> sevens_iter(2, 5)
    2
    >>> sevens_iter(6, 5)
    1
    >>> sevens_iter(7, 5)
    2
    >>> sevens_iter(8, 5)
    1
    >>> sevens_iter(9, 5)
    5
    >>> sevens_iter(18, 5)
    2
    """
    i, who, direction = 1, 1, 1
    while i < n:
        if i % 7 == 0 or has_seven(i):
            direction = -direction
        who = who + direction
        if who > k:
            who = 1
        if who < 1:
            who = k
        i = i + 1
    return who

def sevens(n, k):
    """Return the (clockwise) position of who says n among k players.

    >>> sevens(2, 5)
    2
    >>> sevens(6, 5)
    1
    >>> sevens(7, 5)
    2
    >>> sevens(8, 5)
    1
    >>> sevens(9, 5)
    5
    >>> sevens(18, 5)
    2
    """
    def f(i, who, direction):
        if i == n:
            return who
        if i % 7 == 0 or has_seven(i):
            direction = -direction
        who = who + direction
        if who > k:
            who = 1
        if who < 1:
            who = k
        return f(i + 1, who, direction)
    return f(1, 1, 1)

def has_seven(n):
    if n == 0:
        return False
    elif n % 10 == 7:
        return True
    else:
        return has_seven(n // 10)

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


### Appendix ###

# Streak Solution:

def streak(n):
    """Return whether positive n is a dice integer in which all the digits are the same.

    >>> streak(22222)
    True
    >>> streak(4)
    True
    >>> streak(22322)  # 2 and 3 are different digits.
    False
    >>> streak(99999)  # 9 is not allowed in a dice integer.
    False
    >>> streak(505)
    False
    >>> streak(707)
    False
    >>> streak(7070)
    False
    >>> streak(33333333333333)
    True
    """
    return (n >= 1 and n <= 6) or (n > 9 and n % 10 == n // 10 % 10 and streak(n // 10))

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
   
