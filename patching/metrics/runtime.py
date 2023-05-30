import time

import py4j.java_gateway

from patching.metrics.metric import Metric


class Runtime(Metric):
    def __init__(self):
        self.start = None

    def pre_hook(
            self,
            original_level: list[str],
            original_mario_result: py4j.java_gateway.JavaObject,
            generated_level: list[str],
            generated_mario_result: py4j.java_gateway.JavaObject,
    ):
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
    ) -> dict[str, object]:
        return {
            "Runtime": time.time() - self.start
        }
