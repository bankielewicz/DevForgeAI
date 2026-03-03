"""Test fixture: Clean code with no security vulnerabilities."""

import sqlite3
from typing import Optional


def get_user_by_id_safe(user_id: int) -> Optional[dict]:
    """SAFE: Uses parameterized query to prevent SQL injection."""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # GOOD: Parameterized query - no SQL injection possible
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))

    result = cursor.fetchone()
    conn.close()
    return result


def search_users_safe(search_term: str) -> list:
    """SAFE: Uses parameterized query with wildcards."""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # GOOD: Parameterized query with LIKE
    cursor.execute(
        "SELECT * FROM users WHERE name LIKE ?",
        (f"%{search_term}%",)
    )

    results = cursor.fetchall()
    conn.close()
    return results


def create_user_safe(name: str, email: str) -> int:
    """SAFE: Uses parameterized INSERT statement."""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # GOOD: Parameterized insert
    cursor.execute(
        "INSERT INTO users (name, email) VALUES (?, ?)",
        (name, email)
    )

    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return user_id
