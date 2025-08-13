# Environment Diagrams

def sweet(x, y):
    def dreams(z, f):
        return f(z)

    while x + y > 0:
        y = y - dreams(x + 2, lambda x: x - y)

    return x + y

a = 1
b = 2
a = sweet(a, b)







# Tree Recursion

def remove_person(people, to_remove):
    return [person for person in people if person != to_remove]

def movie_seating(people, seats):
    """
    >>> movie_seating(['L', 'R'], [0, 0])
    [['L', 'R'], ['R', 'L']]
    >>> movie_seating(['L', 'C'], [0, -1, 0])
    [['L', -1, 'C'], ['C', -1, 'L']]
    >>> movie_seating(['L', 'R', 'C'], [0, -1, 0])
    []
    >>> movie_seating(['L', 'R', 'C'], [0, 0, 0])
    [['L', 'R', 'C'], ['L', 'C', 'R'], ['R', 'L', 'C'], ['R', 'C', 'L'], ['C', 'L', 'R'], ['C', 'R', 'L']]
    >>> movie_seating(['R', 'C'], [0, 0, 0])
    [['R', 'C', 0], ['R', 0, 'C'], ['C', 'R', 0], ['C', 0, 'R'], [0, 'R', 'C'], [0, 'C', 'R']]
    """
    if not seats and people:
        return []
    if not people:
        return [seats]
    skip_first_seat = __________
    if seats[0] == -1:
        return [__________ for arrangement in skip_first_seat]
    else:
        ways = []
        for choice in people:
            use_first_seat = __________
            ways.__________([__________ for arrangement in use_first_seat])
        ways.__________([__________ for arrangement in skip_first_seat])
        return ways









# OOP + Linked Lists

class Browser:
    """
    >>> browser = Browser()
    >>> print(browser)

    >>> _ = browser.visit('cs61a.org')
    >>> _ = browser.visit('oh.cs61a.org')
    >>> print(browser)
    oh.cs61a.org<-cs61a.org
    >>> undo = browser.back()
    >>> print(browser)
    cs61a.org
    >>> undo = undo()
    >>> print(browser)
    oh.cs61a.org<-cs61a.org
    >>> undo = undo()
    >>> print(browser)
    cs61a.org
    >>> _ = undo()() # undo'ing an undo cancels it out and does nothing
    >>> print(browser)
    cs61a.org
    """
    
    def __init__(self):
        self.browsing_history = Link.empty
        
    def visit(self, page):
        self.browsing_history = __________
        return __________
    
    def back(self):
        page = self.browsing_history.first
        self.browsing_history = __________
        return __________
        
    def __str__(self):
        display = ''
        head = self.browsing_history
        while head is not Link.empty:
            if __________ is not Link.empty:
                display += __________
            else:
                display += __________
            head = head.rest
        return display
        
class Chrome(Browser):
    """
    >>> browser = Chrome()
    >>> _ = browser.visit('cs61a.org')
    >>> _ = browser.visit('tutor.cs61a.org')
    >>> _ = browser.visit('go.cs61a.org')
    >>> browser2 = Chrome()
    >>> _ = browser2.visit('cs61a.org')
    >>> _ = browser2.visit('sections.cs61a.org')
    >>> _ = browser2.visit('code.cs61a.org')
    >>> _ = browser2.visit('oh.cs61a.org')
    >>> print(browser)
    go.cs61a.org<-tutor.cs61a.org<-cs61a.org<-google.com
    >>> print(browser2)
    oh.cs61a.org<-code.cs61a.org<-sections.cs61a.org<-cs61a.org<-google.com
    >>> browser.interleave_histories(browser2)
    >>> print(browser)
    go.cs61a.org<-oh.cs61a.org<-tutor.cs61a.org<-code.cs61a.org<-cs61a.org<-sections.cs61a.org<-google.com<-cs61a.org<-google.com
    >>> browser.browsing_history is browser2.browsing_history
    True
    """

    def __init__(self):
        self.browsing_history = __________
        
    def interleave_histories(self, other):
        head = self.browsing_history
        other_head = other.browsing_history
        while head is not Link.empty and other_head is not Link.empty: # was 2 blanks
            head.rest, head, other_head = __________, __________, __________
        other.browsing_history = self.browsing_history

class MemorySaverBrowser(__________):
    """
    >>> browser = MemorySaverBrowser(2)
    >>> _ = browser.visit('cs61a.org')
    >>> _ = browser.visit('cs61bl.org')
    >>> print(browser)
    cs61bl.org<-cs61a.org
    >>> _ = browser.visit('cs61c.org')
    >>> print(browser)
    cs61c.org<-cs61bl.org
    >>> _ = browser.back()
    >>> print(browser)
    cs61bl.org
    >>> undo = browser.visit('eecs70.org')
    >>> print(browser)
    eecs70.org<-cs61bl.org
    >>> _ = undo()
    >>> print(browser)
    cs61bl.org
    """
    
    def __init__(self, limit):
        __________ # you may not use `=`
        self.limit = limit
        self.history_length = 0
        
    def visit(self, page):
        if self.history_length == self.limit:
            head = self.browsing_history
            while __________ is not Link.empty:
                head = __________
            __________
        else:
            self.history_length = __________
        return __________
    
    def back(self):
        __________
        return __________
