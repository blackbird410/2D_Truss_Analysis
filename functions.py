import numpy as np
from cs50 import SQL
import sqlite3
from sqlite3 import Error


def create_database():
    """Create a Sqlite database"""

    create_connection(r"data.db")
    db = SQL("sqlite:///data.db")
    db.execute(
        """CREATE TABLE IF NOT EXISTS nodes (
                id INTEGER PRIMARY KEY NOT NULL UNIQUE, 
                x INTEGER NOT NULL, 
                y INTEGER NOT NULL, 
                rx INTEGER NOT NULL, 
                ry INTEGER NOT NULL);"""
    )
    db.execute(
        """CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY NOT NULL, 
                start_node INTEGER NOT NULL, 
                end_node INTEGER NOT NULL, 
                section_area FLOAT NOT NULL, 
                young_mod FLOAT NOT NULL, 
                inertia FLOAT NOT NULL, 
                FOREIGN KEY(start_node) REFERENCES nodes (id), 
                FOREIGN KEY(end_node) REFERENCES nodes (id));"""
    )
    db.execute(
        """CREATE TABLE IF NOT EXISTS loads (
                id INTEGER PRIMARY KEY NOT NULL, 
                x_load FLOAT NOT NULL, 
                y_load FLOAT NOT NULL, 
                node INTEGER NOT NULL UNIQUE, 
                FOREIGN KEY(NODE) REFERENCES nodes(id));"""
    )


def create_connection(db_file):
    """Create a database connection to a SQLite database"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


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