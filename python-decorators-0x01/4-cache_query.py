## Using decorators to cache Database Queries
### Objective
### create a decorator that caches the results of a database queries inorder to avoid redundant calls
--  the code below by implementing a decorator cache_query(func) that caches query results based on the SQL query string--
import time
import sqlite3 
import functools

## Simple in-memory cache
query_cache = {}

## Decorator to manage DB connection
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

## Decorator to cache query results based on the SQL query string
def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        query = kwargs.get("query") or (args[0] if args else None)
        if query in query_cache:
            print("[CACHE] Returning cached result for query.")
            return query_cache[query]
        
        result = func(conn, *args, **kwargs)
        query_cache[query] = result
        print("[CACHE] Caching new result for query.")
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

## First call will execute and cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")
print(users)

## Second call will return the result from cache
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print(users_again)

