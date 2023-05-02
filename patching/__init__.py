from patching.evolutionary_patterns import EvolutionaryPatterns
from patching.stitching import StichingPatcher
from patching.wfc import WFCPatcher


patchers = {
    "Wave Function Collapse": WFCPatcher(),
    "Stitching": StichingPatcher(),
    "Evolutionary Patterns": EvolutionaryPatterns(),
}
