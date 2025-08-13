# Tracking Instances

class Transaction:
    """A logged transaction.

    >>> s = [20, -3, -4]
    >>> ts = [Transaction(x) for x in s]
    >>> ts[1].balance()
    17
    >>> ts[2].balance()
    13
    """    
    log = []

    def __init__(self, amount):
        self.amount = amount
        self.prior = list(self.log)
        self.log.append(self)

    def balance(self):
        return self.amount + sum([t.amount for t in self.prior])

# getattr

class Account:
    
    interest = 0.02

    def __init__(self, account_holder):
        self.holder = account_holder
        self.balance = 0

    def deposit(self, amount):
        self.balance = self.balance + amount
        return self.balance

    def withdraw(self, amount):
        if amount > self.balance:
            return 'Insufficient funds'
        self.balance = self.balance - amount
        return self.balance

def getattr_demo():
    a = Account('Laryn')
    g = 'holder'
    a.g
    getattr(a, g)
    g
    getattr(a, 'hold' + 'er')


# Close friends

class Friend:
    """A Friend hears from other friends.

    >>> me = Friend('Me')
    >>> friends = [Friend(puff) for puff in ['Blossom', 'Bubbles', 'Buttercup']]
    >>> for i in [2, 2, 0, 1, 2, 0, 2, 1]:
    ...     friends[i].hear_from(me)
    ... 
    >>> me.closest(friends).name
    'Bubbles'
    """
    def __init__(self, name):
        self.name = name
        self.heard_from = {}

    def hear_from(self, friend):
        if friend not in self.heard_from:
            self.heard_from[friend] = 0
        self.heard_from[friend] += 1
        friend.just_messaged = self

    def how_close(self, friend):
        bonus = 0
        if hasattr(self, 'just_messaged') and self.just_messaged == friend:
            bonus = 3
        return friend.heard_from[self] + bonus

    def closest(self, friends):
        return max(friends, key=self.how_close)

# CheckingAccount

class CheckingAccount(Account):
    """A bank account that charges for withdrawals.

    >>> ch = CheckingAccount('Jack')
    >>> ch.balance = 20
    >>> ch.withdraw(5)
    14
    >>> ch.interest
    0.01
    """

    withdraw_fee = 1
    interest = 0.01

    def withdraw(self, amount):
        return Account.withdraw(self, amount + self.withdraw_fee)
        # Alternatively:
        return super().withdraw(amount + self.withdraw_fee)

# Representation

def fractions_demo():
    from fractions import Fraction
    Fraction(2, 3)
    f = Fraction(2, 3)
    print(f)
    f
    repr(f)
    eval('2 + 3')
    eval('Fraction(2, 3)')
    g = eval('Fraction(2, 3)')
    type(g)
    dir(g)
    f
    g
    f == g
    f.numerator
    g.numerator
    str(f)
    eval('2/3')
    type(eval('2/3'))

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

# Class Practice

class Letter:
    def __init__(self, contents):

        self.contents = contents

        self.sent = False

    def send(self):

        if self.sent:

            print(self, 'was already sent.')

        else:
            print(self, 'has been sent.')

            self.sent = True

            return Letter(self.contents.upper())

    def __repr__(self):
        return self.contents


class Numbered(Letter):
   
    number = 0

    def __init__(self, contents):

        super().__init__(contents)
        
        self.number = Numbered.number

        Numbered.number += 1

    def __repr__(self):

        return '#' + str(self.number)
