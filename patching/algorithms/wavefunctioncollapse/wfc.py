from __future__ import annotations

import numpy as np

from patching.algorithms.wavefunctioncollapse import WaveFunction, Direction
from patching.algorithms.wavefunctioncollapse.adapters import PatternScanner


class WFC:
    def __init__(self, pattern_scanner: PatternScanner, output_dimensions: tuple[int, int]):
        self.pattern_scanner = pattern_scanner

        self.grid = np.array([
                [WaveFunction(self.pattern_scanner) for _ in range(output_dimensions[1])] for _ in range(output_dimensions[0])
            ]
        )

        self.collapse()

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
