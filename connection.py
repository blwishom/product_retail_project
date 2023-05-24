import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """
    Creates a database connection at specific location.

    Args:
        db_file: filepath for database file

    Returns:
        Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

if __name__ == "__main__":
    create_connection("product_retail.db")
