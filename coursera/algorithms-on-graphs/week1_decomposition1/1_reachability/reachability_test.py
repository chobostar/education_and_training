import unittest
import reachability

class MyTestCase(unittest.TestCase):
    def test1(self):
        result = reachability.reach([[1, 3], [0, 2], [1, 3], [2, 0]], 0, 3)
        self.assertEqual(1, result)
    def test2(self):
        result = reachability.reach([[1], [0], [3], [2]], 0, 3)
        self.assertEqual(0, result)

if __name__ == '__main__':
    unittest.main()
