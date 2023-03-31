import unittest

from pattern import Pattern, Direction


class TestPattern(unittest.TestCase):

    def test_equals(self):
        pattern = Pattern([
            [1, 2],
            [3, 4]
        ])
        target = Pattern([
            [1, 2],
            [3, 4]
        ])

        self.assertTrue(pattern == target)

    def test_rotate(self):
        pattern = Pattern([
            [1, 2],
            [3, 4]
        ])
        target = Pattern([
            [2, 4],
            [1, 3]
        ])

        rotated = pattern.rotate()
        self.assertTrue(rotated == target)

    def test_create_variations(self):
        pattern = Pattern([
            [1, 2],
            [3, 4]
        ])

        rotations: list[Pattern] = pattern.create_variations()

        self.assertTrue(rotations[0] == Pattern([
            [1, 2],
            [3, 4]
        ]))
        self.assertTrue(rotations[1] == Pattern([
            [2, 4],
            [1, 3]
        ]))
        self.assertTrue(rotations[2] == Pattern([
            [4, 3],
            [2, 1]
        ]))
        self.assertTrue(rotations[3] == Pattern([
            [3, 1],
            [4, 2]
        ]))
        self.assertTrue(rotations[4] == Pattern([
            [3, 4],
            [1, 2]
        ]))
        self.assertTrue(rotations[5] == Pattern([
            [2, 1],
            [4, 3]
        ]))

    def test_create_vertical_flip(self):
        pattern = Pattern([
            [1, 2],
            [3, 4]
        ])
        target = Pattern([
            [2, 1],
            [4, 3]
        ])

        flipped = pattern.create_vertical_flip()
        self.assertTrue(flipped == target)

    def test_create_horizontal_flip(self):
        pattern = Pattern([
            [1, 2],
            [3, 4]
        ])
        target = Pattern([
            [3, 4],
            [1, 2]
        ])

        flipped = pattern.create_horizontal_flip()
        self.assertTrue(flipped == target)

    def test_overlaps_up(self):
        pattern = Pattern([
            [1, 1, 1],
            [1, 1, 1],
            [0, 0, 0]
        ])

        target = Pattern([
            [0, 0, 0],
            [1, 1, 1],
            [1, 1, 1]
        ])

        self.assertTrue(pattern.overlaps(target, Direction.UP))

        pattern = Pattern([
            [1, 1, 1],
            [1, 1, 1],
            [0, 0, 0]
        ])

        target = Pattern([
            [0, 0, 0],
            [1, 1, 1],
            [2, 0, 1]
        ])

        self.assertFalse(pattern.overlaps(target, Direction.UP))

    def test_overlaps_down(self):
        pattern = Pattern([
            [0, 0, 0],
            [1, 1, 1],
            [1, 1, 1]
        ])

        target = Pattern([
            [1, 1, 1],
            [1, 1, 1],
            [0, 0, 0]
        ])

        self.assertTrue(pattern.overlaps(target, Direction.DOWN))

        pattern = Pattern([
            [0, 0, 0],
            [1, 1, 1],
            [1, 1, 1]
        ])

        target = Pattern([
            [1, 2, 1],
            [4, 3, 1],
            [0, 0, 0]
        ])

        self.assertFalse(pattern.overlaps(target, Direction.DOWN))

    def test_overlaps_right(self):
        pattern = Pattern([
            [0, 1, 1],
            [0, 1, 1],
            [0, 1, 1]
        ])

        target = Pattern([
            [1, 1, 0],
            [1, 1, 0],
            [1, 1, 0]
        ])

        self.assertTrue(pattern.overlaps(target, Direction.RIGHT))

        pattern = Pattern([
            [0, 1, 1],
            [0, 1, 1],
            [0, 1, 1]
        ])

        target = Pattern([
            [1, 3, 40],
            [4, 1, 3],
            [1, 1, 1]
        ])

        self.assertFalse(pattern.overlaps(target, Direction.RIGHT))

    def test_overlaps_left(self):
        pattern = Pattern([
            [1, 1, 0],
            [1, 1, 0],
            [1, 1, 0]
        ])

        target = Pattern([
            [0, 1, 1],
            [0, 1, 1],
            [0, 1, 1]
        ])

        self.assertTrue(pattern.overlaps(target, Direction.LEFT))

        pattern = Pattern([
            [1, 1, 0],
            [1, 1, 0],
            [1, 1, 0]
        ])

        target = Pattern([
            [1, 3, 40],
            [4, 1, 3],
            [1, 1, 1]
        ])

        self.assertFalse(pattern.overlaps(target, Direction.LEFT))
