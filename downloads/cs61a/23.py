def quiz_question():
    """
    sqlite> SELECT a.name, b.name, c.name FROM dogs AS a, dogs AS b, dogs AS c WHERE a.fur = b.fur AND b.fur = c.fur AND a.name > b.name AND b.name > c.name;
    """

def string_manip():
    """
    sqlite> SELECT a.name || ", " || b.name || ", and " || c.name || " all have " || a.fur || " fur" FROM dogs AS a, dogs AS b, dogs AS c WHERE a.fur = b.fur AND b.fur = c.fur AND a.name > b.name AND b.name > c.name;
    """

def aggregation_demo():
    """
    -- GROUP BY
    sqlite> SELECT * FROM animals;
    sqlite> SELECT legs, COUNT(*) FROM animals GROUP BY legs;
    
    -- Be careful when grouping...
    sqlite> SELECT legs, COUNT(*) FROM animals GROUP BY weight;
    sqlite> SELECT weight, COUNT(*) FROM animals GROUP BY weight;

    sqlite> SELECT * FROM animals WHERE weight = 10;
    
    -- HAVING
    sqlite> SELECT weight, COUNT(*) FROM animals WHERE kind != "cat" GROUP BY weight;
    sqlite> SELECT weight, COUNT(*) FROM animals GROUP BY weight HAVING COUNT(*) < 2;
    sqlite> SELECT weight, COUNT(*) FROM animals WHERE COUNT(*) < 2 GROUP BY weight;
    
    -- Selecting from groups
    sqlite> SELECT weight, COUNT(*), SUM(legs), MAX(legs) FROM animals GROUP BY weight;
    sqlite> SELECT weight, COUNT(*), SUM(legs), MAX(legs), legs FROM animals GROUP BY weight;
    """

def practice_q1():
    """
    -- v1
    sqlite> SELECT * FROM animals AS a, animals AS b;
    sqlite> SELECT * FROM animals AS a, animals AS b WHERE a.weight = b.weight;
    sqlite> SELECT a.legs - b.legs FROM animals AS a, animals AS b WHERE a.weight = b.weight;
    
    -- v2
    sqlite> SELECT weight, COUNT(*), MAX(legs), MIN(legs), MAX(legs) - MIN(legs) FROM animals GROUP BY weight;
    sqlite> SELECT weight, COUNT(*), MAX(legs), MIN(legs), MAX(legs) - MIN(legs) FROM animals GROUP BY weight ORDER BY MAX(legs) - MIN(legs) DESC
    """
