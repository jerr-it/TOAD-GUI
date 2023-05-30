from patching.best_fit_stitching import BestFitStitching
from patching.evolutionary_patterns import EvolutionaryPatterns
from patching.mariogpt import MarioGPT
from patching.online import Online
from patching.stitching import Stitching
from patching.wfc import WFCPatcher

patchers = {
    # "MarioGPT": MarioGPT(),
    # "Online": Online(),
    "Stitching": Stitching(),
    "Best fit stitching": BestFitStitching(),
    "Evolutionary Patterns": EvolutionaryPatterns(),
    "Wave Function Collapse": WFCPatcher(),
}
