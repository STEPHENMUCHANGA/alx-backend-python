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
