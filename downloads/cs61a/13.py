class Account:
    """An account has a balance and a holder.

    >>> a = Account('John')
    >>> a.holder
    'John'
    >>> a.deposit(100)
    100
    >>> a.withdraw(90)
    10
    >>> a.withdraw(90)
    'Insufficient funds'
    >>> a.balance
    10
    """
    def __init__(self, account_holder):
        self.holder = account_holder
        self.balance = 0

    def deposit(self, amount):
        """Add amount to balance."""
        self.balance = self.balance + amount
        return self.balance

    def withdraw(self, amount):
        """Subtract amount from balance if funds are available."""
        if amount > self.balance:
            return 'Insufficient funds'
        self.balance = self.balance - amount
        return self.balance

def account_demo():
    a = Account('Laryn')
    b = Account('Larry')
    a.deposit(10)
    a.deposit(10)
    a.deposit(10)
    b.balance
    b.deposit(10000000000)
    a.balance
    b.balance
    b.holder
    a.holder
    balance # Error
    withdraw # Error
    a.password = '123456789'
    a.balance += 1000
    b.balance = 0

def transfer(source, destination, amount):
    """Transfer amount between two accounts.

    >>> john = Account('John')
    >>> jack = Account('Jack')
    >>> john.deposit(100)
    100
    >>> jack.deposit(100000)
    100000
    >>> transfer(jack, john, 1000)
    'Transfer successful'
    >>> john.balance
    1100
    >>> jack.balance
    99000
    >>> transfer(john, jack, 10000)
    'Insufficient funds'
    >>> transfer(john, jack, 10)
    'Transfer successful'
    >>> john.balance
    1090
    >>> jack.balance
    99010
    """
    result = source.withdraw(amount)
    if type(result) == str:  # something went wrong
        return result
    else:
        destination.deposit(amount)
        return 'Transfer successful'

def create(names):
    """Creates a dictionary of accounts, each with an initial deposit of 5.

    >>> accounts = create(['Alice', 'Bob', 'Charlie'])
    >>> accounts['Alice'].holder
    'Alice'
    >>> accounts['Bob'].balance
    5
    >>> accounts['Charlie'].deposit(10)
    15
    """
    result = {name: Account(name) for name in names}
    for a in result.values():
        a.deposit(5)
    return result

# Method Calls

def dot_expr_demo():
    t = Account('Tom')
    t.deposit(10)
    t.withdraw(2)
    t.withdraw(2)
    f = t.withdraw
    f(2)
    u = Account('someone else')
    u.deposit(100)
    u.balance
    f(2)
    f(2)
    u.balance
    t.balance
    
    # Functions vs Bound Methods
    t.deposit(10)
    t.balance
    Account.withdraw
    t.withdraw
    f = t.withdraw
    f(2)
    g = Account.withdraw
    g(2)
    Account.withdraw(t, 3)
    g(t, 1)
    f(1)
    t.balance
    
    # Classes as Values
    Account
    c = Account
    c('Laryn')
    def make_two_instances(some_type, name):
        return [some_type(name), some_type(name)]
    two_accounts = make_two_instances(Account, 'Laryn')
    two_accounts[0].balance
    two_accounts[0].deposit(1)
    two_accounts[0].balance
    two_accounts[1].balance

# Class Attributes
class Account:
    """An account has a balance and a holder.

    >>> a = Account('John')
    >>> a.holder
    'John'
    >>> a.deposit(100)
    100
    >>> a.withdraw(90)
    10
    >>> a.withdraw(90)
    'Insufficient funds'
    >>> a.balance
    10
    """
    interest = 0.02
    def __init__(self, account_holder):
        self.holder = account_holder # instance attribute
        self.balance = 0
        
def class_attr_demo():
    a = Account('Laryn')
    a.holder
    a.balance
    a.interest
    
# Waldo
class Town:
    def __init__(self, w, aldo):
        if aldo == 7:
            self.street = {self.f(w): 'Waldo'}
    
    def f(self, x):
        return x + 1

def town_demo():
    Town(7)
    Town(0, 7)
    Town(0, 7).street
    Town(0, 6).street
    Town(0, 7).street
    Town(0, 7).street[1]
    Town(2, 7).street[3]
    x = 100
    Town(x, 7).street[x + 1]

class Beach:
    def __init__(self):
        sand = ['Wal', 'do']
        self.dig = sand.pop

    def walk(self, x):
        self.wave = lambda y: self.dig(x) + self.dig(y)
        return self

def beach_demo():
    f = [3, 4, 5].pop
    f
    f(0)
    f(0)
    f(0)
    f(0)
    a = Beach()
    a.sand
    sand
    a.dig
    a.dig(0)
    a.dig(0)
    
    # Solution
    a = Beach()
    walk_return_value = a.walk(0)
    type(walk_return_value)
    a.wave
    b = Beach()
    b.wave
    a.wave(0)

    Beach().walk(0).wave(0)
