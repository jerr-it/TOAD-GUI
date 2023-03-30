from patching import Patcher


class EAPatcher(Patcher):
    """
    This patcher uses an evolutionary algorithm to fix broken level sections
    """
    def patch(
            self,
            level: list[str],  # Level formatted as a list of strings row-wise
            broken_range: tuple[tuple[int, int], tuple[int, int]]  # (x_range, y_range)
    ) -> list[str]:
        raise NotImplementedError("patch is not implemented")
