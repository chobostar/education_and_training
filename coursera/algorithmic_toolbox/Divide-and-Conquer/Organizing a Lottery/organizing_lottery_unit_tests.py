import unittest
from organizing_lottery import points_cover, points_cover_naive


class PointsAndSegments(unittest.TestCase):
    def test_small(self):
        for starts, ends, points in [
            ([0, 7], [5, 10], [1, 6, 11]),
            ([0, 0, 0], [2, 2, 2], [0, 1, 2]),
            ([0, 5], [7, 10], [1, 6, 11])
        ]:
            self.assertEqual(points_cover(list(starts), list(ends), list(points)),
                             points_cover_naive(starts, ends, points))
"""
    def test_random(self):
        type here

    def test_large(self):
        type here
"""

if __name__ == '__main__':
    unittest.main()
