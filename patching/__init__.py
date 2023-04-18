from patching.stitching import StichingPatcher
from patching.wfc import WFCPatcher

GENERATE_STAGE_THREADS = 4
REPAIR_STAGE_THREADS = 8

patchers = {
    "Wave Function Collapse": WFCPatcher(),
    "Stitching": StichingPatcher(),
}
