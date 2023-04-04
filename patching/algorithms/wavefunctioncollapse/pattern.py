from __future__ import annotations

import math
import numpy as np

from enum import Enum


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class Pattern:
    """
    This class represents a wfc pattern.
    It's a two-dimensional array of objects.
    Objects need to be comparable.
    """
    def __init__(self, data):
        self.data: np.ndarray = np.array(data)
        self.rows: int = self.data.shape[0]
        self.columns: int = self.data.shape[1]

        self.adjacencies: dict[Direction, set[Pattern]] = {}

    def __hash__(self) -> int:
        return hash(self.data.tobytes())

    def __eq__(self, other: Pattern) -> bool:
        return (self.data == other.data).all()

    def equals_ignore(self, other: Pattern, symbol) -> bool:
        """
        Checks if the pattern is equal to another pattern, ignoring a given symbol.
        :param other: The other pattern to compare to.
        :param symbol: The symbol to ignore in the comparison.
        :return: True if the patterns are equal, ignoring the given symbol.
        """
        # False if patterns aren't the same shape
        if self.data.shape != other.data.shape:
            return False

        # False if patterns aren't equal, ignoring the given symbol
        for row in range(self.rows):
            for column in range(self.columns):
                # If the element is not the symbol, check if it is equal
                if self.data[row, column] != symbol and self.data[row, column] != other.data[row, column]:
                    return False

        return True

    def center_value(self) -> object:
        """
        Returns the value in the center of the pattern.
        """
        return self.data[self.rows // 2, self.columns // 2]

    def add_adjacency(self, direction: Direction, pattern: Pattern):
        """
        Adds a pattern to the adjacency list of the current pattern.
        """
        if direction not in self.adjacencies:
            self.adjacencies[direction] = set()

        self.adjacencies[direction].add(pattern)

    def overlaps(self, other: Pattern, direction: Direction) -> bool:
        """
        Checks if the pattern overlaps with another pattern in a given direction.
        """
        if self.data.shape != other.data.shape:
            raise Exception("Patterns must have the same shape. Got " + str(self.data.shape) + " and " + str(other.data.shape))

        match direction:
            case Direction.UP:
                # Self          Other
                # x x x ---\     0 0 0
                # x x x --\ \--- x x x
                # 0 0 0    \---- x x x
                half_idx: int = math.ceil(self.rows / 2)

                return (
                    self.data[:half_idx, :] ==
                    other.data[half_idx-1:, :]
                ).all()

            case Direction.RIGHT:
                # Self          Other
                # 0 x x         x x 0
                # 0 x x         x x 0
                # 0 x x         x x 0
                #   | ⎣_________⎦ |
                #   ⎣_____________⎦
                half_idx: int = math.ceil(self.columns / 2)

                return (
                    self.data[:, half_idx-1:] ==
                    other.data[:, :half_idx]
                ).all()

            case Direction.DOWN:
                # Self          Other
                # 0 0 0    /--- x x x
                # x x x --/ /-- x x x
                # x x x ---/    0 0 0
                half_idx: int = math.ceil(self.rows / 2)

                return (
                    self.data[half_idx-1:, :] ==
                    other.data[:half_idx, :]
                ).all()

            case Direction.LEFT:
                # Self          Other
                # x x 0         0 x x
                # x x 0         0 x x
                # x x 0         0 x x
                # | ⎣_____________⎦ |
                # ⎣_________________⎦
                half_idx: int = math.ceil(self.columns / 2)

                return (
                    self.data[:, :half_idx] ==
                    other.data[:, half_idx-1:]
                ).all()

        return False

    def rotate(self) -> Pattern:
        """
        Rotates the grid by 90 degrees counter-clockwise.
        """
        return Pattern(np.rot90(self.data))

    def create_vertical_flip(self) -> Pattern:
        """
        Creates a new pattern by flipping the original pattern horizontally.
        """
        return Pattern(np.fliplr(self.data))

    def create_horizontal_flip(self) -> Pattern:
        """
        Creates a new pattern by flipping the original pattern vertically.
        """
        return Pattern(np.flipud(self.data))

    def create_variations(self) -> list[Pattern]:
        """
        Creates an array of new patterns by rotating the original pattern.
        Also appends the horizontal and vertical flips of the original pattern.
        Includes append the original pattern.
        """
        # rotations = [self, self.rotate()]
        # for i in range(2):
        #     rotations.append(rotations[-1].rotate())
        #
        # rotations.append(self.create_horizontal_flip())
        # rotations.append(self.create_vertical_flip())

        # return rotations
        return [self]

    def __str__(self) -> str:
        return str(self.data)
