from patching.evolutionary_patterns import EvolutionaryPatterns
from patching.stitching import StichingPatcher
from patching.wfc import WFCPatcher

GENERATE_STAGE_THREADS = 6
REPAIR_STAGE_THREADS = 8

patchers = {
    "Wave Function Collapse": WFCPatcher(),
    "Stitching": StichingPatcher(),
    "Evolutionary Patterns": EvolutionaryPatterns(),
}
