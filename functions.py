import numpy as np
from cs50 import SQL


def check_stability(m, r, j):
    """ "Verify the internal stability of a truss"""

    try:
        if (m > 1 and r > 2 and j > 2) and (m + r) >= 2 * j:
            return True
        else:
            return False
    except ValueError:
        ...
    return False


def globalize(dim, index, arr):
    """Transforms a local stiffness matrix to a global matrix of the entire structure by filling
    the columns and rows that are absent from the index by zeros and return the global matrix.
    """

    temp = np.zeros((dim, dim))
    r = len(index) 

    for i in range(r):
        # Insert the values of the local matrix in the global matrix
        for k in range(r):
            temp[[index[k] - 1], [index[i] - 1]] = arr[[k], [i]]

    return temp

def check_table(tablename):
    """Check if an sql table exists in the database, if yes, removes it."""

    db = SQL("sqlite:///data.db")
    
    # Check if the table has already been created
    test = db.execute("""SELECT name FROM sqlite_master WHERE type="table" AND name=(?);""", tablename)
    if test:
        # Remove the old table
        db.execute("DROP TABLE ?;", tablename)