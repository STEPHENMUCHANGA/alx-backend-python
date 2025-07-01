## generator that streams rows from an SQL database

### Objective
#### create a generator that streams rows from an SQL database one by one.
### Requirements Recap
- Use a Python generator (yield) to fetch one row at a time from the user_data table.

- The function must be named stream_users().

- Must use only one loop.

- Output each row as a dictionary.

- Compatible with the provided 1-main.py test script.
  
### 0-stream_users.py using python:
  import mysql.connector

def stream_users():
    connection = mysql.connector.connect(
        host='localhost',
        user='your_mysql_user',
        password='your_mysql_password',
        database='ALX_prodev'
    )

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    for row in cursor:
        yield row

    cursor.close()
    connection.close()
