from patching import Patcher


class WFCPatcher(Patcher):
    """
    This patcher uses the Wave Function Collapse algorithm to fix broken level sections
    """
    def patch(
            self,
            level: list[str],  # Level formatted as a list of strings row-wise
            broken_range: tuple[tuple[int, int], tuple[int, int]]  # (x_range, y_range)
    ) -> list[str]:
        raise NotImplementedError("patch is not implemented")
