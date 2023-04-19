
from patching.algorithms.wavefunctioncollapse.adapters.level_adapter import LevelAdapter
from patching.algorithms.wavefunctioncollapse.wfc import WFC
from patching.patcher import Patcher


class WFCPatcher(Patcher):
    """
    This patcher uses the Wave Function Collapse algorithm to fix broken level sections
    """
    def patch(
            self,
            original_level: list[str],
            level: list[str],  # Level formatted as a list of strings row-wise
            broken_range: tuple[tuple[int, int], tuple[int, int]]  # (x_range, y_range)
    ) -> list[str]:
        level_adapter = LevelAdapter(level, 3)

        wfc = WFC(level_adapter, broken_range, level)
        wfc.collapse()

        # Replace the broken section with the repaired section
        patched_section = level_adapter.result
        x_range, y_range = broken_range

        # Replace the broken section with the repaired section
        for y in range(y_range[0], y_range[1]):
            level[y] = level[y][:x_range[0]] + "".join(patched_section[y-y_range[0]]) + level[y][x_range[1]:]

        return level
