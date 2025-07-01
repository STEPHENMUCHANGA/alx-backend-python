## Memory-Efficient Aggregation with Generators

### Objective

#### to use a generator to compute a memory-efficient aggregate function i.e average age for a large dataset

-Implimentation of memory-efficient average age calculation using a generator and no SQL AVG() function

### 3-average_age.py
import mysql.connector

def stream_user_ages():
    connection = mysql.connector.connect(
        host='localhost',
        user='your_mysql_user',
        password='your_mysql_password',
        database='ALX_prodev'
    )
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")

    for (age,) in cursor:  # Loop 1: yield age one by one
        yield age

    cursor.close()
    connection.close()


def compute_average_age():
    total_age = 0
    count = 0

    for age in stream_user_ages():  # Loop 2: consuming generator
        total_age += age
        count += 1

    if count > 0:
        average = total_age / count
        print(f"Average age of users: {average:.2f}")
    else:
        print("No users in the database.")

### Usage of the average_age.py
#!/usr/bin/python3
from average_age import compute_average_age

compute_average_age()

#### The code ensured that:

- Only 2 loops used: one in stream_user_ages(), one in compute_average_age().

- Fetches and processes one age at a time — memory-efficient.

- No SQL AVG() used — aggregation is done manually in Python.

- The (age,) syntax unpacks a tuple returned by cursor.
