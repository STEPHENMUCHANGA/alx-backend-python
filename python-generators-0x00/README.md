## alx-backend-python
## Getting started with python generators 

### Objective

#### create a generator that streams rows from an SQL database one by one.

#### Complete python script seed.py to:  

- Connect to MySQL

- Create the ALX_prodev database

- Create user_data table

- Insert records from user_data.csv

- Provide generator functionality to stream rows

### Prerequisites
- Install mysql-connector-python
 - pip install mysql-connector-python
- Ensure your user_data.csv file exists in the same directory and looks like this example using graphql:
 - user_id,name,email,age
 - 001-uuid,John Doe,john@example.com,30
 - 002-uuid,Jane Smith,jane@example.com,45
 ...
### seed.py Implementation using python
 import mysql.connector
import csv
import uuid

#### Connect to MySQL Server (without specifying a database)
def connect_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='your_mysql_user',
            password='your_mysql_password'
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Connection Error: {err}")
        return None

#### Create ALX_prodev database
def create_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database created (or already exists).")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Database Creation Error: {err}")

#### Connect specifically to ALX_prodev
def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='your_mysql_user',
            password='your_mysql_password',
            database='ALX_prodev'
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Connection Error: {err}")
        return None

#### Create user_data table
def create_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL NOT NULL
            )
        """)
        print("Table user_data created successfully")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Table Creation Error: {err}")

#### Insert CSV data
def insert_data(connection, file_path):
    try:
        cursor = connection.cursor()
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                cursor.execute("""
                    INSERT IGNORE INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                """, (row['user_id'], row['name'], row['email'], row['age']))
        connection.commit()
        print("CSV data inserted successfully.")
        cursor.close()
    except Exception as e:
        print(f"Insertion Error: {e}")

#### Generator to stream rows
def stream_user_data(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_data")
    while True:
        row = cursor.fetchone()
        if row is None:
            break
        yield row
    cursor.close()

### 0-main.py Sample Execution
#### !/usr/bin/python3

### seed = __import__('seed')

#### connection = seed.connect_db()
#### if connection:
    seed.create_database(connection)
    connection.close()
    print("connection successful")

    connection = seed.connect_to_prodev()

    if connection:
        seed.create_table(connection)
        seed.insert_data(connection, 'user_data.csv')
        cursor = connection.cursor()
        cursor.execute(f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'ALX_prodev';")
        result = cursor.fetchone()
        if result:
            print(f"Database ALX_prodev is present")
        cursor.execute(f"SELECT * FROM user_data LIMIT 5;")
        rows = cursor.fetchall()
        print(rows)
        cursor.close()

        # Test generator
        print("\nStreaming users:")
        for user in seed.stream_user_data(connection):
            print(user)
            break  # Stream one at a time
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
    
## Batch processing Large Data

### Objective
#### Create a generator to fetch and process data in batches from the users database
- The complete solution is "Batch processing Large Data" using generators, MySQL, and Python, while complying with the constraint of using no more than 3 loops and yielding rows:

### 1-batch_processing.py using python:
import mysql.connector

def stream_users_in_batches(batch_size):
    connection = mysql.connector.connect(
        host='localhost',
        user='your_mysql_user',
        password='your_mysql_password',
        database='ALX_prodev'
    )

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    while True:
        rows = cursor.fetchmany(batch_size)
        if not rows:
            break
        yield rows  # Yield the batch

    cursor.close()
    connection.close()


def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                yield user  # YIELD matching user

#### Explanation:
- stream_users_in_batches(batch_size) fetches batch_size rows at a time and yields them as a list.

- Batch_processing(batch_size) consumes each batch, filters users with age > 25, and yields those users one by one.

- Uses only 2 explicit loops and one implicit (via generator consumption), fulfilling the 3-loop limit.

### Example Execution (2-main.py provided)

#!/usr/bin/python3
import sys
processing = __import__('1-batch_processing')

try:
    for user in processing.batch_processing(50):
        print(user)
except BrokenPipeError:
    sys.stderr.close()
    
- If we use "return" instead of "yield", we get:
# Not recommended if generator is required
def batch_processing(batch_size):
    filtered = []
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                filtered.append(user)
    return filtered
      
 - Then the 2-main.py will be:
users = processing.batch_processing(50)
for user in users:
    print(user)

## Lazy loading Paginated Data

### Objective

#### Simulte fetching paginated data from the users database using a generator to lazily load each page

- Lazy pagination using a generator

### Filename: 2-lazy_paginate.py
seed = __import__('seed')


def paginate_users(page_size, offset):
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows


def lazy_pagination(page_size):
    offset = 0
    while True:  # Only ONE loop used
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
      
- paginate_users(page_size, offset) fetches a page of users based on LIMIT and OFFSET.

- lazy_pagination(page_size) uses one loop and yield to lazily return each page.

- The offset increments by the page size after each yield.

- When no more rows are returned, it breaks out of the loop.

### Output with 3-main.py

python 3-main.py | head -n 7

- Will print the first 7 users lazily page-by-page, matching example given:

{'user_id': '00234e50-34eb-4ce2-94ec-26e3fa749796', 'name': 'Dan Altenwerth Jr.', ...}
...

  

