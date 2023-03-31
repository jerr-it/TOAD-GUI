import unittest
import numpy

from adapters import PatternScanner
from pattern import Pattern


class PatternScannerTest(unittest.TestCase):
    def test_scanner(self):
        grid = numpy.array([
            [1, 2, 3, 3, 2, 1],
            [5, 6, 7, 7, 6, 5],
            [9, 10, 11, 11, 10, 9],
            [13, 14, 15, 16, 17, 18],
        ])

        scanner = PatternScanner(grid, 3)

        p1 = Pattern([
            [1, 2, 3],
            [5, 6, 7],
            [9, 10, 11]
        ])

        self.assertTrue(p1 in scanner.pattern_distribution)
        self.assertEqual(scanner.pattern_distribution[p1], 2)

        p2 = Pattern([
            [10, 9, 9],
            [17, 18, 13],
            [2, 1, 1]
        ])

        self.assertTrue(p2 in scanner.pattern_distribution)
        self.assertEqual(scanner.pattern_distribution[p2], 1)

        p3 = Pattern([
            [18, 13, 14],
            [1, 1, 2],
            [5, 5, 6]
        ])

        self.assertTrue(p3 in scanner.pattern_distribution)
        self.assertEqual(scanner.pattern_distribution[p3], 1)
