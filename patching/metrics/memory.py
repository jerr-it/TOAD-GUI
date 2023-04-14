import tracemalloc

from patching.metrics.metric import Metric


class Memory(Metric):
    def pre_hook(self):
        tracemalloc.start()

    def post_hook(self, fixed_level: list[str]) -> int:
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        return peak
