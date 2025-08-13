# DRY

def same_length(a, b):
    """Return whether positive integers a and b have the same number of digits.

    >>> same_length(50, 70)
    True
    >>> same_length(50, 100)
    False
    >>> same_length(1000, 100000)
    False
    """
    return digits(a) == digits(b)
    # a_digits = 0
    # while a > 0:
    #     a = a // 10
    #     a_digits = a_digits + 1
    # b_digits = 0
    # while b > 0:
    #     b = b // 10
    #     b_digits = b_digits + 1
    # return a_digits == b_digits

def digits(n):
    n_digits = 0
    while n > 0:
        n = n // 10
        n_digits = n_digits + 1
    return n_digits

# Functions as Arguments

## Summation Example
def fib(n):
    pred, curr = 0, 1
    k = 1
    while k < n:
        pred, curr = curr, pred + curr
        k = k + 1
    return curr

## Attempt 1:
def sum_cubes(n):
    """Sum the first N cubes of natural numbers.
    
    >>> sum_cubes(5) # 1 + 8 + 27 + 64 + 125
    225
    """
    total, k = 0, 1
    while k <= n:
        total, k = total + pow(k, 3), k + 1
    return total

def sum_fibs(n):
    """Sum the first N fibonacci numbers.
    
    >>> sum_fibs(5) # 1 + 1 + 2 + 3 + 5 
    12
    """
    total, k = 0, 1
    while k <= n:
        total, k = total + fib(k), k + 1
    return total


## Attempt 2:
def summation(n, term):
    total, k = 0, 1
    while k <= n:
        total, k = total + term(k), k + 1
    return total

def cube(n):
    return pow(n, 3)

def sum_fibs(n):
    summation(n, fib)
    
def sum_cubes(n):
    summation(n, cube)

# Nim

# 20: L
# 17,18,19: W
# 16: L
# 13,14,15: W
# 12: L
# 9,10,11: W
# 8: L
# 5,6,7: W
# 4: L
# 1,2,3: W
# 0: L

def play(strategy0, strategy1, goal=21):
    """Play twenty-one and print the winner.
    
    >>> play(two_or_three, two_or_three)
    Player 1 wins!
    """
    n = 0
    who = 0  # Player 0 goes first
    while n < goal:
        if who == 0:
            n = n + strategy0(n)
            who = 1
        elif who == 1:
            n = n + strategy1(n)
            who = 0
    print('Player', who, 'wins!') # The player who didn't just add to n

def two_or_three(n):
    if n < 10:
        return 3
    else:
        return 2

def interactive(n):
    print('How much do you want to add to', n, '(1-3)?')
    choice = int(input())
    return choice

# play(two_or_three, interactive)

# Functions as Return Values

def make_adder(n):
    """Return a function that takes one argument K and returns K + N.

    >>> add_three = make_adder(3)
    >>> add_three(4)
    7
    """
    def adder(k):
        return k + n
    return adder

"""
>>> 2 + 3
5
>>> f = make_adder(2)
>>> f(4)
6
>>> f(5)
7
>>> def g(x):
...      return 100 + x
...
>>> g(1)
101
>>> g(2)
102
>>> g2 = make_adder(100)
>>> g2(1)
101
>>> g2(2)
102
>>> # slides
>>> adder(1)
Error
>>> f
Function: adder
"""

# Using Functions as Arguments & Functions as Return Values in Nim
def noisy(who, strat):
    def noisier(n):
        print('Player', who, 'got number', n)
        return strat(n)
    return noisier

# play(noisy(0, two_or_three), noisy(1, interactive))

# Extra
import random
def winning_strat(n):
    if n % 4 == 0:
        return random.choice([1, 2, 3])
    else:
        return 4 - (n % 4)

def random_strat(n):
    return random.choice([1, 2, 2])

# play(random_strat, winning_strat)
# play(interactive, winning_strat)
