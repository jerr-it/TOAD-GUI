import py4j.java_gateway

from patching.metrics.metric import Metric


class RemainingTime(Metric):
    def __init__(self):
        self.generated_remaining = None
        self.original_remaining = None

    def pre_hook(
            self,
            original_level: list[str],
            original_mario_result: py4j.java_gateway.JavaObject,
            generated_level: list[str],
            generated_mario_result: py4j.java_gateway.JavaObject,
    ):
        self.original_remaining = original_mario_result.getRemainingTime()
        self.generated_remaining = generated_mario_result.getRemainingTime()

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
            "Original remaining time": self.original_remaining,
            "Generated remaining time": self.generated_remaining,
            "Fixed remaining time": mario_result.getRemainingTime(),
        }
