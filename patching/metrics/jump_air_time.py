import py4j.java_gateway

from patching.metrics.metric import Metric


class JumpAirTime(Metric):
    def __init__(self):
        self.generated_air_time = None
        self.original_air_time = None

    def pre_hook(
        self,
        original_level: list[str],
        original_mario_result: py4j.java_gateway.JavaObject,
        generated_level: list[str],
        generated_mario_result: py4j.java_gateway.JavaObject,
    ):
        self.original_air_time = original_mario_result.getMaxJumpAirTime()
        self.generated_air_time = generated_mario_result.getMaxJumpAirTime()

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
            "Original air time": self.original_air_time,
            "Generated air time": self.generated_air_time,
            "Fixed air time": mario_result.getMaxJumpAirTime()
        }
