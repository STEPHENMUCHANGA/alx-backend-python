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
    for batch in stream_users_in_batches(batch_size):  # loop 1
        for user in batch:  # loop 2
            if user['age'] > 25:
                yield user  # loop 3 is implicit inside generator consumption

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
  
