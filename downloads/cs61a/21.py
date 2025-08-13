# Project 4: Scheme Interpreter

def scheme_eval_apply_demos():
    """
    # CAREFULLY Add @trace to scheme_eval
    scm> (define (f x) (* x x))
    f
    scm> (f 4)
    16
    scm> (define x 1)
    x
    scm> (if (= (f 4) 17) (/ 1 0) x)
    1
    """

# Referential Transparency

def one(lst):
    lst[0] += 1
    return 1

def get_first(lst):
    return lst[0]

lst = [1, 2, 3]
from operator import add
add(get_first(lst), one(lst))

lst = [1, 2, 3]
add(one(lst), get_first(lst))

# Tail Recursion Techniques

def fib_iter(n):
    if n <= 1:
        return n
    prev1, prev2 = 0, 1
    k = 1
    while k < n:
        prev1, prev2 = prev1 + prev2, prev1
        k += 1
    return prev1 + prev2
