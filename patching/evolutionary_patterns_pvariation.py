from __future__ import annotations

import numpy as np
import py4j.java_gateway

from patching.metrics.pattern_variation import pattern_variation
from patching.patcher import Patcher

GENERATIONS = 100
POPULATION_SIZE = 20


class EvolutionaryPatternsPVariation(Patcher):
    """
    Uses an evolutionary algorithm to evolve a replacement section for the broken one.
    A specimen has <level_height> horizontal slices, which are the width of the broken section + 2 (+1 for each side).
    These slices are extracted from the original level.
    The fitness function is the similarity function as used for the best fit stitching.
    """

    def patch(
            self,
            original_level: list[str],
            level: list[str],  # Level formatted as a list of strings row-wise
            broken_range: tuple[tuple[int, int], tuple[int, int]],  # (x_range, y_range)
            generator_path: str = "",
            mario_result: py4j.java_gateway.JavaObject = None,
    ) -> list[str]:
        population = Population(level, original_level, broken_range)

        for _ in range(GENERATIONS):
            population.step()

        best = population.best_specimen()
        return [''.join(row) for row in best]


class Population:
    def __init__(
            self,
            level: list[str],
            original_level: list[str],
            broken_range: tuple[tuple[int, int], tuple[int, int]]
    ):
        self.original_pattern_variation = pattern_variation(level)

        self.level = np.array([list(row) for row in level])
        self.generated_level = np.array([list(row) for row in level])
        self.original_level = np.array([list(row) for row in original_level])

        self.broken_range = broken_range
        x_range, y_range = broken_range
        self.slice_width = (x_range[1] - x_range[0]) + 2

        self.population = []
        for _ in range(POPULATION_SIZE):
            slices = []
            for row in range(self.original_level.shape[0]):
                slices.append(self.rng_slice())

            self.population.append(Specimen(slices))

    def rng_slice(self) -> np.ndarray:
        x = np.random.randint(0, self.original_level.shape[1] - self.slice_width)
        y = np.random.randint(0, self.original_level.shape[0])

        return self.original_level[y:y+1, x:x+self.slice_width].flatten()

    def step(self):
        # Sort the population by fitness (descending), higher is better
        self.population.sort(key=self.evaluate, reverse=True)

        # Replace the bottom 50% of the population with offspring
        for i in range(len(self.population) // 2):
            # Select the two best specimens
            parent_1 = self.population[i]
            parent_2 = self.population[i + 1]

            # Create two new specimens by performing one-point crossover
            child_1, child_2 = parent_1.crossover(parent_2)

            # Replace the worst two specimens with the children
            self.population[-(i + 1)] = child_1
            self.population[-(i + 2)] = child_2

        # Mutate all specimens
        for specimen in self.population:
            if np.random.rand() < 0.5:
                specimen.mutate(self.rng_slice())

    def evaluate(self, specimen: Specimen) -> float:
        x_range, y_range = self.broken_range

        for row in range(y_range[1]):
            lslice = specimen.slice_set[row]
            self.level[row, x_range[0]:x_range[1]] = lslice[1:lslice.shape[0]-1]

        return 1.0 / (1.0 + abs(pattern_variation(self.level) - self.original_pattern_variation))

    def best_specimen(self) -> np.ndarray:
        best: Specimen = self.population[0]

        x_range, y_range = self.broken_range

        for row in range(y_range[1]):
            lslice = best.slice_set[row]
            self.level[row, x_range[0]:x_range[1]] = lslice[1:lslice.shape[0]-1]

        return self.level


class Specimen:
    def __init__(self, slice_set: list[np.ndarray]):
        self.slice_set = slice_set.copy()

    def mutate(self, random_slice: np.ndarray):
        self.slice_set[np.random.randint(len(self.slice_set))] = random_slice

    def crossover(self, other: Specimen) -> (Specimen, Specimen):
        # Perform one-point crossover and create two new specimens
        # Randomly select a point in the slice_set
        # point = np.random.randint(len(self.slice_set))
        point = len(self.slice_set) // 2

        # Create two new specimens by swapping the slices after the point
        new_specimen_1 = Specimen(self.slice_set)
        new_specimen_2 = Specimen(other.slice_set)

        new_specimen_1.slice_set[point:] = other.slice_set[point:]
        new_specimen_2.slice_set[point:] = self.slice_set[point:]

        return new_specimen_1, new_specimen_2
