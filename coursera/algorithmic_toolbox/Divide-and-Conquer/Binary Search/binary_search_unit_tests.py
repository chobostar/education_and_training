import unittest
import random
from binary_search import binary_search, linear_search


class TestBinarySearch(unittest.TestCase):
    def test_small(self):
        for (keys, query) in [
            ([1, 2, 3], 1),
            ([4, 5, 6], 7),
            ([1, 2, 3, 4, 5], 6),
        ]:
            self.assertEqual(
                linear_search(keys, query),
                binary_search(keys, query)
            )
        for count in range(1, 1000):
            keys = sorted([random.randint(1, 10000) for i in range(random.randint(1,1000))])
            query = random.randint(1, 10000)
            self.assertEqual(
                linear_search(keys, query),
                binary_search(keys, query)
            )


    def test_large(self):
        for (keys, query, answer) in [
            (list(range(10 ** 4)), 10 ** 4, -1),
            ([1, 2, 3, 4, 5], 6, -1),
            ([1, 2, 3, 4, 5], 1, 0),
            ([1, 5, 8, 12, 13], 11, -1),
            (list(range(10 ** 4)), 239, 239),
        ]:
            self.assertEqual(binary_search(keys, query), answer)


if __name__ == '__main__':
    unittest.main()
