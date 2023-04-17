from patching.metrics.memory import Memory
from patching.metrics.pattern_variation import PatternVariationGenerated, PatternVariationFixed
from patching.metrics.runtime import Runtime
from patching.metrics.tpkl import TPKLGenerated, TPKLPatched

metrics = [
    {"name": "TPKL Generated", "unit": "", "object": TPKLGenerated()},
    {"name": "TPKL Patched", "unit": "", "object": TPKLPatched()},
    {"name": "Pattern variance generated", "unit": "", "object": PatternVariationGenerated()},
    {"name": "Pattern variance fixed", "unit": "", "object": PatternVariationFixed()},
    {"name": "Memory", "unit": "B", "object": Memory()},
    {"name": "Runtime", "unit": "s", "object": Runtime()}
]
