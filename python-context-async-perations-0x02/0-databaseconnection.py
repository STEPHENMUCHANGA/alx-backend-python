## custom class based context manager for Database connection
### Objective
### create a class based context manager to handle opening and closing database connections automatically
--a class custom context manager DatabaseConnection using the __enter__ and the __exit__ methods--
--context manager with the with statement to be able to perform the query SELECT * FROM users--
import sqlite3

# Custom context manager for database connection
class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        return self.conn  ### This will be used as the connection object inside the 'with' block

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()

### Use the context manager with a 'with' statement
with DatabaseConnection('users.db') as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print(results)
