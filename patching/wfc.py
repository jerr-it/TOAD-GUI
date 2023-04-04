
from patching.algorithms.wavefunctioncollapse.adapters.level_adapter import LevelAdapter
from patching.algorithms.wavefunctioncollapse.wfc import WFC
from patching.patcher import Patcher


class WFCPatcher(Patcher):
    """
    This patcher uses the Wave Function Collapse algorithm to fix broken level sections
    """
    def patch(
            self,
            level: list[str],  # Level formatted as a list of strings row-wise
            broken_range: tuple[tuple[int, int], tuple[int, int]]  # (x_range, y_range)
    ) -> list[str]:
        level_adapter = LevelAdapter(level, 3)
        wfc = WFC(level_adapter, broken_range, level)
        wfc.collapse()
        return level_adapter.result
