from patching import Patcher


class WFCPatcher(Patcher):
    """
    This patcher uses the Wave Function Collapse algorithm to fix broken level sections
    """
    def patch(self, level: list[str], broken_spot) -> list[str]:
        # TODO: use wfc implementation (should be put into the algorithm folder)
        pass
