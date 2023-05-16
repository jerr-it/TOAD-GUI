import py4j.java_gateway

from patching.metrics.metric import Metric


class Tries(Metric):
    def __init__(self):
        self.tries: int = 0

    def pre_hook(
        self,
        original_level: list[str],
        original_mario_result: py4j.java_gateway.JavaObject,
        generated_level: list[str],
        generated_mario_result: py4j.java_gateway.JavaObject,
    ):
        pass

    def iter_hook(
        self,
        mario_result: py4j.java_gateway.JavaObject,
        fixed_level: list[str],
    ):
        self.tries += 1

    def post_hook(
        self,
        mario_result: py4j.java_gateway.JavaObject,
        original_level: list[str],
        generated_level: list[str],
        fixed_level: list[str],
    ) -> dict[str, object]:
        ret = self.tries
        self.tries = 0
        return {
            "Tries": ret
        }
