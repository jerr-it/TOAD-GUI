import numpy as np

from patching.patcher import Patcher


class StichingPatcher(Patcher):
    """
    This patcher fixes the broken range by 'stitching' the broken range from the original into the generated level.
    """
    def patch(
            self,
            level_file: str,
            original_level: list[str],
            level: list[str],  # Level formatted as a list of strings row-wise
            broken_range: tuple[tuple[int, int], tuple[int, int]]  # (x_range, y_range)
    ) -> list[str]:
        # Convert levels to 2d numpy arrays, splitting strings into chars
        original_level = np.array([list(row) for row in original_level])
        level = np.array([list(row) for row in level])

        x_range, y_range = broken_range
        x_range_width = x_range[1] - x_range[0]

        # Pick a random range from the original level with the same dimensions as the broken range
        low_x_rng = np.random.randint(0, original_level.shape[1] - x_range_width)

        rng_range = ((low_x_rng, low_x_rng + x_range_width), (y_range[0], y_range[1]))

        a = level[y_range[0]:y_range[1], x_range[0]:x_range[1]].shape
        b = original_level[rng_range[1][0]:rng_range[1][1], rng_range[0][0]:rng_range[0][1]].shape

        # Copy the random range from the original level into the broken range of the generated level
        level[y_range[0]:y_range[1], x_range[0]:x_range[1]] = original_level[rng_range[1][0]:rng_range[1][1], rng_range[0][0]:rng_range[0][1]]

        return ["".join(row) for row in level]
