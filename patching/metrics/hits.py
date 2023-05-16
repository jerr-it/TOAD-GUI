import py4j.java_gateway

from patching.metrics.metric import Metric


class Hits(Metric):
    def __init__(self):
        self.generated_hits: int = 0
        self.original_hits: int = 0

    def pre_hook(
        self,
        original_level: list[str],
        original_mario_result: py4j.java_gateway.JavaObject,
        generated_level: list[str],
        generated_mario_result: py4j.java_gateway.JavaObject,
    ):
        self.original_hits = original_mario_result.getMarioNumHurts()
        self.generated_hits = generated_mario_result.getMarioNumHurts()

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
            "Original hits": self.original_hits,
            "Generated hits": self.generated_hits,
            "Fixed hits": mario_result.getMarioNumHurts(),
        }
