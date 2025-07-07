## Logging database Queries
### Objective
### create a decorator that logs database queries executed by any function
-- a decorator log_queries that logs the SQL query before executing the prototype: def log_queries()--
import sqlite3
import functools
from datetime import datetime  

## Include timestamp logging

## Decorator to log SQL queries with timestamp
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query") or (args[0] if args else None)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if query:
            print(f"[{timestamp}] Executing SQL Query: {query}")
        else:
            print(f"[{timestamp}] No SQL query provided.")
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

## Fetch users while logging the query with timestamp
users = fetch_all_users(query="SELECT * FROM users")
print(users)

-- Example--

[2025-07-03 14:50:21] Executing SQL Query: SELECT * FROM users
[('001', 'Alice', 'alice@example.com'), ('002', 'Bob', 'bob@example.com')]


