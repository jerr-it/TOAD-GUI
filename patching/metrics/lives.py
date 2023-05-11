import py4j.java_gateway

from patching.metrics.metric import Metric


class Lives(Metric):
    def pre_hook(self):
        pass

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
    ) -> object:
        return mario_result.getCurrentLives()
