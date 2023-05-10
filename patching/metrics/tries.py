import py4j.java_gateway

from patching.metrics.metric import Metric


class Tries(Metric):
    def __init__(self):
        self.tries: int = 1

    def pre_hook(self):
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
    ) -> object:
        ret = self.tries
        self.tries = 1
        return ret
