import py4j.java_gateway

from patching.metrics.metric import Metric


class Coins(Metric):
    def __init__(self):
        self.coins_generated: int = 0
        self.coins_original: int = 0

    def pre_hook(
        self,
        original_level: list[str],
        original_mario_result: py4j.java_gateway.JavaObject,
        generated_level: list[str],
        generated_mario_result: py4j.java_gateway.JavaObject,
    ):
        self.coins_original = original_mario_result.getCurrentCoins()
        self.coins_generated = generated_mario_result.getCurrentCoins()

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
            "Coins original": self.coins_original,
            "Coins generated": self.coins_generated,
            "Coins fixed": mario_result.getCurrentCoins(),
        }
