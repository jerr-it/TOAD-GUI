from patching.metrics.memory import Memory
from patching.metrics.pattern_variation import PatternVariationChange
from patching.metrics.runtime import Runtime
from patching.metrics.tpkl import TPKLChange

metrics = [
    {"name": "TPKL Change", "unit": "", "object": TPKLChange()},
    {"name": "Pattern variance change", "unit": "", "object": PatternVariationChange()},
    {"name": "Memory", "unit": "B", "object": Memory()},
    {"name": "Runtime", "unit": "s", "object": Runtime()}
]
