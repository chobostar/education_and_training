import unittest
from quicksort import randomized_quick_sort
from random import randint


class TestQuickSort(unittest.TestCase):
    def test_small(self):
        for array in [
            ([1, 2, 3]),
            ([3, 2, 1]),
            ([1, 1, 7, 7, 0, 8]),
            ([1, 0, 1, 0, 1, 1, 1, 1, 0, 0]),
            ([94531, 48089, 79506, 39398, 60450, 77713, 12997, 85603, 47297, 88096])
        ]:
            sorted_array = sorted(list(array))
            randomized_quick_sort(array, 0, len(array) - 1)
            self.assertEqual(array, sorted_array)

    def test_large(self):
        for n in (10, 100, 10 ** 5):
            for max_value in (1, 2, 10, 10 ** 5):
                array = [randint(0, max_value) for _ in range(n)]
                sorted_array = sorted(list(array))
                randomized_quick_sort(array, 0, len(array) - 1)
                self.assertEqual(array, sorted_array)


if __name__ == '__main__':
    unittest.main()
