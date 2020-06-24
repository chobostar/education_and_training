import unittest
from strongly_connected import number_of_strongly_connected_components

class MyTestCase(unittest.TestCase):
    def test1(self):
        result = number_of_strongly_connected_components([[1], [2], [0], [0]])
        self.assertEqual(2, result)

    def test2(self):
        result = number_of_strongly_connected_components([[], [0], [1, 0], [2, 0], [1, 2]])
        self.assertEqual(5, result)

    def test3(self):
        result = number_of_strongly_connected_components([[1], [2], [0]])
        self.assertEqual(1, result)

    def test4(self):
        result = number_of_strongly_connected_components([[], [], [0]])
        self.assertEqual(3, result)

if __name__ == '__main__':
    unittest.main()
