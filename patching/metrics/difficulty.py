import numpy as np
import py4j.java_gateway

from patching.metrics.metric import Metric
from utils.token_defs import *


class Difficulty(Metric):
    def __init__(self):
        self.original_difficulty: float = 0.0
        self.generated_difficulty: float = 0.0

    def pre_hook(
        self,
        original_level: list[str],
        original_mario_result: py4j.java_gateway.JavaObject,
        generated_level: list[str],
        generated_mario_result: py4j.java_gateway.JavaObject,
    ):
        self.original_difficulty = difficulty(original_level, original_mario_result)
        self.generated_difficulty = difficulty(generated_level, generated_mario_result)

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
        return {
            "Difficulty original": self.original_difficulty,
            "Difficulty generated": self.generated_difficulty,
            "Difficulty fixed": difficulty(fixed_level, mario_result)
        }


def difficulty(level: list[str], mario_result: py4j.java_gateway.JavaObject) -> float:
    """
    Consists of a static and a dynamic evaluation.
    Static evaluation is based on data gathered by analysing the level itself.
    Dynamic evaluation is based on data gathered by the Mario AI Framework agent playing the level
    :param level: Level to analyse
    :param mario_result: Data gathered by the AI agent, type is MarioResult (see Mario AI Framework)
    :return: Difficulty score, higher meaning more difficult
    """
    # Convert level to numpy ndarray
    level = np.array([list(row) for row in level])

    # Determine the height for every vertical column
    width: int = level.shape[1]
    height: int = level.shape[0]

    enemy_count: int = 0
    cannon_count: int = 0
    tube_count: int = 0
    powerup_count: int = 0

    path = mario_result.getMarioPath()  # ArrayList<MarioPosition>

    current_gap_width = 0
    jumps: list[int] = []  # List of gap lengths mario jumped over
    covered_x_position = 0
    for position in path:
        x_pos = position.getX()
        y_pos = position.getY()

        if x_pos <= covered_x_position:
            continue

        is_gap = True
        for y in range(y_pos, height):
            if level[y][x_pos] not in NON_BLOCKS:
                is_gap = False
                break

        covered_x_position += 1

        level[y_pos][x_pos] = MARIO_PATH_TOKEN

        if is_gap:
            current_gap_width += 1
        else:
            if current_gap_width > 0:
                jumps.append(current_gap_width)
                current_gap_width = 0

    easy_jumps = 0
    difficult_jumps = 0
    for jump in jumps:
        if jump <= 6:
            easy_jumps += 1
        else:
            difficult_jumps += 1

    for column in range(width - 1):
        enemy_count += count_enemies(level[:, column])
        cannon_count += count_cannon(level[:, column])
        tube_count += count_tubes((level[:, column], level[:, column + 1]))
        powerup_count += count_powerups(level[:, column])

    score = \
        + enemy_count \
        + cannon_count \
        + tube_count \
        - powerup_count \
        + easy_jumps * 0.5 \
        + difficult_jumps * 2.0 \

    return score


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
