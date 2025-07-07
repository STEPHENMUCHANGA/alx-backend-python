## Handle Database Connections with a Decorator
### Objective
### create a decorator that automatically handles opening and closing database connections
-- the script below by Implementing a decorator with_db_connection that opens a database connection, passes it to the function and closes it afterword--
import sqlite3
import functools

## Decorator to manage DB connection
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            # Pass the connection as the first argument to the function
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

## Fetch user by ID with automatic connection handling
user = get_user_by_id(user_id=1)
print(user)

