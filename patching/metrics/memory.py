import tracemalloc

from patching.metrics.metric import Metric


class Memory(Metric):
    def pre_hook(self):
        tracemalloc.clear_traces()
        tracemalloc.start()

    def post_hook(
            self,
            original_level: list[str],
            generated_level: list[str],
            fixed_level: list[str],
    ) -> int:
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        return peak
