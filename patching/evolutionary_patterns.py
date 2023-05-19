from __future__ import annotations

import numpy as np

from patching.metrics.tpkl import tpkl
from patching.patcher import Patcher

GENERATIONS = 10
POPULATION_SIZE = 10


class EvolutionaryPatterns(Patcher):
    def patch(
            self,
            original_level: list[str],
            level: list[str],  # Level formatted as a list of strings row-wise
            broken_range: tuple[tuple[int, int], tuple[int, int]],  # (x_range, y_range)
            generator_path: str
    ) -> list[str]:
        x_range, y_range = broken_range
        population = Population(level, x_range[1] - x_range[0], original_level, broken_range)

        for _ in range(GENERATIONS):
            population.step()

        best = population.best_specimen()
        return [''.join(row) for row in best]


class Population:
    def __init__(
            self,
            level: list[str],
            width: int,
            original_level: list[str],
            broken_range: tuple[tuple[int, int], tuple[int, int]]
    ):
        self.width = width

        self.level = np.array([list(row) for row in level])
        self.generated_level = np.array([list(row) for row in level])
        self.original_level = np.array([list(row) for row in original_level])
        self.broken_range = broken_range

        self.base_tpkl = tpkl(self.original_level, self.generated_level)

        self.slice_set = []

        # Extract all vertical slices from np_level
        for x in range(self.level.shape[1]):
            self.slice_set.append(self.level[:, x])

        # Create a population of specimens
        self.population = []
        for _ in range(POPULATION_SIZE):
            # Pick a random set of slices, returns indices
            rng_slices = np.random.choice(len(self.slice_set), size=self.width)
            # Convert indices to the actual slices
            slices = [self.slice_set[i] for i in rng_slices]

            self.population.append(Specimen(slices))

    def step(self):
        # Sort the population by fitness (ascending), lower is better
        self.population.sort(key=self.evaluate)

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
            specimen.mutate(self.slice_set)

    def evaluate(self, specimen: Specimen) -> float:
        # Replace the slices in the generated level with the slices from the specimen
        for x in range(self.broken_range[0][0], self.broken_range[0][1]):
            self.level[:, x] = specimen.slice_set[x - self.broken_range[0][0]]

        # Calculate the fitness of the specimen
        return self.base_tpkl - tpkl(self.original_level, self.level)

    def best_specimen(self) -> np.ndarray:
        # Find the best specimen in the population
        best: Specimen = self.population[0]
        # Insert specimen into level
        for x in range(self.broken_range[0][0], self.broken_range[0][1]):
            self.level[:, x] = best.slice_set[x - self.broken_range[0][0]]

        return self.level


class Specimen:
    def __init__(self, slice_set: list[np.ndarray]):
        self.slice_set = slice_set.copy()

    def mutate(self, slice_set: list[np.ndarray]):
        # Randomly select a slice from self.slice_set and replace it with a random slice from slice_set
        # TODO replace, random.choice returns indices, not slices
        rng_slice = np.random.choice(len(slice_set))
        self.slice_set[np.random.randint(len(self.slice_set))] = slice_set[rng_slice]

    def crossover(self, other: Specimen) -> (Specimen, Specimen):
        # Perform one-point crossover and create two new specimens
        # Randomly select a point in the slice_set
        point = np.random.randint(len(self.slice_set))

        # Create two new specimens by swapping the slices after the point
        new_specimen_1 = Specimen(self.slice_set)
        new_specimen_2 = Specimen(other.slice_set)

        new_specimen_1.slice_set[point:] = other.slice_set[point:]
        new_specimen_2.slice_set[point:] = self.slice_set[point:]

        return new_specimen_1, new_specimen_2
