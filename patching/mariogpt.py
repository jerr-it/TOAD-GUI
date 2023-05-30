import numpy as np
import py4j.java_gateway

from mario_gpt import MarioLM
from patching.patcher import Patcher

PROMPTS = {
    "": ["some pipes", "some enemies", "many blocks", "low elevation"],
    "./data/TOAD_GAN_1-1": ["some pipes", "some enemies", "many blocks", "low elevation"],
    "./data/TOAD_GAN_1-2": ["little pipes", "little enemies", "many blocks", "low elevation"],
    "./data/TOAD_GAN_1-3": ["no pipes", "some enemies", "some blocks", "high elevation"],
    "./data/TOAD_GAN_2-1": ["some pipes", "some enemies", "many blocks", "low elevation"],
    "./data/TOAD_GAN_3-1": ["some pipes", "some enemies", "many blocks", "low elevation"],
    "./data/TOAD_GAN_3-3": ["no pipes", "some enemies", "some blocks", "high elevation"],
    "./data/TOAD_GAN_4-1": ["some pipes", "some enemies", "many blocks", "low elevation"],
    "./data/TOAD_GAN_4-2": ["little pipes", "little enemies", "many blocks", "low elevation"],
    "./data/TOAD_GAN_5-1": ["some pipes", "some enemies", "many blocks", "low elevation"],
    "./data/TOAD_GAN_5-3": ["no pipes", "some enemies", "some blocks", "high elevation"],
    "./data/TOAD_GAN_6-1": ["some pipes", "some enemies", "many blocks", "low elevation"],
    "./data/TOAD_GAN_6-2": ["little pipes", "little enemies", "many blocks", "low elevation"],
    "./data/TOAD_GAN_6-3": ["no pipes", "some enemies", "some blocks", "high elevation"],
    "./data/TOAD_GAN_7-1": ["some pipes", "some enemies", "many blocks", "low elevation"],
    "./data/TOAD_GAN_8-1": ["some pipes", "some enemies", "many blocks", "low elevation"],
}


class MarioGPT(Patcher):
    def __init__(self):
        self.mario_lm = MarioLM()

    def patch(
            self,
            original_level: list[str],
            level: list[str],  # Level formatted as a list of strings row-wise
            broken_range: tuple[tuple[int, int], tuple[int, int]],  # (x_range, y_range)
            generator_path: str = "",
            mario_result: py4j.java_gateway.JavaObject = None,
    ) -> list[str]:
        level = np.array([list(row) for row in level])

        x_range, y_range = broken_range
        replacement = self.mario_lm.sample(
            prompts=PROMPTS[generator_path],
            num_steps=142,
            temperature=2.2,
            use_tqdm=False
        )[0]

        level[y_range[0]:y_range[1], x_range[0]:x_range[1]] = convert_format(replacement.level)

        return ["".join(row) for row in level]


def convert_format(level: list[str]) -> np.ndarray:
    convert = ["-" * 10, "-" * 10]

    for line in level:
        convert.append(
            line.replace("x", "-").replace("[", "t").replace("]", "t").replace("<", "t").replace(">", "t")
        )
    return np.array([list(row) for row in convert])
