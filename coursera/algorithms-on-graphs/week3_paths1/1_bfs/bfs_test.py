import unittest
from bfs import distance

class MyTestCase(unittest.TestCase):
    def test1(self):
        result = distance([[1, 3, 2], [0, 2], [1, 0], [0]], 1, 3)
        self.assertEqual(2, result)

    def test2(self):
        result = distance([[], [], [], []], 1, 3)
        self.assertEqual(-1, result)

if __name__ == '__main__':
    unittest.main()
