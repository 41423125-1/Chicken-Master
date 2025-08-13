# Representation

# Bear

class Bear:
    "a bear"

def print_bear():
    oski = Bear()
    print('str:', str(oski))
    print('repr:', repr(oski))

# Bear 2

class Bear:

    def __repr__(self): # class attribute
        return 'Bear()'

    def __str__(self): # class attribute
        return 'a bear'

# Mutable Trees

from tree import *
class Tree:
    """A tree is a label and a list of branches."""
    def __init__(self, label, branches=[]):
        self.label = label
        for branch in branches:
            assert isinstance(branch, Tree)
        self.branches = list(branches)

    def __repr__(self):
        if self.branches:
            branch_str = ', ' + repr(self.branches)
        else:
            branch_str = ''
        return 'Tree({0}{1})'.format(repr(self.label), branch_str)

    def __str__(self):
        return '\n'.join(self.indented())

    def indented(self):
        lines = []
        for b in self.branches:
            for line in b.indented():
                lines.append('  ' + line)
        return [str(self.label)] + lines

    def is_leaf(self):
        return not self.branches

def fib_tree(n):
    """A Fibonacci tree.

    >>> print(fib_tree(4))
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
    if n == 0 or n == 1:
        return Tree(n)
    else:
        left = fib_tree(n-2)
        right = fib_tree(n-1)
        fib_n = left.label + right.label
        return Tree(fib_n, [left, right])

def make_even(t):
    """Mutate t such that every odd label is made even by adding 1.

    >>> t1 = Tree(3, [Tree(4, [Tree(5), Tree(6)]), Tree(4, [Tree(5), Tree(5)])])
    >>> print(t1)
    3
      4
        5
        6
      4
        5
        5
    >>> make_even(t1)
    >>> print(t1)
    4
      4
        6
        6
      4
        6
        6
    """
    t.label += t.label % 2
    for b in t.branches:
        make_even(b)

def largest_of_subtree(t):
    """Mutate t such that the label of each node is the largest of all the labels in the subtree rooted at that node.

    >>> t1 = Tree(3, [Tree(4, [Tree(5), Tree(6)]), Tree(4, [Tree(5), Tree(5)])])
    >>> print(t1)
    3
      4
        5
        6
      4
        5
        5
    >>> largest_of_subtree(t1)
    >>> print(t1)
    6
      6
        5
        6
      5
        5
        5
    """
    for b in t.branches:
        largest_of_subtree(b)
    t.label = max([b.label for b in t.branches] + [t.label])

def keep_k_largest(t, k):
    """Mutate t such that each node has no more than k branches. Keep the k branches with the largest root labels.
    Assume the labels of t are unique.

    >>> t1 = Tree(3, [Tree(4, [Tree(5), Tree(6)]), Tree(7, [Tree(8), Tree(9)])])
    >>> print(t1)
    3
      4
        5
        6
      7
        8
        9
    >>> keep_k_largest(t1, 1)
    >>> print(t1)
    3
      7
        9
      
    """
    while len(t.branches) > k:
        smallest_branch = min(t.branches, key=lambda b: b.label)
        t.branches.remove(smallest_branch)
    for b in t.branches:
        keep_k_largest(b, k)
