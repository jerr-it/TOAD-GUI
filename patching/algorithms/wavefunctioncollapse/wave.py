from __future__ import annotations

import numpy as np

from patching.algorithms.wavefunctioncollapse.adapters.pattern_scanner import PatternScanner
from patching.algorithms.wavefunctioncollapse.pattern import Pattern, Direction


class WaveFunction:
    def __init__(self, inp: PatternScanner | int):
        if isinstance(inp, PatternScanner):
            self.pattern_scanner = inp

            self.patterns: set[int] = self.pattern_scanner.get_full_pattern_set()

            self.entropy = self.calculate_entropy()
        else:
            self.patterns = {inp}

            self.entropy = -1

    def __hash__(self) -> int:
        return hash(self.patterns)

    def __eq__(self, other: WaveFunction) -> bool:
        return self.patterns == other.patterns

    def is_collapsed(self) -> bool:
        return len(self.patterns) == 1

    def is_contradictory(self) -> bool:
        return len(self.patterns) == 0

    # Returns true if the wave function has changed.
    def apply_constraints(self, constraints: set[int]) -> bool:
        old_patterns = self.patterns.copy()
        self.patterns.intersection_update(constraints)
        self.entropy = self.calculate_entropy()

        return self.patterns != old_patterns

    def collect_adjacencies(self, direction: Direction) -> set[int]:
        adjacencies: set[int] = set()

        for pattern_idx in self.patterns:
            pattern: Pattern = self.pattern_scanner.get_pattern_entry(pattern_idx)[0]
            if direction in pattern.adjacencies:
                adjacencies.update(pattern.adjacencies[direction])

        return adjacencies

    def calculate_entropy(self):
        return len(self.patterns)

    def observe(self):
        patterns = list(self.patterns)
        weight = [self.pattern_scanner.get_pattern_entry(pattern)[1] for pattern in patterns]
        weight_sum = np.sum(weight)

        self.patterns = set()
        self.patterns.add(np.random.choice(patterns, p=[weight / weight_sum for weight in weight]))
