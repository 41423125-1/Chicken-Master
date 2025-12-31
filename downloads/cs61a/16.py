class Link:
    """A linked list.

    >>> s = Link(3, Link(4, Link(5)))
    >>> s
    Link(3, Link(4, Link(5)))
    >>> print(s)
    <3 4 5>
    >>> s.first
    3
    >>> s.rest
    Link(4, Link(5))
    >>> s.rest.first
    4
    >>> s.rest.first = 7
    >>> s
    Link(3, Link(7, Link(5)))
    >>> s.first = 6
    >>> s.rest.rest = Link.empty
    >>> s
    Link(6, Link(7))
    >>> print(s)
    <6 7>
    >>> print(s.rest)
    <7>
    >>> t = Link(1, Link(Link(2, Link(3)), Link(4)))
    >>> t
    Link(1, Link(Link(2, Link(3)), Link(4)))
    >>> print(t)
    <1 <2 3> 4>
    """
    empty = ()

    def __init__(self, first, rest=empty):
        assert rest is Link.empty or isinstance(rest, Link)
        self.first = first
        self.rest = rest

    def __repr__(self):
        if self.rest:
            rest_repr = ', ' + repr(self.rest)
        else:
            rest_repr = ''
        return 'Link(' + repr(self.first) + rest_repr + ')'

    def __str__(self):
        string = '<'
        while self.rest is not Link.empty:
            string += str(self.first) + ' '
            self = self.rest
        return string + str(self.first) + '>'

def link_demo():
    s = Link(4, Link(6, Link(8, Link(10))))
    print(s)
    s
    print(s.rest)
    s.first
    s.rest
    
    s.rest.first = 12
    print(s)
    s.rest
    s.rest.first
    
    t = s.rest.rest
    print(t)
    s
    t.first = 16
    t
    s
    s.rest.rest is t
    
    s = Link(1, Link(Link(2, Link(3)), Link(4)))
    print(s)
    s
    [1, [2, 3], 4]
    s
    s.first
    s.rest.first
    t = s.rest.first
    t
    print(t)
    t.rest.rest = Link(5)
    print(t)
    t
    s.rest.first
    print(s)
    
    # How to get the 4?
    print(s)
    s
    s.rest
    s.rest.rest
    s.rest.rest.first
    
    # How to get the 5?
    s
    s.rest
    s.rest.first
    s.rest.first.rest
    s.rest.first.rest.rest
    s.rest.first.rest.rest.first

def double(s, v):
    """Insert another v after each v in s.

    >>> s = [2, 7, 1, 8, 2, 8]
    >>> double(s, 8)
    >>> s
    [2, 7, 1, 8, 8, 2, 8, 8]
    """
    i = 0
    while i < len(s):
        if s[i] == v:
            s.insert(i+1, v)
            i += 2
        else:
            i += 1

def double_link(s, v):
    """Insert another v after each v in s.

    >>> s = Link(2, Link(7, Link(1, Link(8, Link(2, Link(8))))))
    >>> double_link(s, 8)
    >>> print(s)
    <2 7 1 8 8 2 8 8>
    """
    while s is not Link.empty:
        if s.first == v:
            s.rest = Link(v, s.rest)
            s = s.rest.rest
        else:
            s = s.rest
