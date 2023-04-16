from patching.metrics.memory import Memory
from patching.metrics.runtime import Runtime
from patching.metrics.tpkl import TPKLGenerated, TPKLPatched

metrics = [
    {"name": "TPKL Generated", "unit": "", "object": TPKLGenerated()},
    {"name": "TPKL Patched", "unit": "", "object": TPKLPatched()},
    {"name": "Memory", "unit": "B", "object": Memory()},
    {"name": "Runtime", "unit": "s", "object": Runtime()}
]
