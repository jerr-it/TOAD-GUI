import math

import numpy as np

from patching.algorithms.wavefunctioncollapse.pattern import Pattern, Direction


class PatternScanner:
    """
    Analyzes the distribution of patterns in the grid.
    """

    def __init__(self, grid: np.ndarray, kernel_size: int):
        self.pattern_distribution: dict[Pattern, int] = {}
        self.pattern_distribution_list: list[tuple[Pattern, int]] = []
        self.total_weight: int = 0

        self.rows: int = grid.shape[0]
        self.columns: int = grid.shape[1]

        # Pad grid to simulate wrapping around the edges.
        padded_grid: np.ndarray = np.pad(
            grid,
            ((0, math.ceil(kernel_size - 1)), (0, math.ceil(kernel_size - 1))),
            mode="wrap"
        )

        # Iterate over the grid and count the number of times each pattern occurs, including variations.
        for row in range(self.rows):
            for column in range(self.columns):
                kernel = Pattern(padded_grid[row:row + kernel_size, column:column + kernel_size])
                variations: list[Pattern] = kernel.create_variations()

                for variation in variations:
                    if variation not in self.pattern_distribution:
                        self.pattern_distribution[variation] = 0

                    self.pattern_distribution[variation] += 1

        # Generate adjacency lists.
        for pattern in self.pattern_distribution:
            for idx, other_pattern in enumerate(self.pattern_distribution):
                for direction in Direction:
                    if pattern.overlaps(other_pattern, direction):
                        pattern.add_adjacency(direction, idx)

        self.pattern_distribution_list = list(self.pattern_distribution.items())

    def get_full_pattern_set(self) -> set[int]:
        return set([i for i in range(len(self.pattern_distribution_list))])

    def get_pattern_index(self, p: Pattern) -> int:
        for idx, (pattern, weight) in enumerate(self.pattern_distribution_list):
            if pattern == p:
                return idx
        raise LookupError

    def get_pattern_entry(self, index: int) -> tuple[Pattern, int]:
        return self.pattern_distribution_list[index]

    def on_completion(self, grid: np.ndarray):
        raise NotImplementedError
