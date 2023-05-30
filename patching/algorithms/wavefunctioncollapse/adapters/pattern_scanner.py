import math

import numpy as np

from patching.algorithms.wavefunctioncollapse.pattern import Pattern, Direction


class PatternScanner:
    """
    Analyzes the distribution of patterns in the grid.
    """

    def __init__(self, grid: np.ndarray, kernel_size: int):
        self.pattern_distribution: dict[Pattern, int] = {}
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
            for other_pattern in self.pattern_distribution:
                for direction in Direction:
                    if pattern.overlaps(other_pattern, direction):
                        pattern.add_adjacency(direction, other_pattern)

    def get_full_pattern_set(self) -> set[Pattern]:
        return set(self.pattern_distribution.keys())

    def get_pattern_weight(self, pattern: Pattern) -> int:
        return self.pattern_distribution[pattern]

    def on_completion(self, grid: np.ndarray):
        raise NotImplementedError
