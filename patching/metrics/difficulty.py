import numpy as np
import py4j.java_gateway

from patching.metrics.metric import Metric
from utils.token_defs import *

ENEMY_SCORES = {
    "g": 1,     # Goomba
    "G": 1.5,   # Winged Goomba
    "k": 1.5,   # Green Koopa
    "K": 2.0,   # Winged green Koopa
    "r": 1.75,  # Red Koopa
    "R": 2.25,  # Red Winged Koopa
    "y": 2.0,   # Spiny
    "Y": 2.5,   # Winged Spiny
}


class Difficulty(Metric):
    def __init__(self):
        self.original_difficulty: float = 0.0
        self.generated_difficulty: float = 0.0
        self.lookup_table = {}

    def pre_hook(
            self,
            original_level: list[str],
            original_mario_result: py4j.java_gateway.JavaObject,
            generated_level: list[str],
            generated_mario_result: py4j.java_gateway.JavaObject,
    ):
        original_key = "@".join(original_level)

        if original_key in self.lookup_table:
            self.original_difficulty = self.lookup_table[original_key]
        else:
            orig_difficulty = difficulty(original_level, original_mario_result)
            self.lookup_table[original_key] = orig_difficulty
            self.original_difficulty = orig_difficulty

        generated_key = "@".join(generated_level)

        if generated_key in self.lookup_table:
            self.generated_difficulty = self.lookup_table[generated_key]
        else:
            gen_difficulty = difficulty(generated_level, generated_mario_result)
            self.lookup_table[generated_key] = gen_difficulty
            self.generated_difficulty = gen_difficulty

    def iter_hook(
            self,
            mario_result: py4j.java_gateway.JavaObject,
            fixed_level: list[str],
    ):
        pass

    def post_hook(
            self,
            mario_result: py4j.java_gateway.JavaObject,
            original_level: list[str],
            generated_level: list[str],
            fixed_level: list[str],
    ):
        fixed_key = "@".join(fixed_level)

        if fixed_key in self.lookup_table:
            fixed_difficulty = self.lookup_table[fixed_key]
        else:
            nplevel = np.array([list(row) for row in fixed_level])
            fixed_difficulty = difficulty(nplevel, mario_result)
            self.lookup_table[fixed_key] = fixed_difficulty

        return {
            "Difficulty original": self.original_difficulty,
            "Difficulty generated": self.generated_difficulty,
            "Difficulty fixed": fixed_difficulty
        }


def convert_path(nplevel, mario_result, width) -> list[int]:
    path: list[int] = [0] * width

    for position in mario_result.getMarioPath():
        x: int = int(position.getX() * 16.0)
        y: int = int(position.getY() * 16.0)

        if x < 0 or x >= nplevel.shape[0]:
            continue

        if y >= nplevel.shape[1]:
            continue

        if y > path[x]:
            path[x] = y
    return path


def difficulty(level: list[str] | np.ndarray, mario_result: py4j.java_gateway.JavaObject) -> float:
    """
    Consists of a static and a dynamic evaluation.
    Static evaluation is based on data gathered by analysing the level itself.
    Dynamic evaluation is based on data gathered by the Mario AI Framework agent playing the level
    :return: Difficulty score, higher meaning more difficult
    """
    # Convert level to numpy ndarray
    if isinstance(level, list):
        level = np.array([list(row) for row in level])

    # Determine the height for every vertical column
    width: int = level.shape[1]

    path = convert_path(level, mario_result, width)

    static_score: float = 0.0

    for column_start in range(width-1):
        section = level[:, column_start:column_start + 2]

        left_column = level[:, column_start]
        right_column = level[:, column_start + 1]

        enemy_count = count_enemies(left_column) + count_enemies(right_column)
        cannon_count = count_cannon(left_column) + count_cannon(right_column)
        tube_count = count_tubes(section)
        powerup_count = count_powerups(left_column) + count_powerups(right_column)

        static_score += enemy_count + cannon_count + tube_count - powerup_count

    dynamic_score = count_gaps(level, path)

    score = 0.4 * static_score + 0.6 * dynamic_score

    return score


def count_gaps(level: np.ndarray, path: list[int]) -> int:
    gap_count: int = 0
    width: int = level.shape[1]

    for column in range(width):
        mario_height = path[column]
        is_gap = True
        for h in range(mario_height, level.shape[0]):
            if level[h, column] not in NON_BLOCKS:
                is_gap = False
                break

        if is_gap:
            gap_count += 1

    return gap_count


def count_enemies(column: np.ndarray) -> int:
    # Count enemies in a column
    enemies: int = 0
    for row in range(column.shape[0]):
        if column[row] in [GOOMBA, KOOPA, FLYING_KOOPA, SPINY, RED_KOOPA, RED_FLYING_KOOPA]:
            enemies += ENEMY_SCORES[column[row]]
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
        if columns[0][row] == FLOWER_TUBE and columns[1][row] == FLOWER_TUBE:
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
