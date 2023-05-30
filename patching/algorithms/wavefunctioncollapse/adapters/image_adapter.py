import matplotlib.image as mpimg
import numpy as np

from patching.algorithms.wavefunctioncollapse.adapters.pattern_scanner import PatternScanner


class ImageAdapter(PatternScanner):
    def __init__(self, path: str, kernel_size: int, output_filename: str = "output.png"):
        image = mpimg.imread(path)

        self.output_filename = output_filename

        # Convert the image to a 2D array of hexadecimal values.
        data = np.array([[self.pixel_to_hex(pixel) for pixel in line] for line in image])

        super().__init__(data, kernel_size)

    @staticmethod
    def pixel_to_hex(pixel: np.ndarray) -> str:
        return "#" + "".join([f"{int(value * 255):02x}" for value in pixel])

    @staticmethod
    def hex_to_pixel(hex: str) -> np.ndarray:
        return np.array([int(hex[i:i + 2], 16) / 255 for i in range(1, len(hex), 2)])

    def on_completion(self, grid: np.ndarray):
        data = np.array([[self.hex_to_pixel(hex) for hex in line] for line in grid])
        mpimg.imsave(self.output_filename, data)
