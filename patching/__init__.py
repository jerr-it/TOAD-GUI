from patching.best_fit_stitching import BestFitStitching
from patching.evolutionary_patterns import EvolutionaryPatterns
from patching.stitching import Stitching
from patching.wfc import WFCPatcher


patchers = {
    "Wave Function Collapse": WFCPatcher(),
    "Stitching": Stitching(),
    "Best fit stitching": BestFitStitching(),
    "Evolutionary Patterns": EvolutionaryPatterns(),
}
