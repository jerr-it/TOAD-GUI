import py4j.java_gateway

from patching.metrics.metric import Metric


class Jumps(Metric):
    def __init__(self):
        self.generated_jumps = None
        self.original_jumps = None

    def pre_hook(
            self,
            original_level: list[str],
            original_mario_result: py4j.java_gateway.JavaObject,
            generated_level: list[str],
            generated_mario_result: py4j.java_gateway.JavaObject,
    ):
        self.original_jumps = original_mario_result.getNumJumps()
        self.generated_jumps = generated_mario_result.getNumJumps()

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
            "Original jumps": self.original_jumps,
            "Generated jumps": self.generated_jumps,
            "Fixed jumps": mario_result.getNumJumps(),
        }
