import time

import py4j.java_gateway

from patching.metrics.metric import Metric


class Runtime(Metric):
    def __init__(self):
        super().__init__()
        self.start = None

    def pre_hook(self):
        self.start = time.time()

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
    ) -> float:
        return time.time() - self.start
