import py4j.java_gateway

from patching.metrics.metric import Metric


class Lives(Metric):
    def __init__(self):
        self.generated_lives = None
        self.original_lives = None

    def pre_hook(
        self,
        original_level: list[str],
        original_mario_result: py4j.java_gateway.JavaObject,
        generated_level: list[str],
        generated_mario_result: py4j.java_gateway.JavaObject,
    ):
        self.original_lives = original_mario_result.getCurrentLives()
        self.generated_lives = generated_mario_result.getCurrentLives()

    def iter_hook(
            self,
            mario_result: py4j.java_gateway.JavaObject,
            fixed_level: list[str],
    ):
        pass

    def post_hook(
            self,
            mario_result: py4j.java_gateway.JavaObject,
            original_level: list[str],
            generated_level: list[str],
            fixed_level: list[str],
    ) -> dict[str, object]:
        return {
            "Original lives": self.original_lives,
            "Generated lives": self.generated_lives,
            "Fixed lives": mario_result.getCurrentLives(),
        }
