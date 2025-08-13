class CallCounter:
    def __init__(self):
        self.n = 0

    def count(self, f):
        def counted(n):
            self.n += 1
            return f(n)
        return counted
    
def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-2) + fib(n-1)

def memo(f):
    cache = {}
    def memoized(n):
        if n not in cache:
            cache[n] = f(n)
        return cache[n]
    return memoized

def fib_demo():
    c = CallCounter()
    c.n
    fib = c.count(fib)
    fib(30)
    c.n
    fib(30)
    c.n
    fib(35)
    c.n
    
    c.n = 0
    fib(5)
    c.n
    c.n = 0
    fib = memo(fib)
    fib(35)
    c.n
    fib(135)
    fib(535)
    fib(1035)
    c.n
