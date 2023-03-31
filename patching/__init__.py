from .patcher import Patcher

from .wfc import WFCPatcher
from .ea import EAPatcher
from .lsystem import LSystemPatcher
from .multipass import MultiPassPatcher
from .launchpad import LaunchpadPatcher

patchers = {
    "Wave Function Collapse": WFCPatcher(),
}
