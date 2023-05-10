import tracemalloc

import py4j.java_gateway

from patching.metrics.metric import Metric


class Memory(Metric):
    def pre_hook(self):
        tracemalloc.clear_traces()
        tracemalloc.start()

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
    ) -> int:
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        return peak
