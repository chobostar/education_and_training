import unittest
from toposort import toposort


class MyTestCase(unittest.TestCase):
    def test1(self):
        result = toposort([[1], [], [0], [0]])
        expected = [3, 2, 0, 1]
        self.assertEqual(expected, result)
    def test2(self):
        result = toposort([[], [], [0], []])
        expected = [3, 1, 2, 0]
        self.assertEqual(expected, result)
    def test3(self):
        result = toposort([[], [0], [1, 0], [2, 0], [1, 2]])
        expected = [4, 3, 2, 1, 0]
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
