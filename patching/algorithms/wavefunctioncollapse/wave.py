from __future__ import annotations

import numpy as np

from patching.algorithms.wavefunctioncollapse import PatternScanner, Direction, Pattern


class WaveFunction:
    def __init__(self, pattern_scanner: PatternScanner):
        self.pattern_scanner = pattern_scanner

        self.patterns = self.pattern_scanner.get_full_pattern_set()

        self.entropy = 0.0
        self.calculate_entropy()

    def __hash__(self) -> int:
        return hash(self.patterns)

    def __eq__(self, other: WaveFunction) -> bool:
        return self.patterns == other.patterns

    def is_collapsed(self) -> bool:
        return len(self.patterns) == 1

    def is_contradictory(self) -> bool:
        return len(self.patterns) == 0

    # Returns true if the wave function has changed.
    def apply_constraints(self, constraints: set[Pattern]) -> bool:
        old_patterns = self.patterns.copy()
        self.patterns.intersection_update(constraints)
        self.calculate_entropy()

        return self.patterns != old_patterns

    def collect_adjacencies(self, direction: Direction) -> set[Pattern]:
        adjacencies: set[Pattern] = set()

        for pattern in self.patterns:
            if direction in pattern.adjacencies:
                adjacencies.update(pattern.adjacencies[direction])

        return adjacencies

    def calculate_entropy(self):
        return len(self.patterns)

    def observe(self):
        patterns = list(self.patterns)
        weight = [self.pattern_scanner.get_pattern_weight(pattern) for pattern in patterns]
        weight_sum = np.sum(weight)

        self.patterns = set()
        self.patterns.add(np.random.choice(patterns, p=[weight / weight_sum for weight in weight]))