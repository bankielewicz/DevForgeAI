"""Test fixture: Contains SQL injection vulnerability for detection testing."""

import sqlite3


def get_user_by_id_vulnerable(user_id: str) -> dict:
    """VULNERABLE: SQL injection via string concatenation."""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # BAD: String concatenation - SQL injection vulnerability
    query = "SELECT * FROM users WHERE id = " + user_id
    cursor.execute(query)

    result = cursor.fetchone()
    conn.close()
    return result


def search_users_vulnerable(search_term: str) -> list:
    """VULNERABLE: SQL injection via f-string."""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # BAD: f-string interpolation - SQL injection vulnerability
    query = f"SELECT * FROM users WHERE name LIKE '%{search_term}%'"
    cursor.execute(query)

    results = cursor.fetchall()
    conn.close()
    return results


def delete_user_vulnerable(user_id: str) -> None:
    """VULNERABLE: SQL injection in DELETE statement."""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # BAD: format() method - SQL injection vulnerability
    query = "DELETE FROM users WHERE id = {}".format(user_id)
    cursor.execute(query)

    conn.commit()
    conn.close()
