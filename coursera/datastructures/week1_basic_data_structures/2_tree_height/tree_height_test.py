import unittest
from .tree_height import compute_height


class DoTest(unittest.TestCase):
    def test(self):
        for (tree, answer) in [
            ((5, [4, -1, 4, 1, 1]), 3),
            ((5, [-1, 0, 4, 0, 3]), 4),
            ((10, [8, 8, 5, 6, 7, 3, 1, 6, -1, 5]), 6),
        ]:
            self.assertEqual(compute_height(tree[0], tree[1]), answer)


if __name__ == '__main__':
    unittest.main()