"""
Test Fixture: SQL Injection Safe Patterns (Python)

This file contains SAFE SQL query patterns that should NOT trigger false positives
for SEC-001 rule.

Expected detections: 0 violations (no false positives)
Rule ID: SEC-001
Severity: CRITICAL
"""

import sqlite3
from typing import List, Tuple


# Safe Pattern 1: Parameterized query with ?
def get_user_by_id_safe(user_id: int):
    """SAFE: Parameterized query with ? placeholder"""
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # SAFE - parameterized query
    query = "SELECT * FROM users WHERE id = ?"
    cursor.execute(query, (user_id,))

    return cursor.fetchone()


# Safe Pattern 2: Named parameters
def get_user_by_username_safe(username: str):
    """SAFE: Named parameter query"""
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # SAFE - named parameters
    query = "SELECT * FROM users WHERE username = :username"
    cursor.execute(query, {"username": username})

    return cursor.fetchone()


# Safe Pattern 3: Multiple parameterized values
def search_users_safe(min_age: int, max_age: int, status: str):
    """SAFE: Multiple parameterized values"""
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # SAFE - all user inputs parameterized
    query = """
        SELECT * FROM users
        WHERE age BETWEEN ? AND ?
          AND status = ?
    """
    cursor.execute(query, (min_age, max_age, status))

    return cursor.fetchall()


# Safe Pattern 4: IN clause with parameterized list
def get_users_by_ids_safe(user_ids: List[int]):
    """SAFE: IN clause with proper parameterization"""
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # SAFE - create placeholders dynamically, but values are parameterized
    placeholders = ",".join("?" * len(user_ids))
    query = f"SELECT * FROM users WHERE id IN ({placeholders})"
    cursor.execute(query, user_ids)

    return cursor.fetchall()


# Safe Pattern 5: ORM-style query builder
class UserRepository:
    """SAFE: ORM-style abstraction with parameterization"""

    def __init__(self, connection):
        self.conn = connection

    def find_by_email(self, email: str) -> Tuple:
        """SAFE: Repository pattern with parameters"""
        cursor = self.conn.cursor()

        # SAFE - parameterized through repository
        cursor.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        )

        return cursor.fetchone()

    def update_status(self, user_id: int, status: str) -> None:
        """SAFE: Update with parameterized values"""
        cursor = self.conn.cursor()

        # SAFE - both values parameterized
        cursor.execute(
            "UPDATE users SET status = ? WHERE id = ?",
            (status, user_id)
        )

        self.conn.commit()


# Safe Pattern 6: String constant (no user input)
def get_all_active_users():
    """SAFE: Query with no user input"""
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # SAFE - no user input involved
    query = "SELECT * FROM users WHERE status = 'active'"
    cursor.execute(query)

    return cursor.fetchall()
