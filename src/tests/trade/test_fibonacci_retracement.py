import unittest

from fx.trading.fibonacci_retracement import FibonacciRetracement


class TestFibonacciRetracement(unittest.TestCase):
    def test_get_levels_ascending(self):
        levels = FibonacciRetracement.get_levels(min_price=0.60654, max_price=0.61210, mode='ASCENDING')
        expected_levels = {
            '1': 0.60654,
            '0.786': 0.60772,
            '0.618': 0.60866,
            '0.5': 0.60932,
            '0.382': 0.60997,
            '0.236': 0.61078,
            '0': 0.6121,
            '-0.382': 0.61422,
            '-0.618': 0.61553,
            '-1': 0.61766,
            '-1.618': 0.621096
        }

        for k, v in expected_levels.items():
            self.assertAlmostEqual(v, levels[k], places=4)

    def test_get_levels_descending(self):
        levels = FibonacciRetracement.get_levels(min_price=0.61210, max_price=0.60654, mode='DESCENDING')
        expected_levels = {
            '1': 0.60654,
            '0.786': 0.6077,
            '0.618': 0.60866,
            '0.5': 0.60932,
            '0.382': 0.60997,
            '0.236': 0.61078,
            '0': 0.6121,
            '-0.382': 0.614223,
            '-0.618': 0.615536,
            '-1': 0.61766,
            '-1.618': 0.621096
        }

        for k, v in expected_levels.items():
            self.assertAlmostEqual(v, levels[k], places=4)
