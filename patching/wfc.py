
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
            broken_range: tuple[tuple[int, int], tuple[int, int]],  # (x_range, y_range)
            generator_path: str = "",
    ) -> list[str]:
        level_adapter = LevelAdapter(level, 3)

        wfc = WFC(level_adapter, broken_range, level)
        wfc.collapse()

        # Replace the broken section with the repaired section
        patched_section = level_adapter.result
        x_range, y_range = broken_range

        for row in range(y_range[0], y_range[1]):
            row_section = "".join(patched_section[row-y_range[0]])
            level[row] = level[row][:x_range[0]] + row_section + level[row][x_range[1]:]

        return level
