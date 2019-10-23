import unittest
from car_fueling import compute_min_number_of_refills


class CarFueling(unittest.TestCase):
    def test(self):
        for (d, m, stops, answer) in [
            (950, 400, [200, 375, 550, 750], 2),
            (10, 3, [1, 2, 5, 9], -1),
            (200, 250, [100, 150], 0),
            (10, 1, [1, 2, 3, 4, 5, 6, 7, 8, 9], 9),
            (10, 2, [1, 2, 3, 4, 5, 6, 7, 8, 9], 4),
        ]:
            self.assertEqual(compute_min_number_of_refills(d, m, stops), answer)


if __name__ == '__main__':
    unittest.main()
