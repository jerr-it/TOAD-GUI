from __future__ import annotations

import numpy as np

from patching.algorithms.wavefunctioncollapse.adapters.pattern_scanner import PatternScanner
from patching.algorithms.wavefunctioncollapse.pattern import Direction, Pattern
from patching.algorithms.wavefunctioncollapse.wave import WaveFunction


class WFC:
    def __init__(
            self,
            pattern_scanner: PatternScanner,
            to_replace: tuple[tuple[int, int], tuple[int, int]],
            level: list[str]
    ):
        self.pattern_scanner = pattern_scanner
        x_range, y_range = to_replace

        # Convert level to 2d ndarray
        level = np.array([list(row) for row in level])

        # Create empty wave function grid
        self.grid = np.array([
                [WaveFunction(self.pattern_scanner) for _ in range(x_range[1] - x_range[0])]
                for _ in range(y_range[1] - y_range[0])
            ]
        )

        # Initialize edges of the grid for a better fit
        for column in [x_range[0], x_range[1]-1]:
            for row in range(y_range[0] + 1, y_range[1] - 1):
                # Extract 3x3 pattern from level
                pattern_arr = level[row-1:row+2, column-1:column+2]
                wave = self.find_pattern(pattern_arr, self.pattern_scanner)

                # Insert wave into self.grid
                self.grid[row - y_range[0]][column - x_range[0]] = wave

        # Initialize corners
        top_corners = [
            (x_range[0], y_range[0]),
            (x_range[1] - 1, y_range[0]),
        ]

        for corner_column, corner_row in top_corners:
            # 3 wide and 2 tall
            pattern_arr = level[corner_row:corner_row+2, corner_column-1:corner_column+2]
            # Fill unknown spots at the top with "dont cares"
            pattern_arr = np.insert(pattern_arr, 0, np.array([' ', ' ', ' ']), 0)

            wave = self.find_partly_matching_pattern(pattern_arr, self.pattern_scanner)
            self.grid[corner_row - y_range[0]][corner_column - x_range[0]] = wave

        bottom_corners = [
            (x_range[0], y_range[1] - 1),
            (x_range[1] - 1, y_range[1] - 1),
        ]

        for corner_column, corner_row in bottom_corners:
            # 3 wide and 2 tall
            pattern_arr = level[corner_row-1:corner_row+1, corner_column-1:corner_column+2]
            # Fill unknown spots at the top with "dont cares"
            pattern_arr = np.insert(pattern_arr, 2, np.array([' ', ' ', ' ']), 0)

            wave = self.find_partly_matching_pattern(pattern_arr, self.pattern_scanner)
            self.grid[corner_row - y_range[0]][corner_column - x_range[0]] = wave

    @staticmethod
    def find_pattern(pattern: np.ndarray, scanner: PatternScanner) -> WaveFunction | None:
        pattern = Pattern(pattern)
        p_set = scanner.get_full_pattern_set()
        for p in p_set:
            # Check every element in the pattern, defaulting to true if the element is a space
            # If all elements are true, return a new wave function with the pattern as its only possibility
            if pattern == p:
                return WaveFunction(p)
        return None

    @staticmethod
    def find_partly_matching_pattern(pattern: np.ndarray, scanner: PatternScanner) -> WaveFunction | None:
        pattern = Pattern(pattern)
        p_set = scanner.get_full_pattern_set()
        for p in p_set:
            # Check every element in the pattern, defaulting to true if the element is a space
            # If all elements are true, return a new wave function with the pattern as its only possibility
            if pattern.equals_ignore(p, " "):
                return WaveFunction(p)
        return None

    def find_random_least_entropy_wave(self) -> tuple[int, int]:
        least_entropy = np.inf
        least_entropy_wave = None

        for row in range(self.grid.shape[0]):
            for column in range(self.grid.shape[1]):
                wave = self.grid[row][column]

                if wave.is_collapsed():
                    continue

                if wave.entropy < least_entropy:
                    least_entropy = wave.entropy
                    least_entropy_wave = (row, column)

        return least_entropy_wave

    def propagate(self, cell: tuple[int, int]):
        open_stack = [cell]

        while len(open_stack) > 0:
            current = open_stack.pop()

            neighbours = self.get_neighbours(current)

            for direction, neighbour in neighbours.items():
                if self.grid[neighbour].is_collapsed():
                    continue

                if self.grid[neighbour].apply_constraints(self.grid[current].collect_adjacencies(direction)):
                    if self.grid[neighbour].is_contradictory():
                        raise Exception("Ran into contradiction")

                    if neighbour not in open_stack:
                        open_stack.append(neighbour)

    def get_neighbours(self, cell: tuple[int, int]) -> dict[Direction, tuple[int, int]]:
        neighbours = {}

        row, column = cell
        rows, columns = self.grid.shape

        u_row = (row - 1) % rows
        neighbours[Direction.UP] = (u_row, column)

        d_row = (row + 1) % rows
        neighbours[Direction.DOWN] = (d_row, column)

        l_column = (column - 1) % columns
        neighbours[Direction.LEFT] = (row, l_column)

        r_column = (column + 1) % columns
        neighbours[Direction.RIGHT] = (row, r_column)

        return neighbours

    def collapse(self):
        cell = self.find_random_least_entropy_wave()

        while cell is not None:
            self.grid[cell].observe()
            self.propagate(cell)
            cell = self.find_random_least_entropy_wave()

        self.pattern_scanner.on_completion(
            np.array([[list(wave.patterns)[0].center_value() for wave in row] for row in self.grid])
        )
