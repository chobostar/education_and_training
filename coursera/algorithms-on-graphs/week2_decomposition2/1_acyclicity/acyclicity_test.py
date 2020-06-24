import unittest
from acyclicity import acyclic


class MyTestCase(unittest.TestCase):
    def test1(self):
        result = acyclic([[1], [2], [0], [0]])
        self.assertEqual(1, result)
    def test2(self):
        result = acyclic([[1, 2, 3], [2, 4], [3, 4], [], []])
        self.assertEqual(0, result)


if __name__ == '__main__':
    unittest.main()
