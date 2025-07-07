## Logging database Queries
### Objective
### create a decorator that logs database queries executed by any function
-- a decorator log_queries that logs the SQL query before executing the prototype: def log_queries()--
import sqlite3
import functools

## Decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query") or (args[0] if args else None)
        if query:
            print(f"[LOG] Executing SQL Query: {query}")
        else:
            print("[LOG] No SQL query found.")
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

## Fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
print(users)

