from patching import Patcher


class LaunchpadPatcher(Patcher):
    """
    This patcher uses the Launchpad generator by Smith et al. to fix broken level sections
    """
    def patch(self, level: list[str], broken_spot) -> list[str]:
        pass
