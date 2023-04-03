import numpy as np

from patching.algorithms.wavefunctioncollapse.adapters.pattern_scanner import PatternScanner


class LevelAdapter(PatternScanner):
    def __init__(self, level: list[str], kernel_size: int):
        data = np.array([[char for char in line] for line in level])

        self.result: list[str] = []

        super().__init__(data, kernel_size)

    def on_completion(self, grid: np.ndarray):
        # Convert grid back to a list of strings
        self.result = [''.join(row) for row in grid]
