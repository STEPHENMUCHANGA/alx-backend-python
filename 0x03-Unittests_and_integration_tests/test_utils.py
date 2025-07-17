## Parameterize a unit test
### Objective
-Understand how the utils.access_nested_map function works.
- Write a unit test for it using unittest.TestCase.
-Use @parameterized.expand to test multiple input cases concisely.
### Understanding access_nested_map
# utils.py
def access_nested_map(nested_map, path):
    for key in path:
        nested_map = nested_map[key]
    return nested_map
-- function retrieves a value from a nested dictionary based on a sequence of keys (path)--
### Create Unit Test File by
-Import unittest and parameterized.
-Import the function from utils.
-Write a test class that inherits from unittest.TestCase.
### Final Code: test_utils.py
import unittest
from parameterized import parameterized

from utils import access_nested_map

class TestAccessNestedMap(unittest.TestCase):
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)
-- How to Run the Test, run the test using--
python -m unittest test_utils.py


