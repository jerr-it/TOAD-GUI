import math

import numpy as np

from patching.patcher import Patcher


class BestFitStitching(Patcher):
    def __init__(self):
        # Keeps track which sections we already tried to avoid infinite loops
        # level -> list[int]
        self.record: dict[str, list[int]] = {}

    def patch(
            self,
            original_level: list[str],
            level: list[str],  # Level formatted as a list of strings row-wise
            broken_range: tuple[tuple[int, int], tuple[int, int]],  # (x_range, y_range)
            generator_path: str = "",
    ) -> list[str]:
        level_key = "@".join(level)
        if level_key not in self.record:
            self.record[level_key] = []

        original_level = np.array([list(row) for row in original_level])
        level = np.array([list(row) for row in level])

        x_range, y_range = broken_range
        x_range_width = x_range[1] - x_range[0]

        broken_column_left = level[:, x_range[0] - 1]
        broken_column_right = level[:, x_range[0] + 1]

        record_score = -math.inf
        record_pos = -1
        for x in range(1, original_level.shape[1] - x_range_width - 1):
            if x in self.record[level_key]:
                continue

            original_column_left = original_level[:, x - 1]
            original_column_right = original_level[:, x + 1]

            score = \
                similarity(original_column_left, broken_column_left) \
                + similarity(original_column_right, broken_column_right)

            if score > record_score:
                record_score = score
                record_pos = x

        self.record[level_key].append(record_pos)

        repl_range = (
            (record_pos, record_pos + x_range_width),
            (y_range[0], y_range[1])
        )

        level[y_range[0]:y_range[1], x_range[0]:x_range[1]] \
            = original_level[repl_range[1][0]:repl_range[1][1], repl_range[0][0]:repl_range[0][1]]

        return ["".join(row) for row in level]


def similarity(a: np.ndarray, b: np.ndarray) -> int:
    """
    Counts how many elements in the two arrays are equal
    :param a: first array
    :param b: second array
    :return: count of equal elements
    """
    if a.shape != b.shape:
        raise Exception(f"A and B are not the same shape: a: {a.shape}, b: {b.shape}")

    count: int = 0
    for i in range(len(a)):
        if a[i] == b[i]:
            count += 1

    return count
