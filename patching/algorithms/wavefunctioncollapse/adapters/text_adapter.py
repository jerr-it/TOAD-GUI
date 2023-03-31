import numpy as np

from patching.algorithms.wavefunctioncollapse.adapters import PatternScanner


class TextAdapter(PatternScanner):
    def __init__(self, path: str, kernel_size: int, output_filename: str = "output.txt"):
        with open(path) as file:
            text = file.read()

        data = np.array([[char for char in line] for line in text.splitlines()])

        super().__init__(data, kernel_size, output_filename)

    def on_completion(self, grid: np.ndarray):
        # Save the grid as a text file.
        with open(self.output_filename, "w") as file:
            for line in grid:
                file.write("".join(line) + "\n")
