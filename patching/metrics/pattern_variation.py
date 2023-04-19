import numpy as np

from patching.metrics.metric import Metric


class PatternVariationChange(Metric):
    def pre_hook(self):
        pass

    def post_hook(
            self,
            original_level: list[str],
            generated_level: list[str],
            fixed_level: list[str],
    ) -> float:
        return pattern_variation(fixed_level) - pattern_variation(generated_level)


def pattern_variation(level: list[str], kernel_size: int = 3) -> float:
    # Convert level to 2d numpy array, splitting the strings into lists of chars
    level = np.array([list(x) for x in level])

    # Iterate over all kernel_size x kernel_size tiles in the level
    # and count the number of times each pattern appears
    pattern_counts = {}
    for row in range(level.shape[0] - kernel_size + 1):
        for col in range(level.shape[1] - kernel_size + 1):
            pattern = tuple(level[row:row + kernel_size, col:col + kernel_size].flatten())
            pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1

    # Calculate the total number of patterns in the level
    total_patterns = (level.shape[0] - kernel_size + 1) * (level.shape[1] - kernel_size + 1)

    return len(pattern_counts) / total_patterns
