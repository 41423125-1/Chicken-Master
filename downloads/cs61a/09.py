# Dictionaries

"""
d = {3: 9, 4: 4 * 4, 16: 16 * 15}
d
d[3]
d[4]
d[16]
d[12]
d[16]
d[9]
for k in d.keys():
    print(k, 'is the key for', d[k])
{k: k * k for k in [3, 4, 16]}
"""

# Dictionary Comprehension Example

def multiples(s, factors):
    """Create a dictionary where each factor is a key and each value 
    is the elements of s that are multiples of the key.
    
    >>> multiples([3, 4, 5, 6, 7, 8], [2, 3])
    {2: [4, 6, 8], 3: [3, 6]}
    >>> multiples([1, 2, 3, 4, 5], [2, 5, 8])
    {2: [2, 4], 5: [5], 8: []}
    """
    # return {x: [y for y in s if y % x == 0] for x in factors}
    return {x: [y for y in ________ if ___________] for x in ________}

# Data Abstraction

def line(slope, intercept):
    # return lambda x: slope * x + intercept
    # return {'slope': slope, 'intercept': intercept}
    return [slope, intercept]

def slope(f):
    # return f(1) - f(0)
    # return f['slope']
    return f[0]

def y_intercept(f):
    # return f(0)
    # return f['intercept']
    return f[1]

###===--- Abstraction Barrier ---===###

def parallel(f, g):
    """Whether lines f and g are parallel.

    >>> parallel(line(3, 5), line(3, 2))
    True
    >>> parallel(line(3, 5), line(2, 3))
    False
    """
    return slope(f) == slope(g)

# Trees

def tree(label, branches=[]):
    for branch in branches:
        assert is_tree(branch), 'branches must be trees'
    return [label] + list(branches)

def label(tree):
    return tree[0]

def branches(tree):
    return tree[1:]

def is_tree(tree):
    if type(tree) != list or len(tree) < 1:
        return False
    for branch in branches(tree):
        if not is_tree(branch):
            return False
    return True

def is_leaf(tree):
    return not branches(tree)

def print_tree(t, indent=0):
    """Print a representation of this tree in which each label is
    indented by two spaces times its depth from the root.

    >>> print_tree(tree(1))
    1
    >>> print_tree(tree(1, [tree(2)]))
    1
      2
    >>> print_tree(fib_tree(4))
    3
      1
        0
        1
      2
        1
        1
          0
          1
    """
    print('  ' * indent + str(label(t)))
    for b in branches(t):
        print_tree(b, indent + 1)

### +++ === ABSTRACTION BARRIER === +++ ###

t = tree(1, 
         [tree(9, [
             tree(2, [
                 tree(5, [
                     tree(6), 
                     tree(7)]), 
                 tree(8), 
                 tree(3)]), 
             tree(4)])])

"""
t
print_tree(t)
len(branches(t))
b = branches(t)[0]
print_tree(b)
len(branches(b))
c = branches(b)[0]
print_tree(c)
len(branches(c))
"""

# the number 4 is...
  # the label of ...
  # the branch at index 1 of ...
  # the branch at index 0 of ...
  # the tree t
"""
print_tree(t)
"""
label(branches(branches(t)[0])[1])
# t[1][2][0] # DON'T WRITE THAT!!

# Tree Processing Example

def largest_label(t):
    """Return the largest label in tree t.

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
    >>> largest_label(t)
    4
    """
    if is_leaf(t):
        return label(t)
    else:
        return max([label(t)] + [largest_label(b) for b in branches(t)])

def largest_label(t):
    """Return the largest label in tree t."""
    if is_leaf(t):
        return __________
    else:
        return ____([_________________ for b in branches(t)] + ___________)
