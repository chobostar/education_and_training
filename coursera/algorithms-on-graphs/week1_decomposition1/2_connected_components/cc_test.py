import unittest
import connected_components

class MyTestCase(unittest.TestCase):
    def test1(self):
        result = connected_components.number_of_components([[1, 3], [0, 2], [1, 3], [2, 0]])
        self.assertEqual(1, result)
    def test2(self):
        result = connected_components.number_of_components([[1], [0], [3], [2]])
        self.assertEqual(2, result)


if __name__ == '__main__':
    unittest.main()
