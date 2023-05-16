import py4j.java_gateway

from patching.metrics.metric import Metric


class TotalKills(Metric):
    def __init__(self):
        self.generated_kills = None
        self.original_kills = None

    def pre_hook(
        self,
        original_level: list[str],
        original_mario_result: py4j.java_gateway.JavaObject,
        generated_level: list[str],
        generated_mario_result: py4j.java_gateway.JavaObject,
    ):
        self.original_kills = original_mario_result.getKillsTotal()
        self.generated_kills = generated_mario_result.getKillsTotal()

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
            "Original kills": self.original_kills,
            "Generated kills": self.generated_kills,
            "Fixed kills": mario_result.getKillsTotal(),
        }
