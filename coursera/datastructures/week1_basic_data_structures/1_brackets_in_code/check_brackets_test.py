import unittest
from .check_brackets import find_mismatch


class CarFueling(unittest.TestCase):
    def test(self):
        for (input, answer) in [
            ("(){}[]", None),
            ("(}", 2),
            ("(((", 1),
        ]:
            self.assertEqual(find_mismatch(input), answer)


if __name__ == '__main__':
    unittest.main()