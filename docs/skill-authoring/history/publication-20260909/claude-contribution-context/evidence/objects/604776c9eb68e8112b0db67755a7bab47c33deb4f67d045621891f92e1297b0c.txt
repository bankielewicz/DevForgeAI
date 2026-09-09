import sqlite3

def save_and_list(name):
    connection = sqlite3.connect(":memory:")
    try:
        connection.execute("CREATE TABLE notes (name TEXT NOT NULL)")
        connection.execute("INSERT INTO notes VALUES (?)", (name,))
        return [row[0] for row in connection.execute("SELECT name FROM notes")]
    finally:
        connection.close()
