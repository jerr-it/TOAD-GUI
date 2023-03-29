from patching import Patcher


class MultiPassPatcher(Patcher):
    """
    This patcher uses the Probabilistic Multi-Pass Generator by Ben Weber to fix broken level sections
    """
    def patch(self, level: list[str], broken_spot) -> list[str]:
        pass
