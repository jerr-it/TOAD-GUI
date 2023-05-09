from patching.metrics.leniency import LeniencyOriginal, LeniencyGenerated, LeniencyFixed
from patching.metrics.memory import Memory
from patching.metrics.pattern_variation import PatternVariationOriginal, PatternVariationGenerated, PatternVariationFixed
from patching.metrics.runtime import Runtime
from patching.metrics.tpkl import TPKLOriginalGenerated, TPKLOriginalFixed
from patching.metrics.tries import Tries

metrics = [
    {"name": "TPKL Original Generated", "unit": "", "object": TPKLOriginalGenerated()},
    {"name": "TPKL Original Fixed", "unit": "", "object": TPKLOriginalFixed()},
    {"name": "Pattern Variation Original", "unit": "", "object": PatternVariationOriginal()},
    {"name": "Pattern Variation Generated", "unit": "", "object": PatternVariationGenerated()},
    {"name": "Pattern Variation Fixed", "unit": "", "object": PatternVariationFixed()},
    {"name": "Tries", "unit": "", "object": Tries()},
    # {"name": "Leniency Original", "unit": "", "object": LeniencyOriginal()},
    # {"name": "Leniency Generated", "unit": "", "object": LeniencyGenerated()},
    # {"name": "Leniency Fixed", "unit": "", "object": LeniencyFixed()},
    {"name": "Memory", "unit": "B", "object": Memory()},
    {"name": "Runtime", "unit": "s", "object": Runtime()}
]
