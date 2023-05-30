import py4j.java_gateway

from patching.metrics.metric import Metric


class JumpLength(Metric):
    def __init__(self):
        self.generated_max_jump = None
        self.original_max_jump = None

    def pre_hook(
            self,
            original_level: list[str],
            original_mario_result: py4j.java_gateway.JavaObject,
            generated_level: list[str],
            generated_mario_result: py4j.java_gateway.JavaObject,
    ):
        self.original_max_jump = original_mario_result.getMaxXJump() / 16
        self.generated_max_jump = generated_mario_result.getMaxXJump() / 16

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
            "Original max jump": self.original_max_jump,
            "Generated max jump": self.generated_max_jump,
            "Fixed max jump": mario_result.getMaxXJump() / 16
        }
