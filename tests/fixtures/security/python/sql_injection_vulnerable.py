"""
Test Fixture: SQL Injection Vulnerable Patterns (Python)

This file contains 5+ SQL injection vulnerability patterns that MUST be detected by
SEC-001 rule (devforgeai/ast-grep/rules/python/security/sql-injection.yml).

Expected detections: ≥5 violations
Rule ID: SEC-001
Severity: CRITICAL
"""

import sqlite3


# Pattern 1: f-string SQL injection
def get_user_by_id_fstring(user_id: str):
    """VULNERABLE: f-string with user input in SQL"""
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # SEC-001 should detect this
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)

    return cursor.fetchone()


# Pattern 2: .format() SQL injection
def get_user_by_username_format(username: str):
    """VULNERABLE: .format() with user input in SQL"""
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # SEC-001 should detect this
    query = "SELECT * FROM users WHERE username = '{}'".format(username)
    cursor.execute(query)

    return cursor.fetchone()


# Pattern 3: % formatting SQL injection
def delete_user_percent(user_id: int):
    """VULNERABLE: % formatting with user input in SQL"""
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # SEC-001 should detect this
    query = "DELETE FROM users WHERE id = %d" % user_id
    cursor.execute(query)

    conn.commit()


# Pattern 4: String concatenation SQL injection
def search_users_concat(search_term: str):
    """VULNERABLE: String concatenation in SQL"""
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # SEC-001 should detect this
    query = "SELECT * FROM users WHERE name LIKE '%" + search_term + "%'"
    cursor.execute(query)

    return cursor.fetchall()


# Pattern 5: Multi-line f-string SQL injection
def complex_query_fstring(status: str, role: str):
    """VULNERABLE: Multi-line f-string with user input"""
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # SEC-001 should detect this
    query = f"""
        SELECT u.id, u.username, r.role_name
        FROM users u
        JOIN roles r ON u.role_id = r.id
        WHERE u.status = '{status}'
          AND r.role_name = '{role}'
    """
    cursor.execute(query)

    return cursor.fetchall()


# Pattern 6: f-string with WHERE IN clause
def get_users_by_ids_fstring(user_ids: str):
    """VULNERABLE: f-string in WHERE IN clause"""
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # SEC-001 should detect this (user_ids could be "1 OR 1=1")
    query = f"SELECT * FROM users WHERE id IN ({user_ids})"
    cursor.execute(query)

    return cursor.fetchall()
