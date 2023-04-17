import numpy as np

from patching.metrics.metric import Metric

EPSILON = 1e-8


class TPKLGenerated(Metric):
    """
    Calculates the TPKL between the original level and the generated level.
    """

    def pre_hook(self):
        pass

    def post_hook(
            self,
            original_level: list[str],
            generated_level: list[str],
            fixed_level: list[str],
    ) -> float:
        return tpkl(original_level, generated_level)


class TPKLPatched(Metric):
    """
    Calculates the TPKL between the original level and the patched level.
    """

    def pre_hook(self):
        pass

    def post_hook(
            self,
            original_level: list[str],
            generated_level: list[str],
            fixed_level: list[str],
    ) -> float:
        return tpkl(original_level, fixed_level)


def tpkl(level_a: list[str], level_b: list[str], kernel_size: int = 3) -> float:
    """
    Calculate the Tile pattern kullback-leibler divergence between two levels.
    See https://arxiv.org/pdf/1905.05077.pdf

    :param level_a: The first level.
    :param level_b: The second level.
    :param kernel_size: Pattern size.
    :return: The Tile pattern kullback-leibler divergence between the two levels.
    """
    # Convert levels to 2d numpy arrays, splitting the strings into lists of chars
    level_a = np.array([list(x) for x in level_a])
    level_b = np.array([list(x) for x in level_b])

    # Iterate over all kernel_size x kernel_size tiles in the level
    # and count the number of times each tile appears
    tile_counts_a = {}
    tile_counts_b = {}

    for row in range(level_a.shape[0] - kernel_size + 1):
        for col in range(level_a.shape[1] - kernel_size + 1):
            tile = tuple(level_a[row:row + kernel_size, col:col + kernel_size].flatten())
            tile_counts_a[tile] = tile_counts_a.get(tile, 0) + 1

            tile = tuple(level_b[row:row + kernel_size, col:col + kernel_size].flatten())
            tile_counts_b[tile] = tile_counts_b.get(tile, 0) + 1

    # Compute the total number of tiles in the level
    total_tiles_a = sum(tile_counts_a.values())
    total_tiles_b = sum(tile_counts_b.values())

    # Compute the probability of each tile
    tile_probabilities_a = {tile: compute_pattern_probability(count, total_tiles_a) for tile, count in tile_counts_a.items()}
    tile_probabilities_b = {tile: compute_pattern_probability(count, total_tiles_b) for tile, count in tile_counts_b.items()}

    # Compute the kullback-leibler divergence between the two levels
    divergence = 0
    for tile, probability_a in tile_probabilities_a.items():
        probability_b = tile_probabilities_b.get(tile, EPSILON)
        divergence += probability_a * np.log(probability_a / probability_b)

    for tile, probability_b in tile_probabilities_b.items():
        probability_a = tile_probabilities_a.get(tile, EPSILON)
        divergence += probability_b * np.log(probability_b / probability_a)

    return divergence


def compute_pattern_probability(pattern_count: int, total_count: int) -> float:
    """
    Compute the probability of a given pattern.

    :param pattern_count: The number of times the pattern appears.
    :param total_count: The total number of patterns.
    :param epsilon: A small number to prevent division by zero.
    :return: The probability of the pattern.
    """
    return (pattern_count + EPSILON) / ((total_count + EPSILON) * (1 + EPSILON))
