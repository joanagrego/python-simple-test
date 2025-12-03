"""
Database module with intentional SQL injection vulnerabilities
Similar to the Node.js SQLite example but for Python
"""

import sqlite3

# VULNERABILITY: Database connection with no encryption
conn = sqlite3.connect(':memory:', check_same_thread=False)
cursor = conn.cursor()

# Initialize database
cursor.execute('''
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        role TEXT DEFAULT 'user'
    )
''')

# Seed data
cursor.execute("INSERT INTO items (id, name) VALUES (1, 'Item 1')")
cursor.execute("INSERT INTO items (id, name) VALUES (2, 'Item 2')")
cursor.execute("INSERT INTO items (id, name) VALUES (3, 'Item 3')")

# Seed users (passwords should be hashed in production)
cursor.execute("INSERT INTO users (username, password, role) VALUES ('admin', 'admin123', 'admin')")
conn.commit()


# VULNERABILITY: SQL Injection - String concatenation
def get_item_by_name(name):
    # VULNERABILITY: Direct string interpolation
    query = f"SELECT * FROM items WHERE name = '{name}'"
    cursor.execute(query)
    return cursor.fetchone()


# VULNERABILITY: SQL Injection in search
def search_items(search_term):
    # VULNERABILITY: String concatenation in LIKE clause
    query = f"SELECT * FROM items WHERE name LIKE '%{search_term}%'"
    cursor.execute(query)
    return cursor.fetchall()


# VULNERABILITY: SQL Injection in login
def authenticate_user(username, password):
    # VULNERABILITY: Classic SQL injection in authentication
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    return cursor.fetchone()


# VULNERABILITY: SQL Injection in ORDER BY
def get_items_sorted(sort_column):
    # VULNERABILITY: Unvalidated column name in ORDER BY
    query = f"SELECT * FROM items ORDER BY {sort_column}"
    cursor.execute(query)
    return cursor.fetchall()


# VULNERABILITY: SQL Injection via bulk insert
def bulk_insert_items(items):
    values = ', '.join([f"({item['id']}, '{item['name']}')" for item in items])
    # VULNERABILITY: String interpolation for bulk insert
    query = f"INSERT INTO items (id, name) VALUES {values}"
    cursor.execute(query)
    conn.commit()
    return {'inserted': len(items)}


# VULNERABILITY: Second-order SQL injection
def update_item_name(item_id, new_name):
    # VULNERABILITY: Even though id is parameterized, new_name is not
    query = f"UPDATE items SET name = '{new_name}' WHERE id = ?"
    cursor.execute(query, (item_id,))
    conn.commit()
    return {'updated': True}


# Safe version for comparison (parameterized query)
def get_item_by_id_safe(item_id):
    cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
    return cursor.fetchone()
