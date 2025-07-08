## Reusable Query Context Manager
### Objective
### create a reusable context manager that takes a query as input and executes it, managing both connection and the query execution
--Implementing a class based custom context manager ExecuteQuery that takes the query: ”SELECT * FROM users WHERE age > ?” and the parameter 25 and returns the result of the query--
--using the__enter__() and the __exit__() methods-- 
import sqlite3

class ExecuteQuery:
    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params or [])
        return self.cursor.fetchall()  -- return query results directly --

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

### Usage of the custom context manager
query = "SELECT * FROM users WHERE age > ?"
params = (25,)

with ExecuteQuery('users.db', query, params) as results:
    print("Users older than 25:")
    for row in results:
        print(row)
