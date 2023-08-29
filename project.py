from gui import *
from cs50 import SQL
import sqlite3
from sqlite3 import Error


def main():
    create_database()

    create_gui()


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


if __name__ == "__main__":
    main()
