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

def sqlite_demos():
    """
    $ sqlite3 -init 22.sql
    sqlite> .mode columns
    sqlite> SELECT * FROM parents;
    """

def join_demos():
    """
    $ sqlite3 -init 22.sql
    sqlite> .mode columns
    sqlite> SELECT * FROM parents;
    sqlite> SELECT * FROM dogs;
    sqlite> SELECT * FROM parents, dogs;
    sqlite> SELECT * FROM parents JOIN dogs;
    
    -- find the useful, coherent rows
    sqlite> SELECT * FROM parents, dogs WHERE child=name;
    
    sqlite> SELECT * FROM parents, dogs WHERE child=name AND fur="curly";
    sqlite> SELECT parent FROM parents, dogs WHERE child=name AND fur="curly";
    
    -- careful...
    sqlite> SELECT parent, fur FROM parents, dogs WHERE child=name AND fur="curly";
    sqlite> SELECT * FROM dogs;
    """

def quiz_question():
    """
    sqlite> SELECT a.name, b.name, c.name FROM dogs AS a, dogs AS b, dogs AS c WHERE a.fur = b.fur AND b.fur = c.fur AND a.name > b.name AND b.name > c.name;
    """

def string_manip():
    """
    sqlite> SELECT a.name || ", " || b.name || ", and " || c.name || " all have " || a.fur || " fur" FROM dogs AS a, dogs AS b, dogs AS c WHERE a.fur = b.fur AND b.fur = c.fur AND a.name > b.name AND b.name > c.name;
    """
