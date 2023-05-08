import time

from patching.metrics.metric import Metric


class Runtime(Metric):
    def __init__(self):
        super().__init__()
        self.start = None

    def pre_hook(self):
        self.start = time.time()

    def iter_hook(
        self,
        progress: float,
        fixed_level: list[str],
    ):
        pass

    def post_hook(
            self,
            original_level: list[str],
            generated_level: list[str],
            fixed_level: list[str],
    ) -> float:
        return time.time() - self.start
