from patching.metrics.memory import Memory
from patching.metrics.runtime import Runtime

metrics = [
    {"name": "Memory", "unit": "B", "object": Memory()},
    {"name": "Runtime", "unit": "s", "object": Runtime()}
]
