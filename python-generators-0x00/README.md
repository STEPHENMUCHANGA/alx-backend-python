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


