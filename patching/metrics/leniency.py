import numpy as np

from patching.metrics.metric import Metric
from token_defs import *


class LeniencyChange(Metric):
    """
    Leniency is a metric for estimating the difficulty of a level.
    Its definitions are all somewhat different:
    Horn et al, Shaker et al, Smith et al
    Generally it assigns a score to a levels components, for example:
    -1 for enemies
    +1 for powerups
    ...
    """

    def pre_hook(self):
        pass

    def post_hook(
            self,
            original_level: list[str],
            generated_level: list[str],
            fixed_level: list[str],
    ):
        return leniency(fixed_level) - leniency(generated_level)


def leniency(level: list[str]) -> float:
    # Shaker et al:
    # Attribute, Weight:
    # Gap count, -0.5
    # Average gap width, -1
    # Enemy count, -1
    # Cannon / Bullet Bill count, -0.5
    # Powerup count, +1

    # Convert level to numpy ndarray
    level = np.array([list(row) for row in level])

    # Determine the height for every vertical column
    width: int = level.shape[1]
    heights: list[int] = [0] * width

    for column in range(width):
        # Move down the column until we find a non "-" character
        for row in range(level.shape[0]):
            if level[row][column] != "-":
                heights[column] = level.shape[0] - row
                break

    # Iterate all vertical columns
    current_gap_width: int = 0

    gap_count: int = 0
    average_gap_width: float = 0.0
    enemy_count: int = 0
    cannon_tube_count: int = 0
    powerup_count: int = 0

    for column in range(width - 1):
        if heights[column] == 0:
            current_gap_width += 1
        else:
            if current_gap_width > 0:
                gap_count += 1
                average_gap_width += current_gap_width
                current_gap_width = 0

        enemy_count += count_enemies(level[:, column])
        cannon_tube_count += count_cannon(level[:, column]) + count_tubes((level[:, column], level[:, column + 1]))

    average_gap_width /= gap_count

    # Normalize return value to [0, 1]
    le = gap_count * -0.5 + \
         average_gap_width * -1 + \
         enemy_count * -1 + \
         cannon_tube_count * -0.5 + \
         powerup_count * 1 \
         / (gap_count + average_gap_width + enemy_count + cannon_tube_count + powerup_count)

    return le


def count_enemies(column: np.ndarray) -> int:
    # Count enemies in a column
    enemies: int = 0
    for row in range(column.shape[0]):
        if column[row] in [GOOMBA, KOOPA, FLYING_KOOPA, SPINY]:
            enemies += 1
    return enemies


def count_cannon(column: np.ndarray) -> int:
    # Count cannon in a column
    # Can at most be 2 per column
    cannon: int = 0
    reached: int = 0

    for row in range(column.shape[0]):
        if column[row] == CANNON:
            cannon += 1
            reached = row
            break

    # Bullet bill cannons can be stacked, which is indicated by a "B" in the column below the '*' characters
    for r2 in range(reached, column.shape[0]):
        if column[r2] == CANNON_BASE:
            cannon += 1
            break

    return cannon


def count_tubes(columns: tuple[np.ndarray, np.ndarray]) -> int:
    # Receives two columns, since tubes are 2 blocks wide and we dont want to count them twice
    # Can at most be 1 per 2-pair of columns
    tubes: int = 0
    for row in range(columns[0].shape[0]):
        if columns[row][0] == FLOWER_TUBE and columns[row][1] == FLOWER_TUBE:
            tubes += 1
            break

    return tubes


def count_powerups(column: np.ndarray) -> int:
    # Count powerups in a column
    powerups: int = 0
    for row in range(column.shape[0]):
        if column[row] in [QUESTION_LEVEL_UP, BRICK_LEVEL_UP, HIDDEN_ONE_UP, BRICK_ONE_UP]:
            powerups += 1
    return powerups
