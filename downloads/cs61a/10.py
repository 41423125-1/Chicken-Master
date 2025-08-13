from tree import *

def count_nodes(t):
    """
    >>> count_nodes(tree(1))
    1
    >>> count_nodes(tree(1, [tree(2)]))
    2
    >>> t = tree(3, [tree(-1), tree(2, [tree(4, [tree(1)]), tree(3)]), tree(1, [tree(-1)])])
    >>> print_tree(t) 
    3
      -1
      2
        4
          1
        3
      1
        -1
    >>> count_nodes(t)
    8
    """
    if is_leaf(t):
        return 1
    else:
        return 1 + sum([count_nodes(b) for b in branches(t)])

def list_demos():
    x = 4
    y = x
    y
    x = 5
    y
    s = [3, 3, 7, 9]
    u = s
    s[1] = 5
    s
    u
    s.append(11)

    t = [x+3 for x in s]
    t
    s
    u
    for i in range(len(s)):
        s[i] = s[i] + 3
    s
    u
    t

    [s[-(i+1)] for i in range(len(s))]
    s
    for i in range(len(s)):
        s[i] = s[-(i+1)]
    s
    
    s = [13, 15, 17, 19]
    v = [0, 0, 0, 0]
    for i in range(len(s)):
        v[i] = s[-(i+1)]
    v

def list_of_lists_demo():
    s = [1, [2, 3], 4]
    t = s[1]
    t[1] = s
    print(s)
    
def list_of_lists_demo_v2():
    s = [1, [2, 3], 4]
    t = s[1]
    u = [t, 5]
    u.append(6)
    u[0].append(7)
    t[1] = 8
    print(s)
    print(t)
    print(u)

def list_lists_demo_v2_modified():
    s = [1, [2, 3], 4]
    t = s[1]
    u = [list(t), 5]
    u.append(6)
    u[0].append(7)
    t[1] = 8
    print(s)
    print(t)
    print(u)

def sums(n, m):
    """Return lists that sum to n containing positive numbers up to m that
    have no adjacent repeats, for n > 0 and m > 0.

    >>> sums(5, 1)
    []
    >>> sums(5, 2)
    [[2, 1, 2]]
    >>> sums(5, 3)
    [[1, 3, 1], [2, 1, 2], [2, 3], [3, 2]]
    >>> sums(5, 5)
    [[1, 3, 1], [1, 4], [2, 1, 2], [2, 3], [3, 2], [4, 1], [5]]
    >>> sums(6, 3)
    [[1, 2, 1, 2], [1, 2, 3], [1, 3, 2], [2, 1, 2, 1], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
    """
    result = []
    for k in range(1, min(m + 1, n)):
        for rest in sums(n-k, m):
            if rest[0] != k:
                result.append([k] + rest)
    if n <= m:
        result.append([n])
    return result

def identity_demos():
    a = [10]
    b = a
    a == b
    a is b
    a.extend([20, 30])
    print(a)
    print(b)
    a == b
    a is b
    
    a = [10]
    b = [10]
    a == b
    a is not b
    a.append(20)
    print(a)
    print(b)
    a != b

    s = [3, 5, 7]
    t = [9, 11]
    s.append(t)
    s.extend(t)
    t[1] = 13
    print(s)

def mutation_and_names():
    s = [2, 7, [1, 8]]
    t = s[2]
    t.append([2])
    e = s + t
    t[2].append(8)
    print(e)
    e[2][2] is e[-1]
